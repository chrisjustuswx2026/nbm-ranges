"""SDR Weather Intelligence — river gauges for the dashboards (runs in the NBM ranges job).

Writes <out>/rivers.json:
  every river gauge in the lower 48 with its current and forecast flood category, and — for gauges near a client
  site or in flood anywhere — flood stages plus the observed (last 3 days) and forecast river level, for the graph.

Source: the national water prediction service API (api.water.noaa.gov/nwps/v1). No key needed.
Usage:  python rivers.py public
"""
import concurrent.futures as cf
import datetime as dt
import json
import math
import os
import sys
import urllib.request

OUT = sys.argv[1] if len(sys.argv) > 1 else "public"
API = "https://api.water.noaa.gov/nwps/v1"
BBOX = (-125.0, 24.0, -66.0, 50.0)           # the lower 48
SITES = [("clemson", 34.6787, -82.8432), ("greenville", 34.85, -82.39), ("bay", 30.17, -85.66)]
NEAR_MI = 60                                   # hydrographs for gauges this close to a client site
MAX_DETAIL = 150                               # cap on per-gauge detail calls (the dashboard fetches any other gauge live when tapped)
CAT = {"no_flooding": 0, "action": 1, "minor": 2, "moderate": 3, "major": 4}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "SDR-Weather-Intelligence rivers (github actions)", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def miles(la1, lo1, la2, lo2):
    p = math.pi / 180
    a = math.sin((la2 - la1) * p / 2) ** 2 + math.cos(la1 * p) * math.cos(la2 * p) * math.sin((lo2 - lo1) * p / 2) ** 2
    return 3958.8 * 2 * math.asin(math.sqrt(a))


def num(v):
    try:
        v = float(v)
        return None if v <= -900 else round(v, 2)
    except (TypeError, ValueError):
        return None


def cat(s):
    return CAT.get(str(s or "").lower(), -1)


def status_of(g):
    st = g.get("status") or {}
    o, f = st.get("observed") or {}, st.get("forecast") or {}
    return ({"v": num(o.get("primary")), "u": o.get("primaryUnit"), "t": o.get("validTime"), "c": cat(o.get("floodCategory"))},
            {"v": num(f.get("primary")), "u": f.get("primaryUnit"), "t": f.get("validTime"), "c": cat(f.get("floodCategory"))})


def series(block, since=None, step_min=60):
    out, last = [], None
    for d in (block or {}).get("data") or []:
        t, v = d.get("validTime"), num(d.get("primary"))
        if not t or v is None:
            continue
        try:
            tt = dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
        except ValueError:
            continue
        if since and tt < since:
            continue
        if last and (tt - last).total_seconds() < step_min * 60:
            continue
        last = tt
        out.append([int(tt.timestamp()), v])
    return out


def detail(lid):
    g = get(f"{API}/gauges/{lid}")
    sf = get(f"{API}/gauges/{lid}/stageflow")
    fl = (g.get("flood") or {})
    cats = fl.get("categories") or {}
    stages = {k: num((cats.get(k) or {}).get("stage")) for k in ("action", "minor", "moderate", "major")}
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=3)
    obs = series(sf.get("observed"), since, 60)
    fc = series(sf.get("forecast"), None, 180)
    crest = max(fc, key=lambda p: p[1]) if fc else None
    impacts = []
    for im in (fl.get("impacts") or [])[:12]:
        s, txt = num(im.get("stage")), str(im.get("statement") or "").strip()
        if s is not None and txt:
            impacts.append([s, txt[:400]])
    return {"cats": stages, "units": fl.get("stageUnits") or "ft", "obs": obs, "fc": fc,
            "crest": crest, "impacts": impacts}


def main():
    os.makedirs(OUT, exist_ok=True)
    x0, y0, x1, y1 = BBOX
    lst = get(f"{API}/gauges?bbox.xmin={x0}&bbox.ymin={y0}&bbox.xmax={x1}&bbox.ymax={y1}&srid=EPSG_4326")
    raw = lst.get("gauges") if isinstance(lst, dict) else lst
    gauges = []
    for g in raw or []:
        la, lo = num(g.get("latitude")), num(g.get("longitude"))
        if la is None or lo is None:
            continue
        o, f = status_of(g)
        near = min(miles(la, lo, s[1], s[2]) for s in SITES)
        gauges.append({"id": g.get("lid"), "n": g.get("name"), "la": la, "lo": lo, "o": o, "f": f, "near": round(near, 1)})

    # detail (flood stages + river line) for gauges near a site, and every gauge in flood anywhere (for the 24/7 channel)
    want = [g for g in gauges if g["near"] <= NEAR_MI or max(g["o"]["c"], g["f"]["c"]) >= 2]
    want.sort(key=lambda g: (-max(g["o"]["c"], g["f"]["c"]), g["near"]))
    want = want[:MAX_DETAIL]
    by_id = {g["id"]: g for g in gauges}

    def work(g):
        try:
            return g["id"], detail(g["id"])
        except Exception as e:  # one gauge failing never stops the rest
            return g["id"], {"err": str(e)[:120]}

    with cf.ThreadPoolExecutor(6) as ex:
        for lid, d in ex.map(work, want):
            if "err" not in d:
                by_id[lid]["d"] = d

    out = {"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "count": len(gauges),
           "detail": sum(1 for g in gauges if "d" in g), "gauges": gauges}
    with open(os.path.join(OUT, "rivers.json"), "w") as fh:
        json.dump(out, fh, separators=(",", ":"))
    print(f"rivers: {len(gauges)} gauges, {out['detail']} with river lines, "
          f"{sum(1 for g in gauges if max(g['o']['c'], g['f']['c']) >= 2)} in or forecast in flood")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # never fail the whole job over rivers; leave a small file that says what went wrong (readable at /rivers.json)
        print("rivers: skipped —", e)
        try:
            os.makedirs(OUT, exist_ok=True)
            with open(os.path.join(OUT, "rivers.json"), "w") as fh:
                json.dump({"generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"), "count": 0,
                           "gauges": [], "error": str(e)[:300]}, fh)
        except Exception:
            pass
