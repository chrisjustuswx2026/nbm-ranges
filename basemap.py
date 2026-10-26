# Zoomed-in map detail for the SDR dashboards: highways (interstates + U.S. routes), route shields, lakes and rivers.
# Sources (free, public): U.S. Census TIGER primary roads; Natural Earth 10m lakes + rivers (with North America supplements).
# Whole lower 48, cut into 5-degree squares (basemap/{cx}_{cy}.json) so a dashboard loads only what's on screen. Zoomed-in only.
import io, json, math, os, shutil, struct, sys, urllib.request, zipfile

OUT = sys.argv[1] if len(sys.argv) > 1 else "public"
CACHE = "basemap-cache"
BBOX = (-125.5, 24.0, -66.5, 49.8)   # lower 48
ROADS = ["https://www2.census.gov/geo/tiger/TIGER{y}/PRIMARYROADS/tl_{y}_us_primaryroads.zip".format(y=y) for y in (2024, 2023, 2022)]
NE = "https://naciscdn.org/naturalearth/10m/physical/{}.zip"
LAKES = ["ne_10m_lakes", "ne_10m_lakes_north_america"]
RIVERS = ["ne_10m_rivers_lake_centerlines", "ne_10m_rivers_north_america"]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "sdr-basemap/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r: return r.read()

def read_shp(shp):
    out = []; pos = 100
    while pos + 8 <= len(shp):
        _, length = struct.unpack(">2i", shp[pos:pos + 8]); rec = shp[pos + 8: pos + 8 + length * 2]; pos += 8 + length * 2
        st = struct.unpack("<i", rec[:4])[0]
        if st not in (3, 5, 13, 15, 23, 25): out.append(None); continue
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

def shapes(zbytes):
    z = zipfile.ZipFile(io.BytesIO(zbytes)); nm = z.namelist()
    return list(zip(read_shp(z.read([x for x in nm if x.lower().endswith(".shp")][0])), read_dbf(z.read([x for x in nm if x.lower().endswith(".dbf")][0]))))

def in_bbox(parts):
    return any(BBOX[0] <= x <= BBOX[2] and BBOX[1] <= y <= BBOX[3] for p in parts for x, y in p)

R4 = lambda p: [[round(x, 4), round(y, 4)] for x, y in p]


CELL = 5.0
def cell_of(x, y): return (int(math.floor(x / CELL)), int(math.floor(y / CELL)))
def cells_of(pts): return {cell_of(x, y) for x, y in pts}
def write_grid(folder, cells):
    os.makedirs(folder, exist_ok=True)
    for (cx, cy), obj in cells.items():
        json.dump(obj, open(os.path.join(folder, "%d_%d.json" % (cx, cy)), "w"), separators=(",", ":"))
    json.dump(sorted("%d_%d" % k for k in cells), open(os.path.join(folder, "index.json"), "w"))

def build():
    out = {"roads": [], "shields": [], "lakes": [], "rivers": []}
    data = None
    for u in ROADS:
        try: data = get(u); print("roads from", u); break
        except Exception as e: print("roads failed", u, e)
    if data:
        by = {}
        for parts, d in shapes(data):
            if not parts or not in_bbox(parts): continue
            t = d.get("RTTYP", ""); name = d.get("FULLNAME", "")
            if t not in ("I", "U"): continue
            ref = "".join(ch for ch in name.split()[-1] if ch.isdigit()) if name else ""
            if ref: by.setdefault((t, ref), []).extend(parts)
        for (t, ref), parts in by.items():
            lines = [R4(simplify(p, 0.004 if t == "I" else 0.008)) for p in parts if len(p) > 1]
            lines = [l for l in lines if len(l) > 1]
            if not lines: continue
            out["roads"].append([t, ref, lines]); acc = 0.0; last = None; first = True
            for l in lines:
                for x, y in l:
                    if last: acc += math.hypot(x - last[0], y - last[1])
                    last = (x, y)
                    if acc >= 0.6 or first:
                        out["shields"].append([("I-" if t == "I" else "US-") + ref, x, y]); acc = 0.0; first = False
        print("roads", len(out["roads"]), "shields", len(out["shields"]))
    for key, lst, tol in (("lakes", LAKES, 0.003), ("rivers", RIVERS, 0.004)):
        for name in lst:
            try: sh = shapes(get(NE.format(name)))
            except Exception as e: print(name, "failed", e); continue
            for parts, d in sh:
                if not parts or not in_bbox(parts): continue
                nm = d.get("name") or d.get("NAME") or ""
                if key == "lakes": out["lakes"].append(["L", nm, [[R4(simplify(p, tol))] for p in parts if len(p) > 3]])
                else: out["rivers"].append(["R", nm, [R4(simplify(p, tol)) for p in parts if len(p) > 1]])
            print(name, "ok")
    # cut into 5-degree squares (a feature goes in every square it touches; shields only in their own square)
    cells = {}; n = 0
    E = lambda k: cells.setdefault(k, {"roads": [], "shields": [], "lakes": [], "rivers": []})
    for t, ref, lines in out["roads"]:
        for l in lines:
            n += 1
            for k in cells_of(l): E(k)["roads"].append([n, t, ref, l])
    for lab, x, y in out["shields"]: E(cell_of(x, y))["shields"].append([lab, x, y])
    for _, nm, polys in out["lakes"]:
        for poly in polys:
            n += 1
            for k in cells_of(poly[0]): E(k)["lakes"].append([n, poly])
    for _, nm, lines in out["rivers"]:
        for l in lines:
            n += 1
            for k in cells_of(l): E(k)["rivers"].append([n, l])
    print("cells", len(cells)); return cells

def main():
    os.makedirs(OUT, exist_ok=True); c = os.path.join(CACHE, "basemap")
    if not os.path.exists(os.path.join(c, "index.json")):
        b = build()
        if not b: print("basemap: nothing built"); return
        write_grid(c, b)
    shutil.copytree(c, os.path.join(OUT, "basemap"), dirs_exist_ok=True); print("basemap copied to", OUT)

if __name__ == "__main__":
    try: main()
    except BaseException as e: print("basemap skipped:", e)   # never block the forecast publish
