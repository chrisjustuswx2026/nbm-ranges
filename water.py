# Detailed lakes and wide rivers for the SDR dashboard maps (zoomed in only).
# Source (free, public): U.S. Census TIGER "AREAWATER" polygons, one file per county, lower 48 + DC.
# Keeps lakes, reservoirs, bays and wide rivers bigger than about 60 acres; drops ponds, treatment ponds and the open ocean.
# Cut into 1-degree squares (water/{lon}_{lat}.json, lon/lat = floor) so a dashboard loads only what's on screen.
# Built once (about 10-20 minutes), then cached by the GitHub job.
import concurrent.futures as cf, io, json, math, os, re, shutil, struct, sys, urllib.request, zipfile

OUT = sys.argv[1] if len(sys.argv) > 1 else "public"
CACHE = "water-cache"
YEARS = (2024, 2023)
MIN_AREA = 250000          # square meters (about 60 acres)
KEEP = {"H2030", "H2040", "H2051", "H3010", "H3013", "H2025"}   # lake/pond, reservoir, bay/estuary, stream/river, braided stream, swamp
SKIP_STATES = {"02", "15", "60", "66", "69", "72", "78"}
TOL = 0.0004               # about 40 m: crisp at county zoom

def get(url, tries=4):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "sdr-water/1.0"})
            with urllib.request.urlopen(req, timeout=180) as r: return r.read()
        except Exception as e:
            if k == tries - 1: raise
    return None

def read_dbf(dbf):
    n, hlen, rlen = struct.unpack("<xxxxIHH", dbf[:12]); fields = []; p = 32
    while dbf[p] != 0x0D:
        fields.append((dbf[p:p + 11].split(b"\0")[0].decode("latin-1"), dbf[p + 16])); p += 32
    rows = []
    for i in range(n):
        r = dbf[hlen + i * rlen: hlen + (i + 1) * rlen]; o = 1; d = {}
        for name, ln in fields: d[name] = r[o:o + ln].decode("latin-1").strip(); o += ln
        rows.append(d)
    return rows

def read_shp(shp, keep):
    out = {}; pos = 100; i = 0
    while pos + 8 <= len(shp):
        _, length = struct.unpack(">2i", shp[pos:pos + 8]); rec = shp[pos + 8: pos + 8 + length * 2]; pos += 8 + length * 2
        if i in keep:
            st = struct.unpack("<i", rec[:4])[0]
            if st in (5, 15, 25):
                nparts, npts = struct.unpack("<2i", rec[36:44]); parts = list(struct.unpack("<%di" % nparts, rec[44:44 + 4 * nparts]))
                pts = struct.unpack("<%dd" % (2 * npts), rec[44 + 4 * nparts: 44 + 4 * nparts + 16 * npts])
                xy = [(pts[2 * j], pts[2 * j + 1]) for j in range(npts)]; parts.append(npts)
                out[i] = [xy[parts[j]:parts[j + 1]] for j in range(nparts)]
        i += 1
    return out

def simplify(pts, tol):
    if len(pts) < 3: return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True; stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop(); (x1, y1), (x2, y2) = pts[a], pts[b]; dx, dy = x2 - x1, y2 - y1; L = math.sqrt(dx * dx + dy * dy); best, bi = 0, -1
        for i in range(a + 1, b):
            x, y = pts[i]; d = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / L if L else math.hypot(x - x1, y - y1)
            if d > best: best, bi = d, i
        if best > tol and bi > 0: keep[bi] = True; stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]

def ring_area(r):
    return abs(sum(r[i][0] * r[i - 1][1] - r[i - 1][0] * r[i][1] for i in range(len(r)))) / 2

def county_files():
    for y in YEARS:
        try:
            html = get("https://www2.census.gov/geo/tiger/TIGER%d/AREAWATER/" % y).decode("latin-1")
            names = sorted(set(re.findall(r'tl_%d_(\d{5})_areawater\.zip' % y, html)))
            names = [f for f in names if f[:2] not in SKIP_STATES]
            if names:
                print("water: %d county files from %d" % (len(names), y), flush=True)
                return y, names
        except Exception as e:
            print("water: listing failed", y, e, flush=True)
    return None, []

def one(y, fips):
    try:
        z = zipfile.ZipFile(io.BytesIO(get("https://www2.census.gov/geo/tiger/TIGER%d/AREAWATER/tl_%d_%s_areawater.zip" % (y, y, fips))))
        nm = z.namelist(); dbf = read_dbf(z.read([x for x in nm if x.lower().endswith(".dbf")][0]))
        keep = {i for i, d in enumerate(dbf) if d.get("MTFCC") in KEEP and float(d.get("AWATER") or 0) >= MIN_AREA}
        if not keep: return []
        shp = read_shp(z.read([x for x in nm if x.lower().endswith(".shp")][0]), keep); out = []
        for i, parts in shp.items():
            rings = []
            for p in parts:
                s = simplify(p, TOL)
                if len(s) >= 4 and ring_area(s) > 2e-7: rings.append([[round(x, 4), round(yy, 4)] for x, yy in s])
            if rings: out.append(rings)
        return out
    except Exception as e:
        print("water: skipped", fips, e, flush=True); return []

def build():
    y, files = county_files()
    if not files: return None
    cells = {}; n = 0; done = 0
    with cf.ThreadPoolExecutor(16) as ex:
        for polys in ex.map(lambda f: one(y, f), files):
            done += 1
            if done % 250 == 0: print("water: %d / %d counties" % (done, len(files)), flush=True)
            for rings in polys:
                n += 1; xs = [p[0] for p in rings[0]]; ys = [p[1] for p in rings[0]]
                for cx in range(int(math.floor(min(xs))), int(math.floor(max(xs))) + 1):
                    for cy in range(int(math.floor(min(ys))), int(math.floor(max(ys))) + 1):
                        cells.setdefault((cx, cy), []).append([n, rings])
    print("water: %d polygons, %d squares" % (n, len(cells)), flush=True)
    return cells

def main():
    os.makedirs(OUT, exist_ok=True); c = os.path.join(CACHE, "water")
    if not os.path.exists(os.path.join(c, "index.json")):
        cells = build()
        if not cells: print("water: nothing built"); return
        os.makedirs(c, exist_ok=True)
        for (cx, cy), polys in cells.items():
            json.dump({"lakes": polys}, open(os.path.join(c, "%d_%d.json" % (cx, cy)), "w"), separators=(",", ":"))
        json.dump(sorted("%d_%d" % k for k in cells), open(os.path.join(c, "index.json"), "w"))
    shutil.copytree(c, os.path.join(OUT, "water"), dirs_exist_ok=True); print("water copied to", OUT)

if __name__ == "__main__":
    try: main()
    except BaseException as e: print("water skipped:", e)   # never block the forecast publish
