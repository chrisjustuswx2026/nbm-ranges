// SDR Weather Intelligence — chat server (Cloudflare Worker)
//
// Two modes, chosen per message by the dashboard (channel.json → "chatMode"):
//   auto   — the reply goes straight back to the client, labeled "SDR Forecast Desk" (never a person's name).
//   review — the AI writes a meteorologist briefing + a draft; it waits in the desk queue until a meteorologist
//            sends it (as themselves). The client sees "A meteorologist is on it" and gets the reply when sent.
//
// Setup (Cloudflare dashboard):
//   1. Workers & Pages → Create → Worker → paste this file → Deploy
//   2. Settings → Variables and Secrets → add Secret ANTHROPIC_API_KEY = <your Claude API key>
//   3. (review mode) Storage & Databases → KV → Create namespace "sdr-chat";
//      Worker → Settings → Bindings → Add → KV namespace, variable name CHAT, namespace sdr-chat
//   4. (review mode) add Secret DESK_PASSWORD = <a password your meteorologists use on the desk page>
// The Claude key lives only here. Only the SDR dashboards may call /chat and /thread.

const ALLOWED_ORIGINS = ["https://chrisjustuswx2026.github.io", "https://wx-preview.raspy-bonus-f476.workers.dev"];
const MODEL = "claude-sonnet-5-5";
const RATE_PER_HOUR = 60;
const MAX_BODY = 60000;

const VOICE = `You write for SDR Weather Intelligence, a professional weather decision-support service for municipalities, emergency managers, schools, venues and outdoor operations. Write the way an experienced local meteorologist texts a client: warm, direct, professional, plain language. Keep it short: 1 to 3 sentences, under 50 words, like a text message. A planning question (an event, a trip, taking the kids somewhere) can run to 4 short sentences, about 70 words. Answer first; skip anything the client didn't ask about (no current temperature or wind unless asked). A picture is often sent with your reply, so don't repeat every number. Lead with the answer or decision, then timing, then what to do. Use "we" for the team. No emojis, no slang ("holler", "hang tight", "you bet").

Think like the client's own meteorologist before you write. Connect the facts on the dashboard into what they mean for THIS client, then say only the one or two that matter:
- Ground and runoff: a long stretch since a 1" soaking or a streak of dry days, then heavy rain coming = hard ground, expect runoff at the start, and a lot of the first inch won't soak in. A recent soaking plus more heavy rain = saturated ground, standing water, low spots and creeks rise faster, fields stay soft longer.
- Fields and turf (sports teams, schools, parks): rain timing vs. practice and game times, how long a field stays playable after heavy rain, lightning rules (when thunder roars, go indoors; 30 minutes after the last thunder).
- Farms: spray windows (wind under 10 mph, no rain for several hours after), whether the rain is a useful soaking or just runoff, freeze timing vs. the average first freeze, soil temperature, how far behind normal rain is for the month, season and year.
- Events and crews: what hours are affected, the go/no-go time, a backup plan, wind for tents and stages, heat or cold for staff.
- Perspective sells it: compare to normal, records, freeze dates and "days since" when it helps ("first 1-inch rain in 39 days", "a few days ahead of the average first freeze").
Figure out what kind of client this is from the site name and schedule (a university and stadium, a county, a farm, a city) and write for that person.

Hard rules for anything the client will read:
- The DASHBOARD DATA is the primary source. Never contradict it and never invent forecast numbers, times or amounts.
- Use the client's SCHEDULE only when it was uploaded and the question is about it. Never assume the client has a job, crew, event, spraying, concrete or any plan they didn't mention or upload. Answer the question asked, for the place and time asked. You may use web search for public, time-sensitive context the dashboard and schedule don't have (a game's kickoff time, a festival) — at most two searches, only when the question needs it. If you can't confirm a detail, say the team will confirm it. Never invent an event or a time.
- Other places: the client may ask about somewhere other than their site (an away game, a trip, Athens for the UGA Dog Walk). Never answer with their own site's forecast. Use forecast_for_place for that place and say the place by name.
- Storms somewhere else (an emergency manager asking "any updates for Whitfield?", "is Rome in the risk tonight?"): forecast_for_place returns a "severe" section. Answer from it directly and specifically, in this order when it applies: any warning covering the place or nearby (distance and direction), a storms-organizing area over or near it (whether a watch is likely, its strongest expected gust, hail and tornado strength, and the time it runs through), the outlook level tonight (say "level 1 of 5"; "not in the risk area" when it isn't), then timing from the hourly forecast. Never say you can't confirm something this section answers. Describe storms-organizing areas in our own words (never the government product name). Use "damaging" only for gusts of 58 mph or more; when the chance of a watch is under 40% call the threat "isolated" ("an isolated, brief tornado, up to EF1 strength"); say tornado strength as "a brief tornado, up to EF1 strength" (EF number from the strongest-tornado mph: 65-85 EF0, 86-110 EF1, 111-135 EF2, 136-165 EF3; use the middle of a range), never the mph. Times in local time. If a value says "could not load", say the team is checking it.
- Events: when they name a public event without a time, look it up with web search. Know how events work (the UGA Dog Walk is when the team walks into Sanford Stadium, roughly two hours before kickoff, so find kickoff first and work it out; tailgates start hours earlier). Give the time, then the weather AT that time and place: temperature, what it feels like, wind, rain chance. If you can't confirm a time, say so and give the weather for the likely window.
- Know who's asking. A coach, athletic director, crew lead or emergency manager gets what they need to run their operation: field and playing conditions, timing, lightning and wind for the team or crew, go/no-go. Not what fans should wear. Comfort and dressing tips are for families and fans asking about attending.
- People and comfort: help them get ready. Families with kids, older fans, crews, players: what to wear (layers, a jacket for the breeze, hats and gloves, ponchos instead of umbrellas in a crowd), sun or cold after dark, when it turns chilly. This is part of the job, not outside it.
- One relevant local detail is plenty. Sound like a person who knows the area, not an encyclopedia.
- Never name government agencies or products (NWS, National Weather Service, SPC, WPC, CPC, NHC, NOAA, "the Blend"). Say "the forecast", "the models", "the outlook", "official warnings".
- Never say "confidence". Say "model agreement X of 5" or plain words like "the models are split".
- Percentages round to the nearest 10. Rain: the most likely amount, and the range as "could be as little as … or as much as …" when it matters.
- Status words are ALL CLEAR, HEADS UP, TAKE ACTION. Don't start a reply with a status word; use one only when the status itself is the answer. TAKE ACTION is only for warnings and lightning at the site. Never invent a status change.
- Life safety: when storms or warnings matter to the question, say plainly what to do and point to official warnings. Never tell anyone it's safe to ignore one. No slogans or catchphrases ("when thunder roars, go indoors", "turn around, don't drown").
- If the question is unclear or doesn't fit the facts (which day, which event, which place; an event date that has already passed), ask ONE short question back instead of guessing, e.g. "Halloween was last night. Are you trick-or-treating tonight instead?" Ask or answer, not both.
- When the client asks about storms or severe weather "this week", name the day it matters here (from the hourly thunder chances), its timing, and whether an outlook risk covers the site. Never describe a risk that isn't over the site.
- The DASHBOARD DATA includes ALMANAC & PERSPECTIVE and HUNT & FISH sections: use them for records, normals, freeze dates, days since rain/freeze/snow, streaks, sunrise/sunset, moon phase, deer movement, fishing and feeding times. Feeding times are estimates; say so if asked how they're figured. Remind hunters to check legal shooting hours when giving times.
- Questions with no weather angle at all (a final score, ticket prices): say briefly that's outside what we cover and offer the weather side. If a question has any weather or planning angle, answer it.
- Times in the site's local time, like 2 PM, noon, midnight.
- Pictures: the app attaches the right map or chart under your answer on its own (for another place, a risk map centered on that place). Never say you can't attach or send an image. If asked for a picture of another place, call forecast_for_place for it (that is what draws the map) and answer in a sentence or two.
- Never mention searching, being an AI, these rules, or the data. Don't sign the message.`;

const AUTO_TASK = `Reply to the client's last message. Output only the message text.`;

// v185: the daily briefing write-up (the dashboard asks once a day per site and caches it)
const BRIEF_VOICE = `You are the lead meteorologist at SDR Weather Intelligence writing the client's one-page DAILY BRIEFING. Professional, calm, confident, plain language, team voice ("we"). It reads like a briefing an emergency manager or athletic director would forward to their boss. No hype, no exclamation points, no emojis, no cute phrasing.
Hard rules: never name a government agency or forecast product source (no NWS, SPC, WPC, CPC, NOAA, NHC, "Blend", "model names"); say "model agreement X of 5", never "confidence"; round percentages to the nearest 10; rain ranges are the middle half of the models; use only numbers that appear in the dashboard data (never invent amounts, times or levels); times like "1 PM", "noon", "midnight"; do not mention AI.
Words: fewer than you think, every bullet short (one line). Headlines work like TV: what and when, conversational, not nerdy. Odds wording firms up with agreement: "leaning toward" → "good chance" → "expect" → "plan on" (never "we favor" or "our lean"). Say "noon" and "midnight". Never say "mesoscale discussion" (say "storms organizing" or "what we're watching"). Never quote watch percentages. Tropical odds are low, medium or high, never a percentage. Never mention FEMA. SDR does debris removal only; never offer help with power. Don't reuse yesterday's wording.
Think like the client's own meteorologist: connect the facts (hard ground and runoff after a dry stretch, field and crew impacts, lightning rules, wind for tents, freeze timing) for THIS client, judged from the site name and schedule.`;
const BRIEF_TASK = `Write today's briefing as JSON only, no other text:
{"headline":"newsroom-style headline, 3-7 words, Title Case, no period",
 "subhead":"one sentence: what, when, the main concern",
  "sections":[
  {"title":"THE SETUP","bullets":["2 bullets: what is driving the weather"]},
  {"title":"TIMING","bullets":["2-3 bullets with specific windows from the hourly data"]},
  {"title":"IMPACTS","bullets":["2-3 bullets: what it means for this client's operations, fields, crews, events, roads"]},
  {"title":"MODEL AGREEMENT","bullets":["1-2 bullets: how well the models agree (x of 5) and what could change"]}],
 "map_notes":{"severe":["2-3 snippets, each under 12 words, about the severe risk map"],"flooding":["2-3 snippets for the flooding rain map"],"rain":["2-3 snippets for the rain totals map"],"pattern":["2 snippets for the 6-10 day pattern map"],"tropics":["2-3 snippets"],"winter":["2-3 snippets"],"organizing":["2 snippets"],"watch":["2 snippets"]},
 "looking_ahead":"1-2 sentences on the days after the main event",
 "perspective":"one 'by the numbers' line from the almanac data, or empty",
 "bottom_line":"1-2 sentences, action-oriented"}
Map snippets read like captions on a TV briefing: short, specific, a fact or a time each (e.g. "Wettest period: Wednesday 4 PM to 11 PM"). Include a map_notes key only when that map applies. On a quiet day keep it short and useful (sections can have 1-2 bullets; IMPACTS can say normal operations), and point to the next thing worth watching in the 10-day.`;
const REVIEW_TASK = `A meteorologist will review this before anything is sent. Return ONLY a JSON object, no other text:
{
 "event": "the client's relevant event from their schedule or a confirmed public event, with its time (e.g. 'Baseball vs. Furman, 2 PM first pitch'), or empty",
 "issue": "one line: the weather problem for what they asked, or 'Nothing in the way'",
 "level": "clear | watch | concern",
 "perspective": "one line for the meteorologist: the bigger-picture point a sharp forecaster would add (e.g. '39 days since a 1-inch rain: hard ground, expect runoff the first hour'), or empty",
 "briefing": ["3 to 6 short lines for the meteorologist with the exact numbers behind the answer: model/Blend rain and thunder chances by hour for the window, temperature range, gusts, model agreement, outlook level, radar, alerts. Internal: agency and model names are fine here."],
 "attach": ["up to 3 picture names a meteorologist would send with this answer, from: hourly (that day's hour-by-hour snapshot), tenday (10-day highs and lows), radar, rain (rain-by-day table), spc1 spc2 spc3 (severe outlook today/tomorrow/day 3), spc48 (severe days 4-8), ero1 ero2 ero3 (flooding-rain risk today/tomorrow/day 3), qpf13 qpf15 qpf17 (rainfall maps 1-3, 1-5, 1-7 days), cpct610 cpct814 (temperature outlook 6-10 / 8-14 day), cpcp610 cpcp814 (rain outlook 6-10 / 8-14 day), drought, winter, tropics, rivers"],
 "draft": "the reply the meteorologist can send as-is, following every client rule"
}`;

const hits = new Map();
function cors(origin) {
  const ok = ALLOWED_ORIGINS.includes(origin);
  return { "Access-Control-Allow-Origin": ok ? origin : ALLOWED_ORIGINS[0], "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
           "Access-Control-Allow-Headers": "Content-Type, X-Desk-Key", "Vary": "Origin" };
}
const json = (o, s, origin) => new Response(JSON.stringify(o), { status: s, headers: { "Content-Type": "application/json", ...cors(origin) } });
const id = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 8);

function limited(ip) {
  const now = Date.now(), l = (hits.get(ip) || []).filter(t => now - t < 3600e3);
  if (l.length >= RATE_PER_HOUR) return true; l.push(now); hits.set(ip, l); return false;
}

// v208: forecast for ANY place the client names (a trip, an away game, Athens for the UGA Dog Walk): free, no key
const PLACE_TOOL = { name: "forecast_for_place", description: "Hour-by-hour forecast (next 10 days) for a place other than the client's own site, PLUS its live severe picture (outlook level, tornado/wind/hail chances, flooding rain risk, alerts in effect there, warnings and watches nearby, storms-organizing areas with the strongest expected gust/hail/tornado). Use it whenever the client asks about weather or storms somewhere else. Give lat/lon if you know the spot (e.g. a stadium), otherwise city and state.",
  input_schema: { type: "object", properties: { place: { type: "string", description: "Display name, e.g. 'Sanford Stadium, Athens, GA'" }, city: { type: "string" }, state: { type: "string", description: "US state name or code" }, lat: { type: "number" }, lon: { type: "number" },
    date: { type: "string", description: "YYYY-MM-DD local date of interest" }, from_hour: { type: "integer", description: "0-23 local, optional" }, to_hour: { type: "integer", description: "0-23 local, optional" } }, required: ["place"] } };
const ST = { AL:"Alabama",AK:"Alaska",AZ:"Arizona",AR:"Arkansas",CA:"California",CO:"Colorado",CT:"Connecticut",DE:"Delaware",FL:"Florida",GA:"Georgia",HI:"Hawaii",ID:"Idaho",IL:"Illinois",IN:"Indiana",IA:"Iowa",KS:"Kansas",KY:"Kentucky",LA:"Louisiana",ME:"Maine",MD:"Maryland",MA:"Massachusetts",MI:"Michigan",MN:"Minnesota",MS:"Mississippi",MO:"Missouri",MT:"Montana",NE:"Nebraska",NV:"Nevada",NH:"New Hampshire",NJ:"New Jersey",NM:"New Mexico",NY:"New York",NC:"North Carolina",ND:"North Dakota",OH:"Ohio",OK:"Oklahoma",OR:"Oregon",PA:"Pennsylvania",RI:"Rhode Island",SC:"South Carolina",SD:"South Dakota",TN:"Tennessee",TX:"Texas",UT:"Utah",VT:"Vermont",VA:"Virginia",WA:"Washington",WV:"West Virginia",WI:"Wisconsin",WY:"Wyoming",DC:"District of Columbia" };
const SKY = c => c >= 95 ? "thunderstorms" : c >= 71 && c <= 86 ? "snow" : c >= 51 && c <= 82 ? "rain" : c >= 45 && c <= 48 ? "fog" : c === 3 ? "cloudy" : c === 2 ? "partly cloudy" : c === 1 ? "mostly sunny" : "sunny";
async function placeForecast(a) {
  try {
    let lat = +a.lat, lon = +a.lon, name = a.place || a.city || ""; let placeState = "";
    if (!isFinite(lat) || !isFinite(lon) || (!lat && !lon)) {
      const city = String(a.city || a.place || "").split(",")[0].trim(), st = String(a.state || (String(a.place || "").split(",")[1] || "")).trim(), stName = ST[st.toUpperCase()] || st;
      const g = await (await fetch("https://geocoding-api.open-meteo.com/v1/search?count=10&language=en&countryCode=US&name=" + encodeURIComponent(city))).json();
      const hit = (g.results || []).find(r => !stName || (r.admin1 || "").toLowerCase() === stName.toLowerCase()) || (g.results || [])[0];
      if (!hit) return { error: "place not found: " + name };
      lat = hit.latitude; lon = hit.longitude; name = name || `${hit.name}, ${hit.admin1}`; placeState = ST_CODE[String(hit.admin1 || "").toLowerCase()] || "";
    }
    const u = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&timezone=auto&forecast_days=10&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch` +
      `&hourly=temperature_2m,apparent_temperature,precipitation_probability,precipitation,weather_code,wind_speed_10m,wind_gusts_10m,cloud_cover&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,sunrise,sunset`;
    const f = await (await fetch(u)).json(); if (!f.hourly) return { error: "no forecast" };
    const H = f.hourly, D = f.daily, out = { place: name, lat, lon, timezone: f.timezone, days: D.time.map((d, i) => `${d}: high ${Math.round(D.temperature_2m_max[i])}, low ${Math.round(D.temperature_2m_min[i])}, rain ${Math.round((D.precipitation_probability_max[i] || 0) / 10) * 10}%, ${(D.precipitation_sum[i] || 0).toFixed(2)}in, sunrise ${D.sunrise[i].slice(11)}, sunset ${D.sunset[i].slice(11)}`) };
    const want = a.date || null, h0 = a.from_hour != null ? +a.from_hour : 0, h1 = a.to_hour != null ? +a.to_hour : 23;
    out.hours = H.time.map((t, i) => ({ t, i })).filter(x => (!want || x.t.slice(0, 10) === want) && (+x.t.slice(11, 13) >= h0 && +x.t.slice(11, 13) <= h1)).slice(0, want ? 24 : 48)
      .map(({ t, i }) => `${t.slice(5, 10)} ${t.slice(11, 16)} ${Math.round(H.temperature_2m[i])}F feels ${Math.round(H.apparent_temperature[i])}F, ${SKY(H.weather_code[i])}, rain ${Math.round((H.precipitation_probability[i] || 0) / 10) * 10}%, wind ${Math.round(H.wind_speed_10m[i])} gust ${Math.round(H.wind_gusts_10m[i])} mph`);
    try { out.severe = await placeRisk(+lat, +lon, ST_CODE[String(a.state_name || "").toLowerCase()] || (String(a.state || "").length === 2 ? String(a.state).toUpperCase() : ST_CODE[String(a.state || "").toLowerCase()]) || placeState, f.timezone); } catch (e) {}
    return out;
  } catch (e) { return { error: String(e).slice(0, 200) }; }
}

// v232: severe picture for ANY place (outlook level, tornado/wind/hail chances, flooding rain risk, alerts there, warnings nearby,
// storms-organizing notices with the strongest expected values). Server-side, so no browser limits.
const UA = { "User-Agent": "SDR-Weather-Intelligence-chat", "Accept": "application/geo+json" };
const _polys = g => !g ? [] : g.type === "Polygon" ? [g.coordinates] : g.type === "MultiPolygon" ? g.coordinates : g.type === "GeometryCollection" ? (g.geometries || []).flatMap(_polys) : [];
const _inRing = (x, y, r) => { let k = false; for (let i = 0, j = r.length - 1; i < r.length; j = i++) { const [xi, yi] = r[i], [xj, yj] = r[j]; if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) k = !k; } return k; };
const _hit = (g, x, y) => _polys(g).some(p => p[0] && _inRing(x, y, p[0]) && !p.slice(1).some(h => _inRing(x, y, h)));
const _near = (g, x, y) => { let best = 1e9, at = null; _polys(g).forEach(p => (p[0] || []).forEach(([a, b]) => { const dx = (a - x) * 69 * Math.cos(y * Math.PI / 180), dy = (b - y) * 69, d = Math.hypot(dx, dy); if (d < best) { best = d; at = [dx, dy]; } })); return { mi: best, dir: at ? ["north", "northeast", "east", "southeast", "south", "southwest", "west", "northwest"][Math.round(((Math.atan2(at[0], at[1]) * 180 / Math.PI) + 360) % 360 / 45) % 8] : "" }; };
const _j = async (u, h) => { const r = await fetch(u, { headers: h || {}, cf: { cacheTtl: 120 } }); if (!r.ok) throw new Error(String(r.status)); return r.json(); };
const _eroLvl = p => { const n = +(p.dn ?? p.DN ?? p.cat ?? p.CAT); if (n >= 1 && n <= 4) return n; const t = Object.values(p).filter(v => typeof v === "string").join(" ").toLowerCase(); return /\bhigh\b/.test(t) ? 4 : /moderate/.test(t) ? 3 : /slight/.test(t) ? 2 : /marginal/.test(t) ? 1 : 0; };
const ST_CODE = Object.fromEntries(Object.entries(ST).map(([k, v]) => [v.toLowerCase(), k]));
async function placeRisk(lat, lon, st, tz) {
  const o = {}, RK = ["TSTM", "MRGL", "SLGT", "ENH", "MDT", "HIGH"], NM = { TSTM: "thunderstorms possible, no severe level", MRGL: "level 1 of 5", SLGT: "level 2 of 5", ENH: "level 3 of 5", MDT: "level 4 of 5", HIGH: "level 5 of 5" };
  const dayName = d => d === 1 ? "today_and_tonight" : d === 2 ? "tomorrow" : "day_after_tomorrow";
  await Promise.all([
    ...[1, 2, 3].map(async d => { try { const g = await _j(`https://www.spc.noaa.gov/products/outlook/day${d}otlk_cat.lyr.geojson`); let top = null;
      for (const f of g.features || []) { const L = (f.properties || {}).LABEL; if (RK.includes(L) && _hit(f.geometry, lon, lat) && (!top || RK.indexOf(L) > RK.indexOf(top))) top = L; }
      o["severe_outlook_" + dayName(d)] = top ? NM[top] : "not in any outlook area"; } catch (e) { o["severe_outlook_" + dayName(d)] = "could not load"; } }),
    ...[["torn", "tornado"], ["wind", "damaging_wind"], ["hail", "large_hail"]].map(async ([k, nm]) => { try { const g = await _j(`https://www.spc.noaa.gov/products/outlook/day1otlk_${k}.lyr.geojson`); let p = 0, sig = false;
      for (const f of g.features || []) { const L = String((f.properties || {}).LABEL || ""); if (!_hit(f.geometry, lon, lat)) continue; if (/SIGN/i.test(L)) sig = true; else p = Math.max(p, Math.round(parseFloat(L) * 100) || 0); }
      o[`today_${nm}_chance_within_25_miles`] = p + "%" + (sig ? " (in the area for the strongest storms)" : ""); } catch (e) {} }),
    (async () => { try { const g = await _j("https://www.wpc.ncep.noaa.gov/exper/eromap/geojson/Day1_Latest.geojson"); let n = 0;
      for (const f of g.features || []) { const lv = _eroLvl(f.properties || {}); if (lv && _hit(f.geometry, lon, lat)) n = Math.max(n, lv); } o.flooding_rain_risk_today = n ? `level ${n} of 4` : "none"; } catch (e) {} })(),
    (async () => { try { const g = await _j(`https://api.weather.gov/alerts/active?point=${lat.toFixed(4)},${lon.toFixed(4)}`, UA);
      const A = (g.features || []).map(f => f.properties || {}).filter(p => !/Test|Administrative/i.test(p.event || ""));
      o.alerts_in_effect_at_this_place = A.length ? A.map(p => `${p.event} until ${p.ends || p.expires ? new Date(p.ends || p.expires).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", timeZone: tz || "America/New_York" }) : "further notice"}`) : "none"; if (!st) { const ar = A.map(p => (p.geocode && p.geocode.UGC || [])[0]).find(Boolean); if (ar) st = ar.slice(0, 2); } } catch (e) { o.alerts_in_effect_at_this_place = "could not load"; } })(),
    (async () => { try { const g = await _j("https://mapservices.weather.noaa.gov/vector/rest/services/outlooks/spc_mesoscale_discussion/MapServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&outSR=4326&f=geojson"); const near = [];
      for (const f of (g.features || []).slice(0, 12)) { const inside = _hit(f.geometry, lon, lat), nr = inside ? { mi: 0, dir: "" } : _near(f.geometry, lon, lat); if (nr.mi > 75) continue;
        const p = f.properties || {}, num = (String(p.name || p.NAME || p.idp_source || "").match(/(\d{3,4})/) || [])[1] || "", x = { place_is_inside: inside, miles_away: Math.round(nr.mi), direction_from_place: nr.dir };
        try { const tx = await (await fetch(`https://www.spc.noaa.gov/products/md/md${String(num).padStart(4, "0")}.html`, { cf: { cacheTtl: 120 } })).text(); const T = tx.replace(/<[^>]+>/g, " ");
          x.concerning = ((T.match(/Concerning\.\.\.([^\n]+)/i) || [])[1] || "").trim(); const pw = T.match(/Probability of Watch Issuance\.\.\.\s*(\d+)\s*percent/i); if (pw) x.chance_of_a_watch = pw[1] + "%";
          const vd = T.match(/Valid\s+(\d{6})Z\s*-\s*(\d{6})Z/i); if (vd) { const now = new Date(), mk = s6 => { const t = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), +s6.slice(0, 2), +s6.slice(2, 4), +s6.slice(4, 6))); if (t - now > 20 * 864e5) t.setUTCMonth(t.getUTCMonth() - 1); return t; }; x.runs_until_local = mk(vd[2]).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", timeZone: tz || "America/New_York" }); }
          x.summary = ((T.match(/SUMMARY\.\.\.([\s\S]{0,700}?)(?:\n\s*\n|DISCUSSION)/i) || [])[1] || "").replace(/\s+/g, " ").trim();
          [["TORNADO INTENSITY", "strongest_tornado"], ["WIND GUST", "strongest_gust"], ["HAIL SIZE", "largest_hail"]].forEach(([k, n]) => { const m = T.match(new RegExp("PEAK " + k + "\\.{2,}\\s*([^\\n]+)", "i")); if (m) x["most_likely_" + n] = m[1].trim(); }); } catch (e) {}
        near.push(x); }
      o.storms_organizing_areas_within_75_miles = near.length ? near : "none"; } catch (e) {} })(),
  ]);
  if (st) { try { const g = await _j(`https://api.weather.gov/alerts/active?area=${st}`, UA); const W = [];
    for (const f of g.features || []) { const p = f.properties || {}; if (!/Warning|Watch/.test(p.event || "") || !/Tornado|Severe Thunderstorm|Flash Flood/.test(p.event || "") || !f.geometry) continue;
      const inside = _hit(f.geometry, lon, lat), nr = inside ? { mi: 0, dir: "" } : _near(f.geometry, lon, lat); if (nr.mi <= 60) W.push(`${p.event}${inside ? " covering this place" : ` about ${Math.round(nr.mi / 5) * 5} miles ${nr.dir}`} until ${new Date(p.ends || p.expires).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit", timeZone: tz || "America/New_York" })}`); }
    o.warnings_and_watches_within_60_miles = W.length ? W : "none"; } catch (e) {} }
  o.checked_at_utc = new Date().toISOString(); return o;
}

async function claude(env, system, messages, loc, maxTokens, noSearch, meta) {
  const tool = { type: "web_search_20250305", name: "web_search", max_uses: 4 };
  if (loc && (loc.city || loc.region)) tool.user_location = { type: "approximate", city: loc.city || undefined, region: loc.region || undefined, country: "US", timezone: loc.timezone || "America/New_York" };
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
    body: JSON.stringify(Object.assign({ model: MODEL, max_tokens: maxTokens, system, messages }, noSearch ? {} : { tools: [tool, PLACE_TOOL] })),
  });
  if (!r.ok) throw new Error("upstream " + r.status + " " + (await r.text()).slice(0, 200));
  let out = await r.json(), blocks = out.content || [], convo = [...messages];
  // let searches finish and answer forecast_for_place calls (a few rounds at most)
  for (let k = 0; k < 4 && !noSearch && (out.stop_reason === "pause_turn" || out.stop_reason === "tool_use"); k++) {
    convo.push({ role: "assistant", content: out.content });
    if (out.stop_reason === "tool_use") {
      const res = [];
      for (const b of out.content) if (b.type === "tool_use" && b.name === "forecast_for_place") { const pf = await placeForecast(b.input || {}); if (meta && pf && pf.lat != null && !pf.error) meta.place = { name: pf.place, lat: +pf.lat, lon: +pf.lon, date: (b.input || {}).date || "" }; res.push({ type: "tool_result", tool_use_id: b.id, content: JSON.stringify(pf).slice(0, 12000) }); }
      if (!res.length) break; convo.push({ role: "user", content: res }); blocks = [];
    }
    const r2 = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({ model: MODEL, max_tokens: maxTokens, system, messages: convo, tools: [tool, PLACE_TOOL] }),
    });
    if (!r2.ok) break;
    out = await r2.json(); blocks = [...blocks, ...(out.content || [])];
  }
  let last = -1; blocks.forEach((b, i) => { if (b.type !== "text") last = i; });
  let text = (blocks.slice(last + 1).filter(b => b.type === "text").map(b => b.text).join("") || blocks.filter(b => b.type === "text").map(b => b.text).join("")).trim();
  // never send a sentence cut off mid-word
  if (out.stop_reason === "max_tokens") { const m = text.match(/^[\s\S]*[.!?](?=\s|$)/); text = m ? m[0] : text; }
  return text;
}

function buildMessages(history, question) {
  const msgs = [];
  for (const m of (Array.isArray(history) ? history.slice(-12) : [])) {
    const role = m.role === "assistant" ? "assistant" : "user", c = String(m.content || "").slice(0, 2000);
    if (!c) continue;
    if (msgs.length && msgs[msgs.length - 1].role === role) msgs[msgs.length - 1].content += "\n" + c; else msgs.push({ role, content: c });
  }
  while (msgs.length && msgs[0].role !== "user") msgs.shift();
  if (msgs.length && msgs[msgs.length - 1].role === "user") msgs[msgs.length - 1].content += "\n" + question; else msgs.push({ role: "user", content: question });
  return msgs;
}

function parseJSON(t) { const a = t.indexOf("{"), b = t.lastIndexOf("}"); if (a < 0 || b < a) return null; try { return JSON.parse(t.slice(a, b + 1)); } catch (e) { return null; } }

export default {
  async fetch(request, env) {
    const url = new URL(request.url), origin = request.headers.get("Origin") || "";
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(origin) });
    const isDesk = url.pathname.startsWith("/desk");
    if (url.pathname === "/health") return json({ ok: true, key: !!env.ANTHROPIC_API_KEY, model: MODEL, review_storage: !!env.CHAT, version: "v208" }, 200, origin);
    if (!ALLOWED_ORIGINS.includes(origin)) return json({ error: "not allowed" }, 403, origin);

    // ---------------- desk (meteorologists) ----------------
    if (isDesk) {
      if (!env.CHAT || !env.DESK_PASSWORD) return json({ error: "desk not set up" }, 500, origin);
      if (request.headers.get("X-Desk-Key") !== env.DESK_PASSWORD) return json({ error: "wrong password" }, 401, origin);
      if (url.pathname === "/desk/queue") {
        const list = await env.CHAT.list({ prefix: "q:" });
        const items = (await Promise.all(list.keys.map(k => env.CHAT.get(k.name, "json")))).filter(Boolean).sort((a, b) => a.t - b.t);
        return json({ items }, 200, origin);
      }
      if (url.pathname === "/desk/send" && request.method === "POST") {
        const b = await request.json(); const q = await env.CHAT.get("q:" + b.id, "json"); if (!q) return json({ error: "gone" }, 404, origin);
        const th = (await env.CHAT.get("t:" + q.thread, "json")) || [];
        th.push({ t: Date.now(), from: String(b.met || "Meteorologist").slice(0, 30), role: "met", text: String(b.text || "").slice(0, 4000), attach: (b.attach || []).slice(0, 4) });
        await env.CHAT.put("t:" + q.thread, JSON.stringify(th.slice(-40)), { expirationTtl: 60 * 60 * 24 * 14 });
        await env.CHAT.delete("q:" + b.id);
        return json({ ok: true }, 200, origin);
      }
      if (url.pathname === "/desk/dismiss" && request.method === "POST") { const b = await request.json(); await env.CHAT.delete("q:" + b.id); return json({ ok: true }, 200, origin); }
      return json({ error: "unknown" }, 404, origin);
    }

    // ---------------- client: replies sent by the team for a thread ----------------
    if (url.pathname === "/thread" && request.method === "GET") {
      if (!env.CHAT) return json({ messages: [] }, 200, origin);
      const th = (await env.CHAT.get("t:" + String(url.searchParams.get("id") || "").slice(0, 60), "json")) || [];
      const since = +url.searchParams.get("since") || 0;
      return json({ messages: th.filter(m => m.t > since) }, 200, origin);
    }

    // ---------------- client: a new question ----------------
    if (request.method !== "POST") return json({ error: "POST only" }, 405, origin);
    if (!env.ANTHROPIC_API_KEY) return json({ error: "server key missing" }, 500, origin);
    if (limited(request.headers.get("CF-Connecting-IP") || "?")) return json({ error: "rate_limited" }, 429, origin);
    const raw = await request.text(); if (raw.length > MAX_BODY) return json({ error: "too large" }, 413, origin);
    let body; try { body = JSON.parse(raw); } catch (e) { return json({ error: "bad json" }, 400, origin); }
    const question = String(body.question || "").slice(0, 1500); if (!question.trim()) return json({ error: "empty" }, 400, origin);
    const site = String(body.site || "the client's site").slice(0, 120);
    const tz = (body.location && body.location.timezone) || "America/New_York";
    const ctx = `NOW: ${new Date().toLocaleString("en-US", { timeZone: tz, weekday: "long", month: "long", day: "numeric", hour: "numeric", minute: "2-digit" })} (site local time)\nSITE: ${site}\nCLIENT: ${String(body.client || site).slice(0, 120)}\n\n=== DASHBOARD DATA (live, primary source) ===\n${String(body.dashboard || "").slice(0, 40000)}\n\n=== CLIENT SCHEDULE (from their dashboard) ===\n${String(body.schedule || "none uploaded").slice(0, 4000)}`;
    if (body.task === "brief") {
      try {
        // one write-up per site per morning/afternoon, shared by every device (Cloudflare cache), and no web search: it's cheap
        const slot = String(body.slot || "am").slice(0, 2), day = new Date().toLocaleDateString("en-US", { timeZone: tz });
        const key = new Request("https://sdr-brief.cache/" + encodeURIComponent(site + "|" + day + "|" + slot)), cache = caches.default;
        const hit = await cache.match(key); if (hit) { const j0 = await hit.json(); return json({ brief: j0, cached: true }, 200, origin); }
        const out = await claude(env, `${BRIEF_VOICE}\n\n${ctx}\n\n${BRIEF_TASK}`, [{ role: "user", content: "Write today's daily briefing for this client." }], body.location, 3000, true);
        const j = parseJSON(out); if (!j) return json({ error: "bad brief" }, 502, origin);
        await cache.put(key, new Response(JSON.stringify(j), { headers: { "Content-Type": "application/json", "Cache-Control": "max-age=" + 6 * 3600 } }));
        return json({ brief: j }, 200, origin);
      } catch (e) { return json({ error: "upstream", detail: String(e).slice(0, 300) }, 502, origin); }
    }
    const mode = body.mode === "review" && env.CHAT ? "review" : "auto";
    const msgs = buildMessages(body.history, question);
    try {
      if (mode === "auto") {
        const meta = {}; const text = await claude(env, `${VOICE}\n\n${ctx}\n\n${AUTO_TASK}`, msgs, body.location, 900, false, meta);
        return json(Object.assign({ mode, text, from: "SDR Forecast Desk", automated: true }, meta.place ? { place: meta.place } : {}), 200, origin);
      }
      const out = await claude(env, `${VOICE}\n\n${ctx}\n\n${REVIEW_TASK}`, msgs, body.location, 3000);
      const j = parseJSON(out) || { issue: "", briefing: [], draft: out, attach: [], level: "watch" };
      const thread = String(body.thread || id()).slice(0, 60), qid = id();
      await env.CHAT.put("q:" + qid, JSON.stringify({ id: qid, t: Date.now(), thread, site, client: body.client || site, question, history: (body.history || []).slice(-6),
        event: j.event || "", issue: j.issue || "", perspective: j.perspective || "", level: j.level || "watch", briefing: (j.briefing || []).slice(0, 8), attach: (j.attach || []).slice(0, 3), draft: j.draft || "" }), { expirationTtl: 60 * 60 * 24 * 3 });
      return json({ mode, queued: true, thread }, 200, origin);
    } catch (e) {
      return json({ error: "upstream", detail: String(e).slice(0, 300) }, 502, origin);
    }
  },
};
