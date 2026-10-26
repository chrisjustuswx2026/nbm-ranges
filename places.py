# National place list for the dashboard search box (every U.S. city, town and named community, plus every ZIP code).
# Source: U.S. Census Bureau (free, public). Built once, cached by the GitHub job, copied into each publish.
#   places.json : [[name, ST, population, lat, lon], ...] biggest first
#   zips.json   : {"29631": [lat, lon, "Clemson", "SC"], ...}  (each ZIP points at its nearest named place)
# Usage: python places.py public          (reads/writes cache in ./places-cache)
import io, json, math, os, re, sys, urllib.request, zipfile

OUT = sys.argv[1] if len(sys.argv) > 1 else "public"
CACHE = "places-cache"
GAZ = "https://www2.census.gov/geo/docs/maps-data/data/gazetteer/{y}_Gazetteer/{y}_Gaz_{kind}_national.zip"
POP = "https://api.census.gov/data/2020/dec/pl?get=P1_001N&for=place:*&in=state:*"
STATES = {"AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO",
          "MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","PR"}
SUFFIX = re.compile(r"\s+(city and borough|consolidated government|metropolitan government|unified government|metro government|urban county|"
                    r"city|town|village|borough|municipality|CDP|comunidad|zona urbana|plantation|township|corporation)(\s*\(balance\))?$", re.I)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "sdr-places/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r: return r.read()

def gazetteer(kind):
    for y in (2024, 2023, 2022, 2021, 2020):
        try:
            z = zipfile.ZipFile(io.BytesIO(get(GAZ.format(y=y, kind=kind))))
            txt = z.read(z.namelist()[0]).decode("latin-1")
            rows = [l.split("\t") for l in txt.splitlines() if l.strip()]
            head = [h.strip() for h in rows[0]]
            print(f"gazetteer {kind} {y}: {len(rows)-1} rows")
            return [dict(zip(head, [c.strip() for c in r])) for r in rows[1:]]
        except Exception as e:
            print(f"gazetteer {kind} {y} failed: {e}")
    raise SystemExit("no gazetteer")

def clean(name):
    n = re.sub(r"\s*\(balance\)$", "", name).strip()
    n = SUFFIX.sub("", n).strip()
    n = re.sub(r"[-/](Davidson|Jefferson County|Fayette|Clarke County|Richmond County|Muscogee County)$", "", n)  # Nashville-Davidson -> Nashville
    return n

def build():
    pop = {}
    try:
        data = json.loads(get(POP))
        for p, st, pl in data[1:]: pop[st + pl] = int(p)
        print("population rows", len(pop))
    except Exception as e:
        print("population lookup failed (list still builds, sorted by land area):", e)
    places, seen = [], {}
    for r in gazetteer("place"):
        st = r.get("USPS", "")
        if st not in STATES: continue
        try: la, lo = float(r["INTPTLAT"]), float(r["INTPTLONG"])
        except Exception: continue
        n = clean(r["NAME"])
        p = pop.get(r["GEOID"], 0) or int(float(r.get("ALAND_SQMI") or 0) * 10)
        k = (n.lower(), st)
        if k in seen and seen[k][2] >= p: continue          # same name twice in a state (city + CDP): keep the bigger
        row = [n, st, p, round(la, 3), round(lo, 3)]
        if k in seen: places[places.index(seen[k])] = row
        else: places.append(row)
        seen[k] = row
    places.sort(key=lambda x: -x[2])
    print("places", len(places))
    # ZIP -> nearest named place (grid lookup so it runs in seconds)
    grid = {}
    for p in places: grid.setdefault((int(p[3]), int(p[4])), []).append(p)
    zips = {}
    for r in gazetteer("zcta"):
        z = r.get("GEOID", "")[:5]
        try: la, lo = float(r["INTPTLAT"]), float(r["INTPTLONG"])
        except Exception: continue
        best, bd = None, 1e9
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                for p in grid.get((int(la) + dy, int(lo) + dx), []):
                    d = (p[3] - la) ** 2 + ((p[4] - lo) * math.cos(math.radians(la))) ** 2
                    if p[2] < 500: d *= 1.6                   # lean toward real towns over tiny spots
                    if d < bd: best, bd = p, d
        if best: zips[z] = [round(la, 3), round(lo, 3), best[0], best[1]]
    print("zips", len(zips))
    return places, zips

def main():
    os.makedirs(OUT, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
    pc, zc = os.path.join(CACHE, "places.json"), os.path.join(CACHE, "zips.json")
    if not (os.path.exists(pc) and os.path.exists(zc)):
        places, zips = build()
        json.dump(places, open(pc, "w"), separators=(",", ":"))
        json.dump(zips, open(zc, "w"), separators=(",", ":"))
    for f in ("places.json", "zips.json"):
        open(os.path.join(OUT, f), "w").write(open(os.path.join(CACHE, f)).read())
    print("place list copied to", OUT)

if __name__ == "__main__":
    try: main()
    except BaseException as e: print("place list skipped:", e)   # never block the forecast publish
