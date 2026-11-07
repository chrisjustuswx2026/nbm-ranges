# SDR / CJWX dashboard — plan for next session (written v216, Nov 3 2026)

## Tools already built (run before every zip)
- lab/run.js — 15 briefing scenarios through the real code; prints every page; checks one page + banned phrases.
- lab/core.js — home screen on phone + desktop, quiet + storm day; errors, sideways scroll, empty cards, bad text, radar closed/open.
- lab/rb.sh — safe rebuild.

## 1. Fix first (found by the core check)
- What's Next can say "Storms nearby now" from the forecast while radar shows nothing within 60 miles. Only say "now/nearby" when radar actually has echoes nearby; otherwise use the forecast time ("Storms after 4 PM").

## 2. Push server for warnings (most important new build)
- Today alerts come from the open dashboard only; a closed app gets nothing.
- Build: Cloudflare Worker + Cron (every minute) checks official warnings for each client point; Web Push (VAPID keys as Cloudflare secrets) to subscribed phones (iPhone home-screen apps support it on iOS 16.4+).
- Dashboard: "Turn on alerts" subscribes the phone; test button sends a push to Chris only.
- Rules: warnings (tornado, severe t-storm, flash flood) immediate; one push per warning; all-clear when it ends; quiet hours never apply to warnings.

## 3. Full-app test, remaining corners
- Schedule Watch with an uploaded schedule (storm during an event), Map Room every card, Around You, rivers, Hunt & Fish full screen, chat (Athens / Dog Walk, other-city, no assumptions), CJWX mirror, print from iPhone.

## 4. Goodies (Chris is excited about these; sponsorable like Hunt & Fish)
- SKI CONDITIONS: nearby resorts (Cataloochee, Sugar, Beech, Appalachian, Wintergreen, Snowshoe…), 10 days: new snow, snow depth/base, fresh-powder alerts, feels-like at the summit, wind holds on lifts, snowmaking nights (temps/wet-bulb), a /10 "ski day" score, tap for hour-by-hour like Hunt & Fish.
- BEACH & BOATING: pick a beach (Myrtle, PCB, Charleston/Folly, Tybee, Destin, Siesta Key, Miami Beach, Outer Banks, Jersey Shore…), tides, wave height/period, rip current risk, water temp, wind/chop for boating, UV, lightning; /10 beach-day and boat-day scores. Lakes (Hartwell, Keowee, Jocassee, Lake Lure) for boating: wind/chop, water temp, lightning.

## Chat (Chris, Nov 4)
- Send a picture almost every reply when it helps: for games/outdoor work/events, an hour-by-hour GO / NO-GO strip for that day (green/yellow/red by hour with temp, rain, lightning, wind). Not the 7-day rain total unless asked.
- Admin/desk: AI suggests the reply AND the snippet/picture to send (review mode has drafts + suggested pictures today; make it one-tap "send this").
- Audience-aware tone (in v220 worker): coaches/ADs/crews get field, timing, lightning, go/no-go; fans/families get comfort tips.
