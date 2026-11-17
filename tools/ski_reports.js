// ============================================================
//  SKI REPORTS for the SDR dashboards (and the 24/7 channel). Runs inside the GitHub job, Nov–Mar.
//  Opens each resort's own snow report page in a real browser (many pages build their numbers after loading),
//  reads trails / lifts / base / new snow / opening date with the SAME reader as the channel (ski.js parse),
//  and writes public/resorts.json. A resort that can't be read is listed under "_missed" and shows forecast-only.
//  Usage: node site/tools/ski_reports.js public
// ============================================================
const fs = require("fs"), path = require("path");
const OUT = path.resolve(process.argv[2] || "public", "resorts.json");
const R = [
 ["Cataloochee","https://cataloochee.com/the-mountain/snow-report/"],["Sugar Mountain","https://www.skisugar.com/snowreport"],["Beech Mountain","https://www.beechmountainresort.com/mountain/conditions/"],["App Ski Mountain","https://www.appskimtn.com/snow-report"],["Wolf Ridge","https://skiwolfridgenc.com/snow-report/"],["Ober Mountain","https://obermountain.com/ski-report/"],["Wintergreen","https://www.wintergreenresort.com/the-mountain/mountain-report"],["Massanutten","https://www.massresort.com/snowsports/snow-report/"],["Bryce","https://www.bryceresort.com/winter/snow-report"],["Snowshoe","https://www.snowshoemtn.com/mountain-info/snow-report"],["Canaan Valley","https://canaanresort.com/ski/snow-report/"],["Timberline","https://www.timberlinemountain.com/snow-report/"],["Winterplace","https://www.winterplace.com/snow-report"],
 ["Killington","https://www.killington.com/the-mountain/conditions-weather/current-conditions-weather"],["Stowe","https://www.stowe.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Okemo","https://www.okemo.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Jay Peak","https://jaypeakresort.com/skiing-riding/snow-report"],["Mount Snow","https://www.mountsnow.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Sugarbush","https://www.sugarbush.com/mountain/conditions"],["Sugarloaf","https://www.sugarloaf.com/mountain-report"],["Sunday River","https://www.sundayriver.com/mountain-report"],["Loon Mountain","https://www.loonmtn.com/mountain-report"],["Bretton Woods","https://www.brettonwoods.com/snow-report"],["Hunter","https://www.huntermtn.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Whiteface","https://whiteface.com/mountain/conditions/"],["Seven Springs","https://www.7springs.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Camelback","https://www.skicamelback.com/mountain/snow-report"],
 ["Vail","https://www.vail.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Breckenridge","https://www.breckenridge.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Keystone","https://www.keystoneresort.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Aspen Snowmass","https://www.aspensnowmass.com/four-mountains/snow-report"],["Steamboat","https://www.steamboat.com/the-mountain/mountain-report"],["Winter Park","https://www.winterparkresort.com/the-mountain/mountain-report"],["Telluride","https://tellurideskiresort.com/snow-report/"],["Taos","https://www.skitaos.com/snow-report"],["Park City","https://www.parkcitymountain.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Snowbird","https://www.snowbird.com/the-mountain/mountain-report/"],["Alta","https://www.alta.com/conditions"],["Jackson Hole","https://www.jacksonhole.com/conditions"],["Big Sky","https://www.bigskyresort.com/the-mountain/mountain-report"],["Sun Valley","https://www.sunvalley.com/mountain-report"],
 ["Mammoth","https://www.mammothmountain.com/mountain-information/mountain-conditions"],["Palisades Tahoe","https://www.palisadestahoe.com/mountain-information/snow-and-weather-report"],["Heavenly","https://www.skiheavenly.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"],["Mt. Bachelor","https://www.mtbachelor.com/conditions-report"],["Crystal Mountain","https://www.crystalmountainresort.com/the-mountain/mountain-report-and-webcams/"]];
// --- the channel's reader (ski.js v153 parse), unchanged so both read the same way ---
const pair = (t, words) => { const W = `(?:${words})`;
  const pats = [new RegExp(`${W}\\s*(?:open)?\\s*:?\\s*(\\d{1,3})\\s*(?:\\/|of|out of)\\s*(\\d{1,3})`, "i"), new RegExp(`open\\s*${W}\\s*:?\\s*(\\d{1,3})\\s*(?:\\/|of|out of)\\s*(\\d{1,3})`, "i"), new RegExp(`(\\d{1,3})\\s*(?:\\/|of|out of)\\s*(\\d{1,3})\\s*(?:open\\s*)?${W}`, "i")];
  for (const re of pats) { const m = t.match(re); if (m && +m[2] > 0 && +m[2] <= 250 && +m[1] <= +m[2]) return [+m[1], +m[2]]; } return null; };
function parse(text) { const t = String(text || "").replace(/[”″]/g, '"').replace(/\s+/g, " "); const r = {}; const tr = pair(t, "trails|runs|slopes"), li = pair(t, "lifts|chairlifts");
  if (tr) r.trails = tr; if (li) r.lifts = li;
  const b = t.match(/base(?:\s*depth)?\s*:?\s*(\d{1,3})\s*(?:-|–|to)?\s*(\d{1,3})?\s*(?:"|in\b|inches)/i); if (b) r.base = b[2] ? `${b[1]}–${b[2]}"` : `${b[1]}"`;
  const n = t.match(/(?:24\s*h(?:ou)?rs?|last 24|new snow|overnight)\s*:?\s*(\d{1,2}(?:\.\d)?)\s*(?:"|in\b|inches)/i) || t.match(/(\d{1,2}(?:\.\d)?)\s*(?:"|in\b|inches)\s*(?:in the )?(?:last|past)?\s*24/i); if (n) r.new24 = +n[1];
  const op = t.match(/(?:opening day|projected opening|target(?:ed)? opening|scheduled to open|opens?)\s*(?:is|date)?\s*:?\s*((?:mon|tue|wed|thu|fri|sat|sun)[a-z]*,?\s*)?((?:nov|dec)[a-z]*\.?\s*\d{1,2})/i); if (op) r.opening = "Opening " + op[2].replace(/\.$/, "");
  if ((tr && tr[0] === 0) || (!tr && /(currently closed|closed for the season|see you (?:this|next) (?:winter|season)|opening day|projected opening)/i.test(t))) r.status = "closed";
  else if (tr && tr[0] > 0) r.status = "open";
  return r; }
(async () => {
  let old = {}; try { old = JSON.parse(fs.readFileSync(OUT, "utf8")); } catch (e) { try { const r = await fetch("https://chrisjustuswx2026.github.io/nbm-ranges/resorts.json?_=" + Date.now()); if (r.ok) old = await r.json(); } catch (e2) {} }
  const { chromium } = require("playwright"); const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1400, height: 1000 }, userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" });
  const out = { updated: new Date().toISOString(), resorts: {}, _missed: [] };
  for (const [name, url] of R) { let p = null;
    try { p = await ctx.newPage(); await p.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 }); await p.waitForTimeout(6000);
      const text = await Promise.race([p.evaluate(() => document.body.innerText), new Promise((_, j) => setTimeout(() => j(new Error("read timed out")), 15000))]);
      const r = parse(text);
      if (r.trails || r.status || r.base) { const o = { updated: new Date().toISOString(), url };
        if (r.status) o.open = r.status === "open"; if (r.trails) { o.trails_open = r.trails[0]; o.trails_total = r.trails[1]; } if (r.lifts) { o.lifts_open = r.lifts[0]; o.lifts_total = r.lifts[1]; }
        if (r.base) o.base = r.base; if (r.new24 != null) o.new24 = r.new24; if (r.opening) o.opening_text = r.opening.replace(/^Opening/, "Opens");
        out.resorts[name] = o; console.log("⛷ ", name, JSON.stringify(o)); }
      else { out._missed.push({ name, url, why: "no trail/lift numbers on the page" }); console.log("⛷ ✗", name, "no numbers —", url); }
    } catch (e) { out._missed.push({ name, url, why: e.message.split("\n")[0].slice(0, 120) }); console.log("⛷ ✗", name, e.message.split("\n")[0]); }
    try { if (p) await p.close(); } catch (e) {} }
  await browser.close();
  // keep a resort's last good report up to 48 hours if this run missed it
  for (const [k, v] of Object.entries((old && old.resorts) || {})) if (!out.resorts[k] && Date.parse(v.updated) > Date.now() - 48 * 3600e3) out.resorts[k] = v;
  fs.mkdirSync(path.dirname(OUT), { recursive: true }); fs.writeFileSync(OUT, JSON.stringify(out));
  console.log(`— ski reports: ${Object.keys(out.resorts).length}/${R.length} read —`);
})().catch(e => { console.log("ski reports failed:", e.message); process.exit(0); });
