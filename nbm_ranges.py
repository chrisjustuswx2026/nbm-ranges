"""
SDR Weather Intelligence: National Blend of Models (NBM) forecast ranges for the whole U.S.

Every run:
  1. finds the newest NBM run on NOAA's free AWS bucket that has the percentile ("qmd") files
  2. downloads ONLY the pieces we need: 24-hour rain, snow and ice at the 10th / 50th / 90th percentile
     (Min / Likely / Max), for the next 7 days
  3. samples them every 0.1 degree (about 6-7 miles) across the lower 48
  4. writes small files, one per 1x1 degree square, that any dashboard can read:
        public/latest.json           what run this is, which days, which variables
        public/t/{lat}_{lon}.json    the numbers for one square (lat/lon = the square's SW corner, whole degrees)

No keys, no accounts: NOAA's bucket is public. GitHub Actions runs this on a schedule and publishes /public.
Run by hand:  python nbm_ranges.py public
"""
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import numpy as np

BUCKET = "https://noaa-nbm-grib2-pds.s3.amazonaws.com"
OUT = sys.argv[1] if len(sys.argv) > 1 else "public"

STEP = 0.1                                   # grid spacing in degrees (~6-7 miles)
LAT0, LAT1, LON0, LON1 = 24.0, 50.0, -125.0, -66.0
PCTS = (10, 50, 90)                          # Min / Likely / Max
DAYS = 7
VARS = {"APCP": "rain", "ASNOW": "snow", "FICEAC": "ice"}   # GRIB short name -> our name


def log(*a):
    print(*a, flush=True)


def get(url, rng=None, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SDR-Weather-Intelligence-NBM/1.0"})
            if rng:
                req.add_header("Range", "bytes=%d-%s" % (rng[0], "" if rng[1] is None else rng[1]))
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:
            if k == tries - 1:
                raise
            log("  retry", url, e)
            time.sleep(3 * (k + 1))


def list_keys(prefix):
    keys, token = [], None
    ns = "{http://s3.amazonaws.com/doc/2006-03-01/}"
    while True:
        url = f"{BUCKET}/?list-type=2&prefix={prefix}" + (f"&continuation-token={urllib.parse.quote(token)}" if token else "")
        root = ET.fromstring(get(url))
        keys += [c.find(ns + "Key").text for c in root.findall(ns + "Contents")]
        if root.findtext(ns + "IsTruncated") == "true":
            token = root.findtext(ns + "NextContinuationToken")
        else:
            return keys


# ---------- 1. newest run that has 7 days of percentile files ----------
def find_run():
    now = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
    fallback = None
    for back in range(0, 36):
        t = now - dt.timedelta(hours=back)
        prefix = f"blend.{t:%Y%m%d}/{t:%H}/qmd/"
        try:
            keys = [k for k in list_keys(prefix) if k.endswith(".co.grib2.idx")]
        except Exception as e:
            log("list failed", prefix, e)
            continue
        if not keys:
            continue
        fhs = sorted(int(re.search(r"\.f(\d{3})\.", k).group(1)) for k in keys)
        log(f"run {t:%Y-%m-%d %HZ}: {len(keys)} percentile files, f{fhs[0]:03d}-f{fhs[-1]:03d}")
        # a run younger than ~3 h may still be uploading; need the last file of a 7-day window
        if fhs[-1] >= 24 * DAYS + 12:
            return t, keys
        fallback = fallback or (t, keys)
    if fallback:
        log("no complete 7-day run found, using the newest partial run")
        return fallback
    raise SystemExit("No NBM percentile (qmd) files found in the last 36 hours.")


# ---------- 2. read the index files, pick the messages we want ----------
IDX = re.compile(r"^(\d+):(\d+):d=(\d{10}):([^:]+):([^:]*):([^:]*):(.*?):?$")


def window_hours(fc):
    """'12-36 hour acc fcst' -> (12, 36); '0-1 day acc fcst' -> (0, 24); otherwise None."""
    m = re.search(r"(\d+)-(\d+) hour acc", fc)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"(\d+)-(\d+) day acc", fc)
    if m:
        return int(m.group(1)) * 24, int(m.group(2)) * 24
    return None


def pick_messages(run, keys):
    wanted, seen_names = {}, set()
    for key in sorted(keys):
        lines = get(f"{BUCKET}/{key}").decode("utf-8", "replace").strip().splitlines()
        rows = [IDX.match(l) for l in lines]
        rows = [r for r in rows if r]
        for i, r in enumerate(rows):
            var, level, fc, extra = r.group(4), r.group(5), r.group(6), r.group(7)
            seen_names.add(f"{var}:{level}:{fc}:{extra}"[:90])
            if var not in VARS or "surface" not in level:
                continue
            p = re.search(r"(\d+)% level", extra)
            if not p or int(p.group(1)) not in PCTS:
                continue
            w = window_hours(fc)
            if not w or w[1] - w[0] != 24:
                continue
            start = int(r.group(2))
            end = int(rows[i + 1].group(2)) - 1 if i + 1 < len(rows) else None
            grib = key[:-4]
            wanted[(VARS[var], int(p.group(1)), w)] = (grib, start, end)
    if not wanted:
        log("Nothing matched. Sample of what the index files contain (send this to Claude):")
        for s in sorted(seen_names)[:80]:
            log("   ", s)
        raise SystemExit(1)
    return wanted


def choose_days(run, wanted):
    """7 back-to-back 24 h windows. Prefer windows ending at 12Z (the usual 7 AM-7 AM 'day')."""
    by_end = {}
    for (name, pct, w) in wanted:
        by_end.setdefault(w, set()).add(name)
    wins = sorted(by_end)
    for hour in (12, 0, 6, 18):
        sel = [w for w in wins if (run + dt.timedelta(hours=w[1])).hour == hour and w[0] >= 0]
        if len(sel) >= 3:
            return sel[:DAYS]
    return wins[:DAYS]


# ---------- 3. decode + sample on a regular 0.1 degree grid ----------
def decode(blob):
    import pygrib
    msg = pygrib.fromstring(blob)
    vals = np.ma.filled(msg.values.astype("float32"), np.nan)
    units = str(getattr(msg, "units", "")).lower()
    if not hasattr(decode, "ll"):
        decode.ll = msg.latlons()
    return vals, units


def to_inches(vals, units, name):
    if units in ("m", "metre", "meter", "m of water equivalent"):
        return vals * 39.3701
    # kg m-2 == mm of water
    return vals / 25.4


def build_index(lat2d, lon2d):
    from scipy.spatial import cKDTree
    lats = np.arange(LAT0, LAT1 + 1e-6, STEP)
    lons = np.arange(LON0, LON1 + 1e-6, STEP)
    LA, LO = np.meshgrid(lats, lons, indexing="ij")
    src_lon = np.where(lon2d > 180, lon2d - 360, lon2d)
    k = np.cos(np.radians(37.0))
    tree = cKDTree(np.column_stack([lat2d.ravel(), src_lon.ravel() * k]))
    dist, idx = tree.query(np.column_stack([LA.ravel(), LO.ravel() * k]))
    idx[dist > 0.08] = -1                     # outside the NBM grid
    return lats, lons, idx.reshape(LA.shape)


# ---------- 4. write the files ----------
def main():
    t0 = time.time()
    run, keys = find_run()
    wanted = pick_messages(run, keys)
    days = choose_days(run, wanted)
    names = [n for n in ("rain", "snow", "ice") if any((n, p, w) in wanted for p in PCTS for w in days)]
    log("days:", [(run + dt.timedelta(hours=a)).strftime("%a %HZ") + "->" + (run + dt.timedelta(hours=b)).strftime("%a %HZ") for a, b in days])
    log("variables:", names)

    grid = None   # [name] -> array (lat, lon, day, pct) in hundredths of an inch
    lats = lons = idx = None
    for name in names:
        for di, w in enumerate(days):
            for pi, pct in enumerate(PCTS):
                hit = wanted.get((name, pct, w))
                if not hit:
                    continue
                grib, a, b = hit
                vals, units = decode(get(f"{BUCKET}/{grib}", (a, b)))
                if idx is None:
                    lats, lons, idx = build_index(*decode.ll)
                    grid = {n: np.full(idx.shape + (len(days), len(PCTS)), -1, dtype=np.int32) for n in names}
                flat = to_inches(vals.ravel(), units, name)
                v = np.where(idx >= 0, flat[np.clip(idx, 0, None)], np.nan)
                grid[name][:, :, di, pi] = np.where(np.isfinite(v), np.round(np.clip(v, 0, None) * 100), -1).astype(np.int32)
                log(f"  {name} p{pct} {w[0]}-{w[1]}h  units={units or '?'}  max={np.nanmax(v):.2f} in")

    os.makedirs(os.path.join(OUT, "t"), exist_ok=True)
    per = int(round(1 / STEP))
    n_files = 0
    for la in range(int(LAT0), int(LAT1)):
        for lo in range(int(LON0), int(LON1)):
            r0, c0 = int(round((la - LAT0) / STEP)), int(round((lo - LON0) / STEP))
            sub = {n: grid[n][r0:r0 + per, c0:c0 + per] for n in names}
            if all((s < 0).all() for s in sub.values()):
                continue
            doc = {"lat0": la, "lon0": lo, "step": STEP, "n": per,
                   # each variable: rows south->north, cols west->east, then day, then [min, likely, max], hundredths of an inch, -1 = no data
                   **{n: sub[n].tolist() for n in names}}
            with open(os.path.join(OUT, "t", f"{la}_{lo}.json"), "w") as f:
                json.dump(doc, f, separators=(",", ":"))
            n_files += 1

    meta = {
        "source": "NOAA National Blend of Models (NBM) percentiles, 10th / 50th / 90th",
        "run": run.strftime("%Y-%m-%dT%H:00Z"),
        "made": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "days": [{"start": (run + dt.timedelta(hours=a)).strftime("%Y-%m-%dT%H:00Z"),
                  "end": (run + dt.timedelta(hours=b)).strftime("%Y-%m-%dT%H:00Z")} for a, b in days],
        "vars": names, "pcts": list(PCTS), "units": "hundredths of an inch",
        "step": STEP, "tile": "t/{lat}_{lon}.json  (lat, lon = floor of the point)",
    }
    with open(os.path.join(OUT, "latest.json"), "w") as f:
        json.dump(meta, f, indent=1)
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(f"<!doctype html><meta charset=utf-8><title>SDR NBM ranges</title><body style='font-family:system-ui;background:#0A1428;color:#F4F7FB;padding:24px'>"
                f"<h1>SDR forecast ranges are running</h1><p>Run {meta['run']} &middot; made {meta['made']} &middot; {n_files} squares &middot; {', '.join(names)}</p>"
                f"<p>Test a spot: <a style='color:#6FB7FF' href='t/34_-83.json'>Clemson square</a> &middot; <a style='color:#6FB7FF' href='latest.json'>latest.json</a></p>")
    log(f"done: {n_files} files in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
