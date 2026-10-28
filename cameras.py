# DOT traffic cameras for the SDR dashboard maps (dots at zoom 9+, picture loads when tapped; live video where the state streams it, "vid").
# Built once a day from each state's public feed, cut into 1-degree squares: cameras/{lon}_{lat}.json + cameras/index.json.
# The page never sees any key; only each camera's public picture address.
#
# States and how they're reached:
#   KY  Kentucky Transportation Cabinet ArcGIS layer, no key.
#   NC, GA, LA  TravelIQ "511" sites (DriveNC, 511GA, 511LA): free developer key per site (register at <site>/my511/register,
#       then request a key on <site>/developers/doc). Put them in the repo's Settings > Secrets as
#       DRIVENC_KEY, GA511_KEY, LA511_KEY. A state with no key is skipped, never an error.
#   SC  SCDOT's 511 map data (sc.cdn.iteris-atis.com), open GeoJSON, no key.
#   FL  FL511 (TravelIQ, same as NC/GA): FL511_KEY. FL511's terms say personal use only unless FDOT gives written consent;
#       the key stays unset until Chris has that consent in writing.
#   TN  TDOT SmartWay camera list (www.tdot.tn.gov/opendata/api/public/RoadwayCameras) with the ApiKey the SmartWay
#       website itself uses (TDOT_KEY in Secrets; undocumented, no written reuse terms yet). Pictures are TDOT's public
#       snapshots on tnsnapshots.com. With no key, falls back to a cached copy of the list (Aug 2026) so TN still shows.
#   Not included yet: AL/MS (video streams only), VA (no documented feed).
import json, math, os, shutil, sys, time, urllib.request

OUT = sys.argv[1] if len(sys.argv) > 1 else "public"
CACHE = "cameras-cache"
TODAY = time.strftime("%Y-%m-%d", time.gmtime())

def get(url, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SDR-Weather-Intelligence/1.0", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            if k == tries - 1: raise
            time.sleep(3)

def kentucky():
    out = []
    url = ("https://kygisserver.ky.gov/arcgis/rest/services/WGS84WM_Services/Ky_WebCams_WGS84WM/MapServer/0/query"
           "?where=1%3D1&outFields=id,name,status,county,highway,milemarker,description,direction,latitude,longitude,snapshot&outSR=4326&f=geojson")
    j = get(url)
    for f in j.get("features", []):
        p = f.get("properties") or {}; g = f.get("geometry") or {}
        la = p.get("latitude"); lo = p.get("longitude")
        if (la is None or lo is None) and g.get("coordinates"): lo, la = g["coordinates"][:2]
        img = p.get("snapshot")
        if not img or la is None: continue
        name = p.get("name") or p.get("description") or "Camera"
        road = " ".join(x for x in [p.get("highway"), ("MM " + str(p["milemarker"])) if p.get("milemarker") else "", p.get("direction")] if x)
        out.append({"id": "KY-%s" % p.get("id"), "la": round(float(la), 5), "lo": round(float(lo), 5), "name": name, "road": road or (p.get("county") or ""),
                    "st": "KY", "img": img, "refresh": 120, "src": "kytc", "attr": "Camera: Kentucky Transportation Cabinet"})
    return out

def traveliq(st, host, key, attr):
    out = []
    if not key: print("cameras: no key for", st, "(skipped)"); return out
    j = get("https://%s/api/v2/get/cameras?key=%s&format=json" % (host, key))
    for c in (j if isinstance(j, list) else j.get("Cameras", j.get("cameras", []))):
        views = [v for v in (c.get("Views") or []) if v.get("Url")]
        if not views or c.get("Latitude") is None: continue
        v = views[0]
        name = c.get("Location") or c.get("Name") or "Camera"
        road = " ".join(x for x in [c.get("Roadway"), c.get("Direction")] if x)
        out.append({"id": "%s-%s" % (st, c.get("Id")), "la": round(float(c["Latitude"]), 5), "lo": round(float(c["Longitude"]), 5), "name": name, "road": road,
                    "st": st, "img": v["Url"], "refresh": 60, "src": host.split(".")[0], "attr": attr, "vid": v.get("VideoUrl") or None})
    return out

def south_carolina():
    out = []
    j = get("https://sc.cdn.iteris-atis.com/geojson/icons/metadata/icons.cameras.geojson")
    for f in j.get("features", []):
        p = f.get("properties") or {}; g = f.get("geometry") or {}
        co = g.get("coordinates") or []
        if len(co) < 2: continue
        lo, la = co[:2]
        img = p.get("image_url") or p.get("https_url") or p.get("snapshot")
        if not img or p.get("active") is False: continue
        name = p.get("description") or p.get("name") or "Camera"
        road = " ".join(x for x in [p.get("route"), p.get("direction")] if x)
        out.append({"id": "SC-%s" % (p.get("id") or p.get("guid")), "la": round(float(la), 5), "lo": round(float(lo), 5), "name": name, "road": road,
                    "st": "SC", "img": img, "refresh": 120, "src": "sc511", "attr": "Camera: SCDOT 511",
                    "vid": (p.get("https_url") if str(p.get("https_url") or "").endswith(".m3u8") else None)})
    return out

def tennessee():
    out = []; key = os.environ.get("TDOT_KEY")
    if key:
        req = urllib.request.Request("https://www.tdot.tn.gov/opendata/api/public/RoadwayCameras",
                                     headers={"User-Agent": "SDR-Weather-Intelligence/1.0", "Accept": "application/json", "ApiKey": key})
        with urllib.request.urlopen(req, timeout=60) as r: j = json.loads(r.read().decode("utf-8", "replace"))
        src = "tdot"
    else:
        print("cameras: no TDOT_KEY, using cached Tennessee list")
        j = get("https://rawcdn.githack.com/stephenyeargin/trmnl-tdot-smartway/refs/heads/main/assets/cameras.json"); src = "tdot-cached"
    for c in (j if isinstance(j, list) else j.get("data", [])):
        img = c.get("thumbnailUrl"); la = c.get("lat"); lo = c.get("lng")
        if not img or la is None or lo is None or str(c.get("active", "true")).lower() == "false": continue
        road = " ".join(x for x in [c.get("route"), ("MM " + str(c["mileMarker"])) if c.get("mileMarker") else "", c.get("direction")] if x)
        out.append({"id": "TN-%s" % c.get("id"), "la": round(float(la), 5), "lo": round(float(lo), 5), "name": c.get("title") or "Camera", "road": road or (c.get("jurisdiction") or ""),
                    "st": "TN", "img": img, "refresh": 120, "src": src, "attr": "Camera: TDOT SmartWay", "vid": c.get("httpsVideoUrl") or None})
    return out

def build():
    cams = []; status = {}
    for st, fn in [("KY", kentucky),
                   ("NC", lambda: traveliq("NC", "drivenc.gov", os.environ.get("DRIVENC_KEY"), "Camera: NCDOT DriveNC")),
                   ("SC", south_carolina),
                   ("GA", lambda: traveliq("GA", "511ga.org", os.environ.get("GA511_KEY"), "Camera: Georgia DOT 511GA")),
                   ("TN", tennessee),
                   ("FL", lambda: traveliq("FL", "fl511.com", os.environ.get("FL511_KEY"), "Camera: Florida DOT FL511")),
                   ("LA", lambda: traveliq("LA", "511la.org", os.environ.get("LA511_KEY"), "Camera: Louisiana DOTD 511LA"))]:
        try:
            got = fn(); cams += got; status[st] = "ok %d" % len(got); print("cameras:", st, len(got), flush=True)
        except Exception as e:
            status[st] = "failed: %s" % e; print("cameras:", st, "failed", e, flush=True)
    cells = {}
    for c in cams:
        if "vid" in c and not c["vid"]: del c["vid"]
        k = (int(math.floor(c["lo"])), int(math.floor(c["la"])))
        cells.setdefault(k, []).append(c)
    return cams, cells, status

def main():
    os.makedirs(OUT, exist_ok=True); c = os.path.join(CACHE, "cameras")
    stamp = os.path.join(c, "built.txt")
    fresh = os.path.exists(stamp) and open(stamp).read().strip() == TODAY
    if not fresh:
        cams, cells, status = build()
        if cams:
            if os.path.exists(c): shutil.rmtree(c)
            os.makedirs(c, exist_ok=True)
            for (cx, cy), lst in cells.items():
                json.dump({"cams": lst}, open(os.path.join(c, "%d_%d.json" % (cx, cy)), "w"), separators=(",", ":"))
            json.dump(sorted("%d_%d" % k for k in cells), open(os.path.join(c, "index.json"), "w"))
            json.dump({"generatedAt": TODAY, "count": len(cams), "states": status}, open(os.path.join(c, "status.json"), "w"))
            open(stamp, "w").write(TODAY)
            print("cameras: %d cameras in %d squares" % (len(cams), len(cells)), flush=True)
        elif not os.path.exists(os.path.join(c, "index.json")):
            print("cameras: nothing built"); return
    shutil.copytree(c, os.path.join(OUT, "cameras"), dirs_exist_ok=True); print("cameras copied to", OUT)

if __name__ == "__main__":
    try: main()
    except BaseException as e: print("cameras skipped:", e)   # never block the forecast publish
