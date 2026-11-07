# SDR 24/7 Channel: Handoff from the Dashboard (v218, Nov 4, 2026)

Everything we built and fixed in the client dashboards over the last few days, written up so the 24/7 channel matches it. Source code for every piece is in `/source` (the dashboard is built by Python "patch blocks" that add CSS/JS to the page; search a block for the function names given below). The finished, working page is `/source/built/greenville-index.html`, which is the best reference: every function below runs there.

**Rule of thumb: the channel and the dashboard must never disagree.** Same status, same headline, same numbers, same words. Where possible, the channel should load the same logic rather than re-write it.

---

## 1. House language rules (apply to every word on screen)
- No agency names on screen: no NWS, SPC, WPC, CPC, NOAA or NHC. Say "the forecast", "the outlook", "official warnings".
- Never say "mesoscale discussion". Say "storms organizing" or "what we're watching".
- Say "model agreement X of 5", never "confidence".
- Round percentages to the nearest 10. Say "noon" and "midnight", never 12 PM or 12 AM.
- Odds ladder: leaning toward → good chance → expect → plan on.
- "Damaging" gusts only at 58 mph or higher. Below that: "strong gusts to 45 mph".
- No slogans ("when thunder roars", "turn around don't drown"). Say the action plainly.
- Never assume a client has a job or event they didn't tell us about.
- No FEMA. Never offer help with power. Closing line: "SDR stands ready to serve."
- Never put a person's name on an automated message. No CJWX or Chris on SDR before 2028.

## 2. Status rules: ALL CLEAR / HEADS UP / TAKE ACTION
- **TAKE ACTION**: only an official warning at the site, or lightning at the site. Never invented.
- **HEADS UP**: a meaningful threat ahead, such as a severe outlook level 1+ for the day (level 1 wording: "isolated severe storms possible; not everyone gets one"), a watch nearby, storms organizing within 25 miles, a flooding-rain risk, freeze, heat, wind or winter weather.
- **ALL CLEAR**: nothing in the way.
- Watches within 25 miles count. If the site is just outside, say "just outside".
- Code: status card in the built page (`#call`, `#status`); notification rules in `notify(...)`.

## 3. Visual fixes to copy
- **What's Next card**: not brown, and not a yellow box inside the green card. It's its own navy card with a 6 px colored left edge (green/yellow/red by level), a colored headline, an icon on the right and up to 3 bullets (upcoming alerts, storms, rain, snow, freeze, gusts). Code: `block_design.py` → `#next.nxcard`, `bullets()`.
- **Hero**: status on the left (ALL CLEAR) with conditions beside it (temperature, wind, gusts).
- **Line icons**, not emoji. Warnings button is a triangle line icon, not a bell emoji.
- **Radar ("naked radar")**: shows only the weather (rain, warning boxes, lightning, the 30-mile ring) and the logo, a little smaller. Tools appear only when opened. On TV, keep it naked and leave the tools off entirely.
- **Warning card (branded)**: colored header, hail, wind, damage tags (CONSIDERABLE / DESTRUCTIVE / PDS / CONFIRMED / RADAR INDICATED), time left, motion, counties and the storm track with ETAs. Code: built page, `details(i)` and `render()` in the radar alerts module; `channel/sdr-warnfocus-tv.js` is the TV version. Bring the TV version up to date with the damage tags and track.
- **Labels**: no county or parish names as map labels. At continent scale, label countries, oceans and major cities, not small towns.

## 4. Forecast logic to copy
- **10-day**:
  - After 5 PM the first row is **TONIGHT**.
  - The low shown is that morning's low until 11 AM, today's low from 11 to 5, then tonight's.
  - Show feels-like only when it's 3°+ different from the temperature.
  - The rain strip has a time axis (6A/12P/6P) and a start marker.
- **Rain amounts**: within ~2.5 days, the likely amount = the official forecast amount, and the models' range is scaled around it. Never stretch the high end above the models. Past 2.5 days, use the model blend's middle half. Code: `block_design.py` → `attach(x,i)` (v208/v212).
- **Model agreement** (rebuilt, v212). Blend these factors, don't take the single worst:
  - Temperature spread vs. what's normal for that lead time: `sd / (2.2 + 0.45 × days out)`.
  - Will it rain: chances near 0 or 100% mean the models agree; near 50% means they don't.
  - How much: how many decision bands the range crosses (trace / .10 / .25 / .50 / 1 / 2 / 3"). Only counts when the likely amount is .10"+ or the high end .25"+.
  - Snow bands when snow is in play.
  - −1 point when the official amount and the models' middle differ by more than 2×.
  - The 10-day header shows the average of the next 3 days.
  - The reason line names the cause: "whether it rains", "how much rain" or "temperatures".
  - Code: `block_design.py` → `confOf`, `confWhy`.
- **What's Next** names the main window ("Storms tomorrow afternoon"), not the first sprinkle.
- **Known issue to fix on both**: don't say "storms nearby now" unless radar shows echoes nearby.

## 5. Briefings engine (the channel's briefing segment should use it as-is)
- One page and image-forward, in SDR colors and layout. Code: `block_daily.py` → `richDaily`, `_threat`, `_meansHZ`, `_means`, `_bottom`, `tempChart`, `weekTemps`.
- **Event briefings fire with no limits**: storms organizing, watches (within 25 miles), severe or flood outlook upgrades, warnings, freeze, heat, wind, winter, and **any Atlantic/Caribbean/Gulf tropical activity, near or far**.
- **Scheduled briefings**: morning, plus an afternoon/evening update. They step aside if the team posted within 12 hours. Events always outrank the team's briefing.
- **One briefing per threat**: an official alert and our own forecast become one briefing, and winter absorbs freeze.
- **Each threat reads its own way**:
  - Severe: when, main threat, what to do, shelter.
  - Flood: how much, what it does, flood actions.
  - Winter: snow amounts, start time, roads.
  - Freeze: how cold, the freezing hours, a second freeze if one is coming.
  - Heat, wind and regional ("Not at Greenville; closest part ~70 miles away").
  - Tropical: map, the chance, the exact spot ("about 350 miles south of the Louisiana coast"), distance from the client, and what it means locally when we're in the cone.
- **One main threat per page.** Subhead, panel and tiles agree. Tiles fit the threat: tornado tile under a tornado threat, flooding 4+ under a Flood Warning, snow & ice on winter pages.
- **Daily briefings lead with an active watch or warning.**
- **Bottom lines fit the threat**, e.g. "Tornado Watch in effect. Know where you'll shelter, and move people right away if a warning is issued."
- **Tested**: `lab/run.js` runs 15 scenarios, 29 pages, all one page, with a banned-phrase scan. Run it whenever briefing logic changes.

## 6. Maps the channel should carry
- **Tropics**: outlook areas (read layer 3 "Seven-Day: Potential Development Region"; the old name match missed it), forecast cones, and a wide Atlantic frame that stretches to fit areas out toward Africa. Wording is coast-first. Code: `block_design.py` → v210/v213, `SDR_TROPBOX`, `SDR_NEARPLACE`.
- **International basemap**: full country outlines with borders from `world-atlas@2.0.2` (countries-50m), decoded in the page; country, ocean and major-city labels. Code: `block_design.py` v212 (`SDR_BIGLBL`, `SDR_INTL`).
- **Winter impacts map**: already in the Map Room. Add it to the channel.
- **NEW for the channel**:
  - **Nationwide current conditions**: temperatures and a few cities' conditions across the U.S.
  - **Fronts**: surface fronts and highs/lows "coming in".
  - Both belong in the national rotation.

## 7. Sponsored segments (dashboard and 24/7 channel)
Each segment gets a 10-day outlook scored /10 with a one-line reason, a peak window, tap-for-detail in the app, and a full-screen slate on TV. There's a sponsor slot on every one.
- **Hunt & Fish** (built):
  - Deer Hunting and Fishing scores out of 10 for 10 days, with morning/midday/evening scores, a peak window, hour bars, reasons and "how to play it".
  - The moon is only a tiebreaker. Rut dates are set by region.
  - Code: `block_alm2.py` → `deerHour`, `fishHour`, `hfDay`.
- **Ski Conditions** (to build):
  - Nearby resorts: Cataloochee, Sugar, Beech, Appalachian, Wintergreen, Snowshoe…
  - New snow, base depth, fresh-powder alerts, summit feels-like, lift-wind holds, snowmaking nights (wet-bulb), a ski-day score and an hour-by-hour.
- **Beach & Boating** (to build):
  - Beach picker: Myrtle, Panama City Beach, Charleston/Folly, Tybee, Destin, Siesta Key, Miami Beach, Outer Banks, Jersey Shore.
  - Tides, wave height/period, rip current risk, water temperature, wind/chop, UV and lightning; beach-day and boat-day scores.
- **Lakes** (to build): Hartwell, Keowee, Jocassee, Lake Lure. Wind/chop, water temperature, lightning and a boat-day score.

## 8. Chat (if the channel ever shows the chat or Q&A)
- Claude answers with the dashboard data plus web search and a forecast for any place (`forecast_for_place`).
- It never uses the sample Schedule Watch events, never assumes plans, uses no slogans, and doesn't open with a status word.
- Code: `sdr-chat-worker.js`.

## 9. Suggested 24/7 rundown (loop ~10–12 min; warnings break in immediately)
1. Status + What's Next (local)
2. Radar, naked (local, then region)
3. Hour by hour + 10-day with model agreement
4. Latest briefing slate (one page)
5. National: current conditions → fronts → radar
6. Severe / flooding outlook maps (only when active)
7. Tropics (any activity) and winter impacts (in season)
8. Sponsored segment, rotating: Hunt & Fish → Ski (in season) → Beach & Boating / Lakes (in season)
9. Rivers / Rain Bucket

**Warning break-in**: full-screen branded warning card plus the warning polygon on radar and the storm track. It stays until the warning ends, then shows ALL CLEAR.

## 10. Files in this package
- `source/blocks/`: every dashboard patch block (`block_*.py`) and the chat page (`chat-src.html`).
- `source/built/greenville-index.html`: the finished dashboard page; all logic runs here.
- `source/channel/`: the existing TV pieces (`sdr-riskcard-tv.js`, `sdr-warnfocus-tv.js`, preview).
- `source/workers/`: the chat server and the private CJWX preview mirror.
- `source/lab/`: the test scripts (`run.js` briefings, `core.js` home screen, `warn.js` warning card).
- `CHANGELOG.md`: every version with what changed.
- `NEXT-SESSION-PLAN.md`: push server, remaining tests and the goodies.
