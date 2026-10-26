# Crisp county lines for the SDR dashboard maps: U.S. Census detailed county outlines (cartographic boundary, 1:500,000),
# for the whole U.S., cut into 5-degree squares so a dashboard only loads what's on screen. Built once, cached by the GitHub job.
#   counties/{cx}_{cy}.json = {"lines": [[id, [[lon,lat],...]], ...]}   + counties/index.json (no outside libraries needed)
import io, json, math, os, shutil, struct, sys, urllib.request, zipfile

OUT = sys.argv[1] if len(sys.argv) > 1 else "public"
CACHE = "counties-cache"
SRC = ["https://www2.census.gov/geo/tiger/GENZ{y}/shp/cb_{y}_us_county_500k.zip".format(y=y) for y in (2024, 2023, 2022)]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "sdr-counties/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r: return r.read()

def read_shp(shp):
    out = []; pos = 100
    while pos + 8 <= len(shp):
        _, length = struct.unpack(">2i", shp[pos:pos + 8]); rec = shp[pos + 8: pos + 8 + length * 2]; pos += 8 + length * 2
        st = struct.unpack("<i", rec[:4])[0]
        if st not in (5, 15, 25): out.append(None); continue
        nparts, npts = struct.unpack("<2i", rec[36:44]); parts = list(struct.unpack("<%di" % nparts, rec[44:44 + 4 * nparts]))
        pts = struct.unpack("<%dd" % (2 * npts), rec[44 + 4 * nparts: 44 + 4 * nparts + 16 * npts])
        xy = [(pts[2 * i], pts[2 * i + 1]) for i in range(npts)]; parts.append(npts)
        out.append([xy[parts[i]:parts[i + 1]] for i in range(nparts)])
    return out

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

def simplify(pts, tol):
    if len(pts) < 3: return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True; stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop(); (x1, y1), (x2, y2) = pts[a], pts[b]; dx, dy = x2 - x1, y2 - y1; L = dx * dx + dy * dy; best, bi = 0, -1
        for i in range(a + 1, b):
            x, y = pts[i]; d = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / math.sqrt(L) if L else math.hypot(x - x1, y - y1)
            if d > best: best, bi = d, i
        if best > tol and bi > 0: keep[bi] = True; stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]


CELL = 5.0
def cell_of(x, y): return (int(math.floor(x / CELL)), int(math.floor(y / CELL)))
def cells_of(pts): return {cell_of(x, y) for x, y in pts}
def write_grid(folder, cells):
    os.makedirs(folder, exist_ok=True)
    for (cx, cy), obj in cells.items():
        json.dump(obj, open(os.path.join(folder, "%d_%d.json" % (cx, cy)), "w"), separators=(",", ":"))
    json.dump(sorted("%d_%d" % k for k in cells), open(os.path.join(folder, "index.json"), "w"))

def build():
    data = None
    for u in SRC:
        try: data = get(u); print("counties from", u); break
        except Exception as e: print("failed", u, e)
    if not data: return None
    z = zipfile.ZipFile(io.BytesIO(data)); nm = z.namelist()
    shp = read_shp(z.read([x for x in nm if x.lower().endswith(".shp")][0])); dbf = read_dbf(z.read([x for x in nm if x.lower().endswith(".dbf")][0]))
    cells = {}; n = 0
    for parts, d in zip(shp, dbf):
        if not parts or d.get("STATEFP") in ("02", "15", "60", "66", "69", "72", "78"): continue   # lower 48 + DC
        for p in parts:
            s = simplify(p, 0.0015)                       # ~150 m: crisp at county zoom, small files
            if len(s) < 3: continue
            n += 1; line = [n, [[round(x, 4), round(y, 4)] for x, y in s]]
            for k in cells_of(s): cells.setdefault(k, {"lines": []})["lines"].append(line)
    print("county outlines", n, "cells", len(cells)); return cells

def main():
    os.makedirs(OUT, exist_ok=True); c = os.path.join(CACHE, "counties")
    if not os.path.exists(os.path.join(c, "index.json")):
        b = build()
        if not b: print("counties: nothing built"); return
        write_grid(c, b)
    shutil.copytree(c, os.path.join(OUT, "counties"), dirs_exist_ok=True); print("counties copied to", OUT)

if __name__ == "__main__":
    try: main()
    except BaseException as e: print("counties skipped:", e)   # never block the forecast publish
