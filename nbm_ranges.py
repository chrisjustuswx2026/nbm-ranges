"""
SDR Weather Intelligence: 10-day guidance for the whole U.S. from NOAA's National Blend of Models (NBM),
plus soil temperature from NOAA's GFS. Free, public data; no keys.

Per point (every 0.1 degree, about 6-7 miles) and per day (10 days), it keeps:
  rain, snow, ice      Min / Likely / Max (10th / 50th / 90th percentile), 24 h, 7 AM-7 AM Eastern-ish (12Z-12Z)
  snowP, iceP          chance of measurable snow / ice (%)
  popD, popN           chance of rain, daytime (12Z-00Z) and overnight (00Z-12Z)
  tmax, tmin           high (afternoon) and the low that follows it (next morning), deg F       <- used by the dashboard for days 8-10
  tmaxsd               model spread of the high (tenths of a deg F)  <- feeds the confidence score
  wind, wdir, gust, dpt, rh   at 2 PM Eastern (18Z)                   <- used for days 8-10
  soil                 0-10 cm soil temperature, daily mean, deg F (GFS)

Output (published by GitHub Pages):
  public/latest.json           run times, the 10 dates, field list
  public/t/{lat}_{lon}.json    one 1x1 degree square (lat, lon = floor of the point)
Run by hand:  python nbm_ranges.py public
"""
import concurrent.futures as cf
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

NBM = "https://noaa-nbm-grib2-pds.s3.amazonaws.com"
GFS = "https://noaa-gfs-bdp-pds.s3.amazonaws.com"
OUT = sys.argv[1] if len(sys.argv) > 1 else "public"

STEP = 0.1
LAT0, LAT1, LON0, LON1 = 24.0, 50.0, -125.0, -66.0
PCTS = (10, 50, 90)
NDAYS = 10
MISSING = -999

RANGE_FIELDS = ("rain", "snow", "ice")
DAILY24 = ("rain", "snow", "ice", "snowP", "iceP")
SCALAR_FIELDS = ("snowP", "iceP", "popD", "popN", "tmax", "tmin", "tmaxsd", "wind", "wdir", "gust", "dpt", "rh", "soil")


def log(*a):
    print(*a, flush=True)


def get(url, rng=None, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SDR-Weather-Intelligence/1.0"})
            if rng:
                req.add_header("Range", "bytes=%d-%s" % (rng[0], "" if rng[1] is None else rng[1]))
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except Exception as e:
            if k == tries - 1:
                raise
            time.sleep(3 * (k + 1))


def exists(url):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "SDR-Weather-Intelligence/1.0"})
        with urllib.request.urlopen(req, timeout=30):
            return True
    except Exception:
        return False


def list_keys(base, prefix):
    keys, token = [], None
    ns = "{http://s3.amazonaws.com/doc/2006-03-01/}"
    while True:
        url = f"{base}/?list-type=2&prefix={prefix}" + (f"&continuation-token={urllib.parse.quote(token)}" if token else "")
        root = ET.fromstring(get(url))
        keys += [c.find(ns + "Key").text for c in root.findall(ns + "Contents")]
        if root.findtext(ns + "IsTruncated") == "true":
            token = root.findtext(ns + "NextContinuationToken")
        else:
            return keys


# ------------------------------------------------------------------ find runs
def fhs(keys):
    return sorted(int(re.search(r"\.f(\d{3})\.", k).group(1)) for k in keys)


def find_nbm_run():
    now = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
    for back in range(0, 40):
        t = now - dt.timedelta(hours=back)
        base = f"blend.{t:%Y%m%d}/{t:%H}"
        try:
            q = [k for k in list_keys(NBM, base + "/qmd/") if k.endswith(".co.grib2.idx")]
            c = [k for k in list_keys(NBM, base + "/core/") if k.endswith(".co.grib2.idx")]
        except Exception as e:
            log("list failed", base, e)
            continue
        if not q or not c:
            continue
        log(f"NBM {t:%Y-%m-%d %HZ}: qmd f{fhs(q)[0]:03d}-f{fhs(q)[-1]:03d} ({len(q)}), core f{fhs(c)[0]:03d}-f{fhs(c)[-1]:03d} ({len(c)})")
        if fhs(q)[-1] >= 250 and fhs(c)[-1] >= 250:
            return t, q + c
    raise SystemExit("No complete NBM run (qmd + core to 250 h) in the last 40 hours.")


def find_gfs_run():
    now = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
    t = now.replace(hour=now.hour // 6 * 6)
    for _ in range(6):
        if exists(f"{GFS}/gfs.{t:%Y%m%d}/{t:%H}/atmos/gfs.t{t:%H}z.pgrb2.0p25.f252.idx"):
            log(f"GFS {t:%Y-%m-%d %HZ}")
            return t
        t -= dt.timedelta(hours=6)
    log("GFS: no complete run found; soil temperature skipped")
    return None


# ------------------------------------------------------------------ index parsing
LINE = re.compile(r"^([\d.]+):(\d+):d=(\d{10}):([^:]+):([^:]*):([^:]*):?(.*?):?$")


def read_idx(url):
    rows = []
    for l in get(url).decode("utf-8", "replace").strip().splitlines():
        m = LINE.match(l)
        if m:
            rows.append(dict(off=int(m.group(2)), var=m.group(4), level=m.group(5), fc=m.group(6), extra=m.group(7).strip(": ")))
    for i, r in enumerate(rows):  # end byte = start of the next message at a different offset
        nxt = next((x["off"] for x in rows[i + 1:] if x["off"] > r["off"]), None)
        r["end"] = None if nxt is None else nxt - 1
    return rows


def win(fc, kind):
    m = re.search(r"(\d+)-(\d+) hour " + kind, fc)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"(\d+)-(\d+) day " + kind, fc)
    return (int(m.group(1)) * 24, int(m.group(2)) * 24) if m else None


def inst(fc):
    if fc.strip() == "anl":
        return 0
    m = re.match(r"^(\d+) hour fcst$", fc.strip())
    return int(m.group(1)) if m else None


def classify(r, run):
    """Return (field, pct_index or None, valid_end_datetime) or None."""
    v, lvl, fc, ex = r["var"], r["level"], r["fc"], r["extra"]
    endt = lambda h: run + dt.timedelta(hours=h)
    pm = re.match(r"^(\d+)% level$", ex)
    # 24 h ranges ending 12Z
    if v in ("APCP", "ASNOW", "FICEAC") and "surface" in lvl and pm and int(pm.group(1)) in PCTS:
        w = win(fc, "acc")
        if w and w[1] - w[0] == 24:
            return ({"APCP": "rain", "ASNOW": "snow", "FICEAC": "ice"}[v], PCTS.index(int(pm.group(1))), endt(w[1]))
    # chances of snow / ice in 24 h ending 12Z
    if v == "ASNOW" and ex.startswith("prob >0.00254"):
        w = win(fc, "acc")
        if w and w[1] - w[0] == 24:
            return ("snowP", None, endt(w[1]))
    if v == "FICEAC" and ex.startswith("prob >0.254"):
        w = win(fc, "acc")
        if w and w[1] - w[0] == 24:
            return ("iceP", None, endt(w[1]))
    # 12 h chance of rain: day (ends 00Z) and night (ends 12Z)
    if v == "APCP" and ex.startswith("prob >0.254"):
        w = win(fc, "acc")
        if w and w[1] - w[0] == 12 and endt(w[1]).hour in (0, 12):
            return ("popD" if endt(w[1]).hour == 0 else "popN", None, endt(w[1]))
    # highs / lows
    if v in ("TMAX", "TMIN") and "2 m" in lvl:
        w = win(fc, "max" if v == "TMAX" else "min")
        if w and w[1] - w[0] == 12:
            if v == "TMAX" and endt(w[1]).hour == 0:
                if ex == "":
                    return ("tmax", None, endt(w[1]))
                if "std dev" in ex:
                    return ("tmaxsd", None, endt(w[1]))
            if v == "TMIN" and endt(w[1]).hour == 12 and ex == "":
                return ("tmin", None, endt(w[1]))
    # afternoon snapshot, 18Z
    h = inst(fc)
    if h is not None and ex == "" and endt(h).hour == 18:
        if v in ("WIND", "WDIR", "GUST") and lvl == "10 m above ground":
            return (v.lower(), None, endt(h))
        if v in ("DPT", "RH") and lvl == "2 m above ground":
            return ({"DPT": "dpt", "RH": "rh"}[v], None, endt(h))
    return None


def day_of(field, t):
    """Which calendar date (Eastern day) a message belongs to."""
    if field in ("rain", "snow", "ice", "snowP", "iceP", "popN"):
        return (t - dt.timedelta(hours=24)).date()      # window ends 12Z the next morning
    if field in ("tmax", "tmaxsd", "popD"):
        return (t - dt.timedelta(hours=12)).date()      # 12Z-00Z daytime window
    if field == "tmin":
        return (t - dt.timedelta(hours=24)).date()      # the low that follows day D (next morning), like the NWS
    return t.date()                                      # 18Z snapshot


# ------------------------------------------------------------------ decode + sample
def decode(blob):
    import pygrib
    msg = pygrib.fromstring(blob)
    return np.ma.filled(msg.values.astype("float32"), np.nan), msg


_IDX = {}


def sample_index(msg):
    key = (msg.Ni if hasattr(msg, "Ni") else 0, msg.Nj if hasattr(msg, "Nj") else 0, str(msg.gridType))
    if key in _IDX:
        return _IDX[key]
    from scipy.spatial import cKDTree
    la, lo = msg.latlons()
    lo = np.where(lo > 180, lo - 360, lo)
    lats = np.arange(LAT0, LAT1 + 1e-6, STEP)
    lons = np.arange(LON0, LON1 + 1e-6, STEP)
    LA, LO = np.meshgrid(lats, lons, indexing="ij")
    k = np.cos(np.radians(37.0))
    sel = (la > LAT0 - 1) & (la < LAT1 + 1) & (lo > LON0 - 1) & (lo < LON1 + 1)
    src = np.flatnonzero(sel.ravel())
    tree = cKDTree(np.column_stack([la.ravel()[src], lo.ravel()[src] * k]))
    dist, j = tree.query(np.column_stack([LA.ravel(), LO.ravel() * k]))
    idx = np.where(dist < 0.3, src[j], -1).reshape(LA.shape)
    _IDX[key] = idx
    return idx


def convert(field, vals, msg):
    u = str(getattr(msg, "units", "")).lower()
    if field in ("rain", "ice"):
        return vals / 25.4 * 100                              # kg m-2 (mm) -> hundredths of an inch
    if field == "snow":
        return vals * 39.3701 * 100 if u.startswith("m") and "kg" not in u else vals / 25.4 * 100
    if field in ("tmax", "tmin", "dpt", "soil"):
        return (vals - 273.15) * 9 / 5 + 32
    if field == "tmaxsd":
        return vals * 9 / 5 * 10                              # tenths of a deg F
    if field in ("wind", "gust"):
        return vals * 2.23694
    return vals                                               # %, degrees


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    run, keys = find_nbm_run()
    d0 = run.date() if run.hour <= 12 else (run + dt.timedelta(days=1)).date()
    dates = [d0 + dt.timedelta(days=i) for i in range(NDAYS)]
    log("dates:", dates[0], "->", dates[-1])

    # pick messages from every index file (in parallel)
    jobs = {}
    cands = {}
    found = set()
    with cf.ThreadPoolExecutor(12) as ex:
        idxs = dict(zip(keys, ex.map(lambda k: read_idx(f"{NBM}/{k}"), keys)))
    for key, rows in idxs.items():
        for r in rows:
            found.add(f"{r['var']}:{r['level']}:{r['fc']}:{r['extra']}"[:90])
            c = classify(r, run)
            if not c:
                continue
            field, pi, t = c
            job = (f"{NBM}/{key[:-4]}", r["off"], r["end"])
            if field in DAILY24:
                cands.setdefault((field, pi), {})
                if t not in cands[(field, pi)] or "qmd" in key:
                    cands[(field, pi)][t] = job
                continue
            d = day_of(field, t)
            if d not in dates:
                continue
            slot = (field, dates.index(d), pi)
            if slot not in jobs or "qmd" in key:          # prefer qmd percentiles when both exist
                jobs[slot] = job
    # each day = the 24 h total ending closest to 12Z (7-8 AM Eastern) the next morning
    used = {}
    for (field, pi), byend in cands.items():
        for di, d in enumerate(dates):
            target = dt.datetime.combine(d + dt.timedelta(days=1), dt.time(12), tzinfo=dt.timezone.utc)
            for off in (0, -6, 6, -12, 12):
                t = target + dt.timedelta(hours=off)
                if t in byend:
                    jobs[(field, di, pi)] = byend[t]
                    used.setdefault(field, set()).add(t.strftime("%HZ"))
                    break
    log("24 h windows used (end times):", {k: sorted(v) for k, v in used.items()})
    got = sorted({s[0] for s in jobs})
    log("fields found:", got)
    missing = [f for f in RANGE_FIELDS + SCALAR_FIELDS if f not in got and f != "soil"]
    if missing:
        log("not found (check names):", missing)
        for v in ("ASNOW", "FICEAC", "APCP", "TMAX", "TMIN"):
            for x in sorted(x for x in found if x.startswith(v + ":"))[:6]:
                log("   ", x)
        for f in missing:
            for (field, pi), byend in cands.items():
                if field == f:
                    log(f"    {f} windows end at:", sorted({t.strftime('%a %HZ') for t in byend})[:12])

    # GFS soil temperature (daily mean of 06, 12, 18, 00Z)
    g = find_gfs_run()
    if g:
        for di, d in enumerate(dates):
            for hh in (6, 12, 18, 24):
                vt = dt.datetime.combine(d, dt.time(0), tzinfo=dt.timezone.utc) + dt.timedelta(hours=hh)
                fh = int((vt - g).total_seconds() // 3600)
                if fh < 0 or fh > 384 or (fh > 120 and fh % 3):
                    continue
                url = f"{GFS}/gfs.{g:%Y%m%d}/{g:%H}/atmos/gfs.t{g:%H}z.pgrb2.0p25.f{fh:03d}"
                jobs[("soil", di, hh)] = (url, None, None)    # resolved below

    # resolve GFS byte ranges
    gfs_idx = {}
    for slot, (url, a, b) in list(jobs.items()):
        if slot[0] != "soil":
            continue
        try:
            rows = gfs_idx.get(url) or read_idx(url + ".idx")
            gfs_idx[url] = rows
            r = next(x for x in rows if x["var"] == "TSOIL" and x["level"] == "0-0.1 m below ground")
            jobs[slot] = (url, r["off"], r["end"])
        except Exception as e:
            log("soil skipped", url[-30:], e)
            jobs.pop(slot)

    log(f"downloading {len(jobs)} fields")
    shape = None
    out_r = {f: None for f in RANGE_FIELDS}
    out_s = {f: None for f in SCALAR_FIELDS}
    soil_acc = {}

    def fetch(item):
        slot, (url, a, b) = item
        return slot, get(url, (a, b))

    with cf.ThreadPoolExecutor(8) as ex:
        for slot, blob in ex.map(fetch, sorted(jobs.items(), key=lambda kv: str(kv[0]))):
            field, di, pi = slot
            vals, msg = decode(blob)
            idx = sample_index(msg)
            if shape is None:
                shape = idx.shape
                for f in RANGE_FIELDS:
                    out_r[f] = np.full(shape + (NDAYS, 3), -1, dtype=np.int32)
                for f in SCALAR_FIELDS:
                    out_s[f] = np.full(shape + (NDAYS,), MISSING, dtype=np.int32)
            v = convert(field, vals.ravel(), msg)
            s = np.where(idx >= 0, v[np.clip(idx, 0, None)], np.nan)
            if field in RANGE_FIELDS:
                out_r[field][:, :, di, pi] = np.where(np.isfinite(s), np.round(np.clip(s, 0, None)), -1)
            elif field == "soil":
                acc = soil_acc.setdefault(di, [np.zeros(shape), np.zeros(shape)])
                ok = np.isfinite(s)
                acc[0][ok] += s[ok]; acc[1][ok] += 1
            else:
                if field in ("snowP", "iceP", "popD", "popN", "rh"):
                    s = np.clip(s, 0, 100)
                out_s[field][:, :, di] = np.where(np.isfinite(s), np.round(s), MISSING)
    for di, (sm, n) in soil_acc.items():
        out_s["soil"][:, :, di] = np.where(n > 0, np.round(sm / np.maximum(n, 1)), MISSING)

    for f in RANGE_FIELDS:
        if out_r[f] is not None:
            log(f"  {f:6s} likely max by day:", [round(float(np.max(out_r[f][:, :, d, 1])) / 100, 2) for d in range(NDAYS)])
    for f in ("tmax", "tmin", "popD", "soil"):
        a = out_s[f]
        if a is not None:
            log(f"  {f:6s} Clemson-ish:", [int(a[int((34.68 - LAT0) / STEP), int((-82.84 - LON0) / STEP), d]) for d in range(NDAYS)])

    # ---------------------------------------------------------------- write squares
    os.makedirs(os.path.join(OUT, "t"), exist_ok=True)
    per = int(round(1 / STEP))
    fields_r = [f for f in RANGE_FIELDS if (out_r[f] >= 0).any()]
    fields_s = [f for f in SCALAR_FIELDS if (out_s[f] != MISSING).any()]
    n_files = 0
    for la in range(int(LAT0), int(LAT1)):
        for lo in range(int(LON0), int(LON1)):
            r0, c0 = int(round((la - LAT0) / STEP)), int(round((lo - LON0) / STEP))
            sub = out_r["rain"][r0:r0 + per, c0:c0 + per]
            if (sub < 0).all() and (out_s["tmax"][r0:r0 + per, c0:c0 + per] == MISSING).all():
                continue
            doc = {"lat0": la, "lon0": lo, "step": STEP, "n": per, "dates": [d.isoformat() for d in dates]}
            for f in fields_r:
                s = out_r[f][r0:r0 + per, c0:c0 + per]
                doc[f] = None if f != "rain" and (s <= 0).all() else s.tolist()   # all-zero snow/ice squares stay small
            for f in fields_s:
                doc[f] = out_s[f][r0:r0 + per, c0:c0 + per].tolist()
            with open(os.path.join(OUT, "t", f"{la}_{lo}.json"), "w") as fh:
                json.dump(doc, fh, separators=(",", ":"))
            n_files += 1

    meta = {
        "source": "NOAA National Blend of Models (ranges = 10th/50th/90th percentile); soil temperature NOAA GFS",
        "run": run.strftime("%Y-%m-%dT%H:00Z"), "gfs": g.strftime("%Y-%m-%dT%H:00Z") if g else None,
        "made": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "dates": [d.isoformat() for d in dates], "ranges": fields_r, "fields": fields_s,
        "units": {"rain/snow/ice": "hundredths of an inch [min, likely, max]", "temps": "deg F", "tmaxsd": "tenths deg F",
                  "wind/gust": "mph", "wdir": "deg from", "pops/rh": "%", "missing": MISSING},
        "step": STEP, "tile": "t/{lat}_{lon}.json  (lat, lon = floor of the point; arrays [row S->N][col W->E][day](...))",
    }
    with open(os.path.join(OUT, "latest.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
    with open(os.path.join(OUT, "index.html"), "w") as fh:
        fh.write("<!doctype html><meta charset=utf-8><title>SDR 10-day guidance</title><body style='font-family:system-ui;background:#0A1428;color:#F4F7FB;padding:24px'>"
                 f"<h1>SDR 10-day guidance is running</h1><p>Blend run {meta['run']} &middot; GFS {meta['gfs']} &middot; made {meta['made']} &middot; {n_files} squares</p>"
                 f"<p>Ranges: {', '.join(fields_r)}<br>Fields: {', '.join(fields_s)}</p>"
                 "<p>Test a spot: <a style='color:#6FB7FF' href='t/34_-83.json'>Clemson square</a> &middot; <a style='color:#6FB7FF' href='latest.json'>latest.json</a></p>")
    log(f"done: {n_files} files in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
