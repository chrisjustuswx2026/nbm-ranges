# SDR Weather Intelligence dashboard: change log

Version numbers match the published prototype. Live files: clemson-live.html, bay/bay-county-live.html.

## v163
- **Shorter Home (about a quarter less scrolling on a phone).** The 10-day shows 5 days with "SHOW ALL 10 DAYS"; day rows are tighter. Around You and Your Schedule are one bar each until tapped. With no schedule uploaded, the bar reads "UPLOAD YOUR SCHEDULE · Games, jobs, spray days, events. We'll tell you when weather will affect any of them."

## v179
- **10-day rows reorganized:** DAY · HIGH/LOW · ICON with the rain chance right under it · WHEN · WIND. Wet days: the timing strip with the likely total on its label ("⚡ AFTER 1 PM · 0.68\""). Dry days: the sky in plain words ("Sunny", "Partly Cloudy"). The far-right rain column and the dry-day temperature bars are gone.

## v178
- **ClearCall before anything is uploaded is a tucked pill:** "CLEARCALL · ONLY ON SDR · We watch your plans for weather · See how ›". Tap it and it drops down to the full pitch with the three examples and the UPLOAD YOUR SCHEDULE NOW button.

## v177
- **ClearCall closed pill tucked in:** one short row. "CLEARCALL · 6 EVENTS · All clear · we are watching every one", or with a yellow/red border and ⚠️ the time and name of the event that needs attention ("7 AM · Crews roll · mowing…").

## v176
- **ClearCall closed bar** shows its state: ✅ "All clear. We will tell you the moment that changes." or, with a yellow (or red) border, ⚠️ the event that needs attention by name and time ("Crews roll · mowing & landscaping · 7:00 AM needs attention", +N more).
- **ClearCall card reads like an ad:** "We make the call for you. Upload your personal or business schedule now…" with an UPLOAD YOUR SCHEDULE NOW button.

## v175
- **Tapping a warning (or outlook, storms-organizing area) on the radar** now opens a compact bubble with an arrow pointing at the spot you tapped, like the warnings-bell popup: colored title bar, the key lines ("Until 5:14 PM · 1h 30m left", counties, how it was detected), "More" for the full text, and a × that's always reachable. It stays clear of the zoom buttons and moves the map if needed. Multiple warnings at one spot keep the ‹ › arrows.

## v174
- **Tighter Home on phones:** smaller ALL CLEAR / HEADS UP word and What's Next headline; the radar is shorter (300 px, opened a half-step wider so the rings still show; tap it for full screen); the radar play button is a clean PLAY / STOP pill instead of the blue emoji box.
- **10-day:** shows 6 days, then "Show all 10 days". Dry days now show a **temperature bar** (where that day's low-to-high sits in the 10-day range, colored cool to warm); wet days keep the timing strip. Slimmer header.
- **Almanac:** **Today so far** sits beside **Normal for today** (normal high/low plus record high/low with the year), with today's high and low marked +/− vs normal. Yesterday is one line underneath.
- **Hunt & Fish:** fixed "5:noon–7:noon" (should read 5:12–7:12 PM); the note explains the feeding times (solunar: moon overhead or underfoot = major, moonrise or moonset = minor, estimated).

## v173
- **Daily briefing, every morning, automatically** (and pushed, even on a quiet day: "☀️ TODAY'S BRIEFING"). It replaces the separate 6:45 AM headline push. Contents:
  - the What's Next headline and sentence (on a quiet day: "Monday: Dry through the weekend · A quiet day for Greenville.")
  - Today, Tonight, Tomorrow in one line each
  - **Watching:** the biggest thing in the next 7 days (heavy rain, storms, a freeze, wind, heat, snow)
  - **Perspective:** one almanac line, the most useful one that day (a heat or freeze streak, "39 days since a 1-inch rain: hard ground, expect runoff", dry stretch, first-freeze timing, near-record, or vs normal)
  - **The picture that explains it:** severe outlook on a stormy day, rain totals map on a wet one, drought map in a dry spell, otherwise the pattern outlook or radar
  - the team's latest video when it's under 36 hours old, the timing banner and the bottom line
- Tagged "TODAY'S BRIEFING" (DAILY in the library). It doesn't take over the Home "New briefing" strip, which stays for real threats.

## v172
- **No more automatic "risk removed / threat is over" briefings.** A flooding or severe risk dropping off (often by a few miles) while heavy rain and lightning are still coming sent the wrong message. Downgrades to zero no longer create a briefing (the team can still post one), and any already saved on phones are cleared. Where a "none" message is unavoidable it now reads "Soaking rain still on the way" / "Storms still possible… lightning is still possible", never "normal plans are back on".

## v171
- **ClearCall**, our exclusive schedule feature, gets a real showcase on Home when nothing is uploaded yet: "ONLY ON SDR · Put it on the calendar. We will make the call.", a one-line pitch, three samples (Soccer practice · Clear, Soccer game · Storms 6–8 PM, Olivia’s 5th birthday · Tent it) and a big ADD YOUR SCHEDULE button. Once a schedule is in, it folds to one bar: "CLEARCALL · 6 EVENTS COVERED · 1 needs attention."

## v170
- **The chat knows the almanac and Hunt & Fish.** Every question now carries sunrise/sunset/daylight, moon phase, today's records and normals, yesterday's numbers, days since and streaks, freeze dates, rain this month/year vs normal, and today's deer movement, fishing and feeding times. Ask "when's sunset?", "what's the record high today?", "how long since a good soaking?", "when's the first freeze usually?", "are the deer moving tomorrow morning?" and it answers from the same numbers on the dashboard.
- **Smarter drafts.** The AI now thinks like the client's meteorologist before writing: it connects "39 days since a 1-inch rain" with heavy rain coming (hard ground, runoff first), a recent soaking with more rain (saturated, standing water), spray windows, field playability, freeze timing vs. normal, and writes for the kind of client it is (stadium, county, farm, city).
- **Forecast Desk:** each card now shows a 💡 perspective line for the meteorologist ("39 days since a 1-inch rain: hard ground, expect runoff the first hour").
- **Chat server (sdr-chat-worker.js)** updated to use these sections (feeding times called estimates; hunters reminded about legal shooting hours). Paste it into Cloudflare.

## v169
- **Almanac, now with perspective** (open the ALMANAC bar):
  - **Sun & moon**: sunrise, sunset, daylight (and minutes gained or lost vs yesterday), moon phase and % lit.
  - **Today in history**: record high, record low and record rain for today's date with the year each was set, plus today's normal high/low.
  - **Streaks & days since**: days since 0.10"+ rain, since a 1" soaking, since a freeze, since measurable snow (and since a 90° day in the warm season). Running streaks call themselves out: "10 days in a row at 90° or hotter", "4 freezing nights in a row", "14 dry days in a row".
  - **Freeze dates**: average first fall and last spring freeze (1991–2020), and this year's actual dates ("Nov 1, 6 days early").
- **HUNT & FISH** (its own bar under the almanac): **Deer movement** and **Fishing** rated Good / Fair / Slow with the reasons (pressure falling or rising, wind, a cold snap, the moon), first and last light, and major and minor feeding times from the moon's position. "Always check your state's legal shooting hours."

## v168
- **ALMANAC** (under the rain bucket, folded to one bar: "Yesterday 72° / 51° · rain 0.10" · gusts 18 mph"). Open it for:
  - **Today so far and Yesterday**: high, low, rain and peak wind.
  - **A month calendar**: each day shows its high/low, 💧 rain and ❄️ snow, tinted **red when it ran warmer than normal and blue when cooler** (deeper color = bigger difference). ‹ › to step back through earlier months. A summary line: "16 warmer and 11 cooler days than normal, 4.20" of rain."
  - **🧊 ice / sleet days** are marked too (from the nearest airport's hourly reports: freezing rain = "ice", ice pellets = "sleet"), and "❄️ flakes" when snow fell but didn't measure. The summary counts the ice days.
  - Official daily records from the nearest climate station; today's numbers come from the nearest weather station as they come in.

## v167
- **Rain bucket is now month · season · year** (what growers ask: how far behind are we). Each shows the total, how far above or below normal, and a fill bar with the % of normal. The last full day moved to the small note line. Seasons: winter Dec–Feb, spring Mar–May, summer Jun–Aug, fall Sep–Nov.

## v166
- **10-day rows, our own design:** on wet days the middle of the row is a **timing strip**, one small bar per hour (blue rain, amber thunder, white snow) with a short label ("AFTER 2 PM", "⚡ ALL DAY", "UNTIL 10 AM"), so you see *when* at a glance. The rain column shows the **likely total** under the chance (80% · 0.46"). Dry days stay clean. The colored edge still carries ALL CLEAR / HEADS UP / TAKE ACTION.
- **Warnings bell on the radar:** every active warning in the U.S., grouped Warnings / Long-fused warnings / Statements, with time left. Tap one and the radar flies there, outlines it and shows what it is and until when. The bell turns red with a count when warnings are near the site. Marine, freeze and frost warnings are left out.
- **Rain bucket** (under the 10-day): last full day, this month and this year from the nearest official weather station, each with how far above or below normal, plus a Drought Monitor thumbnail that opens the drought map.

## v165
- **Every bar in the day charts has its number, with the unit**: "10 mph", "50%", "0.3"" — wind, gusts, rain chance, thunder, snow and ice. Nothing to work out.

- **HEADS UP for rain is tighter** (so summer pop-ups don't nag): yellow only when it's raining at the site, rain is due within about 30 minutes (distance ÷ speed), or storms/heavy rain are within 15 miles. A shower 15 miles off that isn't arriving soon stays ALL CLEAR, and the line still says where it is and which way it's moving.
- **Chat:** the RIGHT NOW banner at the top no longer slides under the header (the chat page itself no longer scrolls; only the messages do).

## v164
- **New Home order (phones and tablets):** Right Now → What's Next → Your Schedule → Radar → Hour by hour → 10-day → Alerts Near You → Briefings → Map Room → Around You. Now, then your plans, then the next hours, the next days, then the deeper reading. The desktop layout is unchanged.

## v162
- **LIVE pill up top is the live-data light again**, always red and pulsing while the dashboard is live (it had gone gray when no one was on air).
- **The bottom LIVE tab is the on-air signal.** When channel.json says `"deskLive": true`, the whole LIVE tab flashes red with a red dot beside the icon so people tap it. Off air, it's a normal tab.

## v161
- **Briefing rain banner makes sense now.** It was "HEAVIEST RAIN · WED 6 PM – THU NOON · MOST LIKELY 7 PM – THU NOON" (the same window twice). Now: "RAIN · WED 6 PM – THU NOON · HEAVIEST 9 PM – THU 3 AM". The window is the one stretch of rain that starts that day; HEAVIEST is the 3–6 hours with the most rain falling (from the hourly amounts), and it only appears when it's a real part of the window.

## v160
- **RIGHT NOW looks in every direction, not just at the nearest rain.** If more (or heavier) rain is upstream, the line leads with it: "Heavier rain 15 miles southwest headed this way, lighter rain 5 miles northeast." Rain on its way makes it HEADS UP even when the nearest shower is drifting off.
- Includes everything in v159 (rain on radar = yellow, moving-away stays green, real sunrise/sunset and night icons, no stale hours).

## v159
- **Rain on radar turns the card yellow when it matters.** RIGHT NOW goes **HEADS UP** when real rain (clusters, not stray specks) is at the site ("Rain at your location now."), within 10 miles, or anywhere within 30 miles and headed this way ("Rain 15 miles north, headed your way at 25 mph."). Rain moving away stays **ALL CLEAR** ("Rain 20 miles north, moving away."). Goes back to green on its own; never overrides TAKE ACTION.
- Removed the station check for "rain here" (stations lagged and caused "Showers nearby, none falling here right now" while it was pouring). That sentence is gone.
- The weather icon switches to rain as soon as radar shows rain at the site or within 10 miles, without waiting for the weather stations.
- **No sun after sunset.** Day and night now follow the real sunrise and sunset at the site (it was a fixed 7 AM to 7 PM, wrong after the clocks changed). Partly cloudy at night shows a moon behind a cloud, in RIGHT NOW, hour by hour and the 10-day.
- **Hour by hour never shows hours that are over**, and the whole dashboard refreshes the moment the app comes back on screen (phones pause the 5-minute refresh while the app is in the background, so it could still say "NOW 4 PM" at 6).

## v158
- **Rivers card always shows up.** The whole-country river file is bigger and on phones often arrived after the Map Room was already built, so the card never appeared. Now the card is added the moment the river data lands, and refreshed every 15 minutes.

## v157
- **The chat can send any map in the Map Room**: severe outlook today / tomorrow / day 3 / days 4–8, flooding-rain risk days 1–3, rainfall 1–3 / 1–5 / 1–7 days, temperature and rain outlooks 6–10 / 8–14 day, drought, winter impacts, tropics, rivers, radar.
- **Automatic picks:** drought → drought map; tropics → tropics; flooding → today's (or that day's) flooding-rain risk plus rainfall 1–3 days; "rain this week" → rainfall 1–7 days plus the rain table; severe "next week / weekend" → days 4–8; "wetter / drier later" → 10-day plus the rain outlook.
- **Forecast Desk:** the pictures the AI picked are pre-ticked at the top with the four everyday ones; every other dashboard map is one tap away under "More maps from the dashboard".

## v156
- **Chat: "cool down / warm up / next week / pattern" questions** now send a **NEXT 10 DAYS · HIGHS AND LOWS** picture (one bar per day, coldest night and warmest day called out) plus the 6–10 or 8–14 day temperature outlook map from the Map Room.
- **Forecast Desk:** the attach boxes now include Day snapshot, 10-day highs & lows, Radar, Severe outlook, Rain this week, Rainfall map, Temperature outlook and Rain outlook. The AI pre-checks the ones it would send; the meteorologist just unticks or ticks and hits Send (up to 4).
- **Chat server:** suggests those same pictures with each draft.

## v155
- **RIGHT NOW lists everything happening, not just one thing.** When two or more things are in effect for the site right now (warnings, watches and advisories covering it, storms on radar within 20 miles, lightning), the line reads "4 alerts for your area right now. Tap any for details." and each one is listed, worst first. Tapping an alert opens its full text in Alerts Near You; storms go to the radar; The status word always matches the worst item (a warning is never under ALL CLEAR or HEADS UP). What's Next still covers what's coming.
- **Rivers tile:** moved to the end of the Map Room, unless a river near the site is in flood (then it's second). The tile shows gauges spread across the area with the site, flooding rivers big and labeled, and says the story in the title: "RIVERS · ALL IN THEIR BANKS", "RIVERS · 2 NEAR FLOOD STAGE" or "RIVERS · MODERATE FLOODING NEARBY".

## v154
- **Chat day picture is now a "WEDNESDAY SNAPSHOT"**: temperature, chance of rain (with thunder), and, when it's breezy, a WIND · GUSTS panel, all lined up hour by hour. On a wet day (40%+) a second picture follows with the rain totals (the rainfall map for the next 3 days, the week's rain table after that).

## v153
- **Rivers map is fast now**, like the sky cams: zoomed out it shows only rivers near or in flood (the spots that matter); zoom in and every gauge in view appears. Only what's on screen is drawn.

## v152
- **River view:** SDR Weather Intelligence logo in the top corner; a small source line at the bottom ("river levels and forecasts from U.S. government river gauges"); the NOW label moved to the bottom of its line so the river height never covers it.

## v151
- **Chat hour-by-hour picture redesigned**: two panels (temperature line, then CHANCE OF RAIN bars), the % written on the bars, "⚡ THUNDER" over the thunder hours, a summary line ("Rain chance up to 80% · thunder possible · gusts to 28").
- **Chat server**: answers are 1 to 3 sentences (under 50 words), answer first, no current temperature or wind unless asked.

## v150
- **Rivers: the whole country.** The data job now reads every river gauge in the lower 48 (was the Southeast only). The Map Room card still says what's near you; the map shows every gauge, small dots far away, bigger dots near the site or in flood.
- **Rivers map opens on your site**, zoomed in, not the whole country.
- **River names on the map** ("Reedy River · Greenville") when zoomed in, gauges in flood first, never piled on each other.
- **Tap a dot: a big river view** (nearly full screen on a computer, full width on a phone): right now, trend over 6 hours, flood stage and how far above or below, forecast crest and when, a large graph with flood bands, and "what happens at each level". Gauges outside the job's detail list load their graph live when tapped.
- The river rows under Alerts Near You open the same big view.

## v149
- **"Storms" means storms.** The radar only says storms for real storm cores (about 50 dBZ and up). Moderate rain is "Rain" or "Heavy rain" (fixes Asheville's "Storms at Asheville right now").
- **Hour by hour is cleaner.** Phones show 5 hours at a time (8 on tablets, 10 on desktop) with wider columns; swipe for more. The % sign is smaller so 70% 80% 90% don't run together.
- **Snow and ice.**
  - The snow and ice spread (low end / most likely / high end) shows whenever snow or ice is possible, not only when it's 0.1"+. Small amounts read "Under 0.1" · a dusting at most".
  - The snow chart is a **running total** through the day, with the day's total underneath.
  - New **ROADS** line on snow and ice days: wet roads, slick spots, snow-covered, or ice, colored by severity.
  - The "when" line on a snow day talks about snow, not "spotty showers". What's Next notes say "snow 70%", not "storms 70%".
- **Icons.** New snow, rain-and-snow, ice and thundersnow icons. Snow showers never show a rain icon. An hour with snow never shows a plain lightning icon.
- **Every warning is TAKE ACTION (red)**, including avalanche, winter storm, ice storm, blizzard, flood, high wind, heat, cold and red flag. Freeze, frost and marine warnings stay HEADS UP. The line says what to do for that warning (e.g. "Stay off and out from under steep, snow-covered slopes"), and no longer names the home county when viewing another place.
- **New briefing card stays on Home for 6 hours** after it's issued. After that it stays until the client has opened it.
- **What's Next puts now first.** Spotty showers in the next few hours (or rain on radar within 20 miles) lead: "Spotty showers until 2 PM", then the bigger event.
- **No more false "Rain falling here now."** The RIGHT NOW line only counts rain in real clusters on radar, not scattered specks (ground clutter around the radar site near Greer). "Rain falling here now" also needs a nearby station measuring it; otherwise it says "Showers nearby, none falling here right now."
- **rivers.py**: if the river data can't be fetched, it now leaves a small rivers.json saying why, instead of nothing (no more blank 404).
- **Chat: no person's name on an automated answer.** The opening status message and the built-in backup answers are now labeled "SDR Forecast Desk · automated answer" (they were showing a meteorologist's name).
- **Chat: severe-weather pictures fit the question.** "When will there be severe weather this week?" sends the hour-by-hour for the stormy day here (thunder chances shown), plus that day's outlook map only when a risk covers the site. No more today's national map when nothing is happening here.
- **Chat server (sdr-chat-worker.js):** asks one short question back when something's unclear ("Halloween was last night. Are you trick-or-treating tonight instead?"); knows the current local date and time; answers are never cut off mid-sentence; long web searches finish instead of stopping partway.
- **Noon and midnight.** Every "12 PM" reads "noon" and every "12 AM" reads "midnight". The heaviest-rain box names the next day when the window runs past midnight ("WED 6 PM – THU NOON").

## v148
- **RIGHT NOW is one sentence.** The place name next to RIGHT NOW is gone (it's already in the site picker), and the line under the status is one plain sentence:
  - "No rain within 30 miles." · "Rain 20 miles north, headed your way at 15 mph." · "Rain 15 miles west, moving away." · "Just a few sprinkles 21 miles north." · "Rain falling here now."
  - **Which way it's going**: the dashboard compares the rain now with a radar frame from about 15 minutes ago. It only says a direction when the rain is clearly moving (5–70 mph); otherwise it says nothing about motion.
- **"LIGHTNING · FEED NOT CONNECTED" is hidden** until the lightning feed is connected. Once it is, the line comes back on its own.
- The backup sentence (if radar can't be read) no longer repeats the place name: "No watches or warnings nearby."

## v147
- **Chat modes (channel.json → `chatMode`).**
  - `auto` — answers go out right away under **"SDR Forecast Desk · automated answer"**, never a person's name. (Tonight's test setting.)
  - `review` — the permanent setting: the client sees "A meteorologist has your question…", and the answer arrives under the meteorologist's name once they send it from the desk. Replies are checked every 8 seconds.
- **desk.html — the SDR Forecast Desk** (site/desk.html → /nbm-ranges/desk.html), password-protected. Each question is a card: the client, their event (from the schedule they uploaded on their dashboard, or a confirmed public event), **the issue in one line**, a **briefing** with the exact numbers (model/Blend chances by hour, temperatures, gusts, model agreement, outlook, radar, alerts — internal, so model and agency names are fine), the **draft** to edit, tick boxes to attach **radar / hour by hour / outlook / rain this week**, then **Send** (as the chosen meteorologist) or **Dismiss**. Refreshes every 8 seconds; the tab title shows how many are waiting.
- **server/sdr-chat-worker.js** updated for both modes. Review mode needs a KV namespace bound as `CHAT` and a `DESK_PASSWORD` secret; without them it stays in auto mode.
- The client's uploaded schedule now goes with each question, so the AI knows "their game is at 2 PM" without asking.

## v146
- **River levels.** New data step `rivers.py` (in the repo root, run by the workflow) writes `rivers.json`: every river gauge in the Southeast with its current and forecast flood category, and — for gauges within 60 miles of a client site or in flood anywhere — flood stages, the last 3 days observed, the forecast, the crest, and the published impact statements. It never fails the job.
  - **Map Room → RIVERS card** (right after Live Radar): gauges within 40 miles as dots — green in its banks, yellow near flood stage, orange minor, red moderate, purple major (the worse of now, the forecast, and the crest). Tap a dot: the river graph (observed solid, forecast dashed, flood-stage bands), "5.4 ft now · forecast to crest near 16.2 ft around 4 AM Mon · flood stage 12.0 ft", and the impact statement for that level ("At 14.0 ft: flooding of Cleveland Park…").
  - **Alerts Near You:** quiet on a normal day. A RIVER row appears when a gauge within 40 miles is near, in, or forecast into flood — or, when a flood watch or warning is out near the site, the nearest forecast gauges are listed even if they stay in their banks. Tap → the graph.
  - **Minor flooding stays quiet** (a row in Alerts Near You only). **Moderate or major** flooding, now or forecast, within 40 miles lifts ALL CLEAR to **HEADS UP**: "Reedy River at Greenville is forecast to reach moderate flooding, cresting near 16.2 ft around 4 AM Mon. Low roads and areas along the river flood first." Never overrides HEADS UP or TAKE ACTION from anything else (TAKE ACTION still comes only from warnings); steps back down by itself when the river does. River rows sort worst first.
  - **Tap a river row → the map opens zoomed to that gauge with its graph already showing.**
- The first prototype's sample chat drawer is removed from the live sites (it was parked off-screen; the CHAT tab opens the real chat).

## v145
- **AI chat replies (switch in channel.json → `aiChatUrl`).** When set to the SDR chat server's address, every client question goes to that server with the site's live dashboard data (right now, What's Next, alerts, radar, outlook maps, 10-day with rain ranges and model agreement, hour by hour) plus the conversation so far. The server writes the reply in the SDR voice under the same rules (no agency names, "model agreement", ALL CLEAR / HEADS UP / TAKE ACTION, never invent numbers), and can look up local context (a game time, an event) with at most two web searches. A matching chart still attaches. If the server is unreachable or slow (45 s), the built-in answers take over. Empty `aiChatUrl` = built-in answers only.
- **server/sdr-chat-worker.js**: the Cloudflare Worker. The Claude API key lives only there, as a secret. Only the SDR dashboards can call it, 40 questions per hour per address.
- Test phase: replies post automatically (testers know it's a test). Before paying clients, switch to drafts reviewed by a meteorologist.

## v144
- **On-air switch for the desk** (in `site/channel.json`): `"deskLive": true` while a meteorologist is on air, `false` when off. Optional `"deskNote"` shows a line while live ("Tracking storms west of Greenville."). Dashboards check every 2 minutes, no reload needed.
  - **Live:** the LIVE tab turns red with a flashing dot; the top LIVE pill pulses red; the LIVE page header reads LIVE NOW (red) with a red LIVE NOW bar and the note.
  - **Off:** LIVE tab and pill stay calm (gray); the LIVE page reads "No live coverage needed at this time. The 24/7 channel keeps rolling below."

## v143
- **No floating channel player over the radar on phones.** It covered the site and the rings — the spot clients look at. The channel lives in the LIVE tab (and beside the radar on desktop).
- **Chat fix — the opening "right now" message no longer sticks.** Before, any later question that didn't name a day ("Sunset?") got the right-now conditions back.
- **Sunset / sunrise** for the client's site: "Sunset tonight is 6:37 PM in Greenville County, SC. It's mostly dark about 25 minutes after that, and sunrise tomorrow is 6:49 AM."
- **Wind = the next 12 hours** with its own chart (solid wind, light gusts): "Next 12 hours: wind ENE 7 to 14 mph, gusts to 21 around 4 PM. It eases later — gusts under 14 by 11 PM."
- **Questions the dashboard can't answer get an honest hand-off** ("That's not something I have in front of me on your dashboard. Let me pass it to the team…") instead of a forecast.
- "This evening / this afternoon / this morning" = today. "Are we good?" answers for now first, then names the next thing to plan around.

## v142
- **New stream link:** youtube.com/live/0kJsmlz95V0.
- **The stream link lives in one file: `site/channel.json`.** All three dashboards read it. When the stream restarts and YouTube gives a new link, open `site/channel.json` on GitHub, paste the new link between the quotes, and Commit — no zip, no rebuild. A full share link (with ?feature=share) or just the 11-character ID both work. Never paste the stream key there.

## v141
- **Desktop channel panel, cleaned up.** The stream fills the panel edge to edge at true 16:9 (no black bars, no small picture floating in the middle). The OPS ROOM VIEW bar is gone; its OPEN button sits in the panel header. Alerts Near You tucks right under the video. The radar on the left stretches to line up with the right column on wide screens.

## v140
- **The 24/7 channel is connected.** The LIVE tab, the desktop channel panel and the phone mini player play the SDR YouTube Live stream (video NxVyl9W87Vg), muted until tapped. If a YouTube channel ID (starts with UC) is ever set in CHANNEL.youtubeChannelId, it takes over and follows whatever the channel is streaming, so a restarted stream never breaks the link.

## v139
- **Risk cards on the outlook maps.** Tapping a flooding-rain or severe-storm area opens a clean card instead of the blend numbers:
  - Header in white: "SLIGHT RISK · FLOODING RAIN", "ENHANCED RISK · SEVERE STORMS". Color lives only in the bubble and the level label, same as the model agreement row.
  - Level bubble like model agreement: flooding 4 segments (1 green, 2 yellow, 3 red, 4 magenta); severe 5 segments (1 green, 2 yellow, 3 orange, 4 red, 5 magenta). "LEVEL 2 OF 4" in the same color.
  - Three bullets: what the level means · When (the day, plus the hour window at the client's site when the site is inside the area) · What to do.
  - No blend rain numbers under flooding or severe areas (other maps keep them).
- **No agency names anywhere clients can see:** removed (WPC), (SPC), (CPC), "WPC total precipitation" → "Total rainfall", "CPC outlook" → "Pattern outlook", "WPC winter storm severity" → "Winter storm impacts", "SPC extended outlook" → "Extended outlook", "LIVE · NWS" → "LIVE", and the data-didn't-load messages.

## v138
- **The day-pill row under What's Next is gone** ("WED Storms 70%"). It repeated the headline, and because it rebuilt itself every few seconds it popped in and out, pushing the radar and the 10-day up and down and making buttons hard to hit. What's Next is now the headline, the sub-line and the short notes only.

## v137
- **The chat remembers the question it asked.** When the team asks "setup or the event itself?", "morning crew or afternoon?", "what time are you trying to be done by?" or "indoor backup?", the client's next message is the answer, and the reply goes straight to it — no new hello, no repeated chart. Examples:
  - "rain itself" → "For the rain itself: rain chances climb past 30% around 7 AM, peak near 80% 1 PM to 8 PM, and stay up into the night. Thunder risk 2 PM to 9 PM… About 1.24" in all."
  - "by 2 pm" → "Not really — rain moves in around 7 AM Wednesday, so you'd be working in it most of that window, and the heaviest starts at 1 PM. If it can move to another day, I would."
  - "it has to be outside" → "Then I'd get the outdoor part done before 7 AM Wednesday and avoid 1 PM to 8 PM — that's the heaviest. If there's lightning, people need somewhere to go…"
- **One hello per conversation, and never the same chart twice** in a thread (a new thread after 20 quiet minutes starts fresh).
- **Chat banner: word and color always match.** Line 1 is RIGHT NOW in its own color ("ALL CLEAR right now"); line 2 is What's Next with its own colored NEXT tag ("NEXT · Heavy rain Wed–Thu", yellow). They're never mixed into one line.

## v136
- **Terms of Use & Weather Disclaimer** page (terms.html in each site folder), from SDR's text, styled to match. Linked in Settings → Legal. Contact: chip@gosdr.com.
- Chat header says "Usually replies within 15 min" (the Terms say response times aren't guaranteed).
- Privacy Policy row stays hidden until a real privacy policy exists (the text sent Oct 30 is a product description, not a privacy policy).

## v135
- **Settings (gear in the top bar).** Client-facing name is SDR Weather Intelligence only.
  - Your site: the current site, Switch site, and Request a change (opens the chat with "I'd like to request a change to my site:" started). Clients don't move the site point themselves.
  - Alerts: notification status (turn on / blocked help) and separate switches for TAKE ACTION, HEADS UP (and back to All Clear), new briefings, and the morning / afternoon update. The alert sender honors them; tests always go through. A note appears if TAKE ACTION is switched off.
  - Sound: alert tones on/off. On phones the separate speaker button leaves the top bar (it lives here now), so the site name has room.
  - Support: Message the team. **Email support** appears once SUPPORT_EMAIL is set in block_settings.py.
  - **Privacy Policy / Terms of Use** rows appear once PRIVACY_URL / TERMS_URL are set — after legal review. Nothing with Chris's name or Justus Media Group shows before 2028.
  - Footer: SDR WEATHER INTELLIGENCE · Confidence in Chaos · version.

## v134
- **Desktop chat is a pop-up panel** docked on the right (440 px wide, between the top bar and the tab bar), with the dashboard still visible and usable beside it. Tap CHAT again or the back arrow to close it. Phones stay full screen.
- The chat header wraps onto two lines when the site name is long, so nothing gets cut off at any width.

## v133
**Day charts, cleaned up**
- **WIND and GUSTS are separate tiles with separate charts** ("WIND SPEED" and "WIND GUSTS", hour by hour, mph), on the same scale so they compare. Nothing is drawn on top of the bars anymore.
- **THUNDER tile always opens its chart** when any hour has a thunder chance (before, a 20% day with no single hour at 20% showed the tile but wouldn't open). The chart title carries the window: "THUNDER ⚡ 1–7 AM".
- **One lightning bolt.** The rain chart keeps a single "⚡ THUNDER 1–7 AM" in its title; the ⚡20% tag on every bar is gone.
- **Numbers on the bars:** the peak, plus every time the value steps up or down. Not every bar, not every 3 hours. Same rule for rain, thunder, wind, gusts, clouds.
**Percentages round to the nearest 10 everywhere** (40, 50, 60 — never 45 or 51): Around You city strips, the day calls, snow and ice chances, and the chat.
**Chat, smarter**
- Answers the actual question: start time, end time, how long, a part of the day ("Thursday morning"), cancel / postpone, concrete, spraying, painting, mowing, tarping, best day this week, freeze this week, severe or tornado threat in the next 3 days, model agreement for a day, and current temperature.
- Weekend answers in one sentence when both days match. "Tonight," not "today night."

## v132
- **Pictures match the day asked about.** The rainfall map only covers days 1–3, so it's sent only when the question is about today, tomorrow or the day after. For a day further out ("How much rain?" → Wednesday), the team sends that day's hour-by-hour plus the week's rain table with that day highlighted ("Rain by day · Wednesday is the wet one").

## v131
- **Tap a picture to enlarge it.** Opens full screen; pinch or double-tap to zoom, drag to look around, CLOSE or swipe back to return.
- **Pictures no longer shrink to thin lines** once a conversation gets long enough to scroll.
- **Thunder and lightning questions read the hour-by-hour.** "When will it lightning?" → the thunder window, the peak hour and percent, the next-best day, and what to do. "Lightning near us?" → right now, plus the next thunder chance.
- **"thunder" is no longer read as Thursday** (and "wedding" is not Wednesday). Only real day names count.
- **No repeats.** Ask about the same day again and the team goes a level deeper (when it starts, peaks and ends, thunder, gusts) instead of saying the same thing.
- **A new question stops the old answer** so replies don't interleave.
- **Close-out wording:** "Does that help answer your question? If so, tap Got it and we'll close out the thread for now. You can reach out any time." Got it button is bigger.
- **"in Greenville County"**, "at Memorial Stadium."
- **The + button is hidden** (it was the sample's fake photo). It comes back when real photo uploads are built.
- Week rain total no longer stacks every day's high end; it names the wettest day's high end instead. Table column reads CHANCE.

## v130
- **Chat banner always shows.** Opening CHAT right after the app launched (before the top card filled in) left the banner off for up to 30 seconds. It now shows the call word right away and refreshes at 1, 2.5 and 6 seconds, then every 15 seconds.

## v129
- **Test bar really gone.** The SAMPLE / DAY / AFTER HRS / RESET row was marked hidden but its style kept showing it. Fixed.
- **LIVE CHAT label stays** in the header when the venue name is added.
- **Real time stamp** on a new conversation (was a leftover "7:10 AM").

## v128
- **The bench talks like professionals.** Removed casual lines ("Give a shout," "You bet," "hang tight," "back in a sec," "Hey!"). Greetings are now Good morning / Good afternoon / Good evening / Hi. Same warmth, client-ready.

## v127 (Oct 30, 4:00 PM): one temperature rule, shared with the 24/7 channel · chat banner
- **The bench answers like a meteorologist would:** a rain question with no day named goes to the next rain ("How much rain?" → "Expect storms Sunday, 2 PM to 9 PM. Call it 0.45\", could be as little as 0.15\" or up near 1.20\"…" with Sunday's hourly attached). "When" questions lead with the timing. A follow-up without a day keeps the day you were talking about. Dry answers point to the next rain ("Rain doesn't show up until Sunday — 60%, around 0.45\", with storms"). "Holler" is gone.
- **Chat banner mirrors the dashboard:** the call word (green / yellow / red, same as RIGHT NOW) plus the What's Next headline and its line, banner colored like the What's Next card. Tap it to go back to the dashboard. Refreshes every 30 seconds.
- **The chat always loads the version that shipped with the page** (a phone could keep showing an old saved copy, which is why the SAMPLE bar was still there).
- **The bench only says a warning "covers" the site when RIGHT NOW says so.** A warning in a neighboring county reads "You're clear at Memorial Stadium, but there's a Severe Thunderstorm Warning nearby for Oconee, SC — I'm watching it."
- **Yellow** (What's Next and the 10-day row): low 25° or colder · wind chill 9° or colder · high 95°+ · heat index 105°+ · a 15°+ change in the high either way (What's Next only — "Much colder tomorrow · 80° to 62°").
- **A line, no color:** a 10–14° change · freeze 26–32° · frost 33–36°.
- Temperature never turns anything red and never touches RIGHT NOW. Heat at 100° no longer shows TAKE ACTION on a 10-day row.
- A swing never headlines when anything else is coming in the week (rain, storms, heat, freeze, wind) — it drops to the notes line. A one-day spike doesn't read as two events.

## v126 (Oct 30, 3:15 PM): What's Next — the main thing stays the main thing
- **Headline priority, locked:** snow, ice, severe and heavy rain lead alone whenever they're in the 10 days — a windy tomorrow or a cool-down never shares or steals the headline from them. Snow on day 9 still leads ("Snow next Saturday · 35% chance. Windy tomorrow first."). Winter and severe don't fade with distance the way rain chances do. "Storms" only when thunder is really in play.
- Notes are short and one line each: "TOMORROW cool-down 80° → 68° · gusts to 32", "TOMORROW NIGHT frost". No mph, no "possible".
- The headline stays the headline. Under the sub-sentence, up to three stacked lines (a fourth only for a freeze) carry the notes for the next 48 hours, in priority order, each only when it earns it and never repeating the headline's subject: a 10°+ swing in the high ("Cool-down tomorrow: 80° to 68°"), a freeze or frost night, gusts 30+, and rain or storms inside 48 hours when the headline is about something later. Grouped by day so the day is said once ("TOMORROW cool-down, 80° to 68° · gusts to 32 mph"); the day label turns yellow or red when the item warrants it, no icons. The sub-sentence hides itself when it only repeats the headline. Hidden when there's nothing to say. The hero and What's Next cards pulse softly when the call isn't ALL CLEAR (yellow slow, red faster); 10-day rows don't pulse. The call color does not change for a cool-down — a 68° dry day doesn't change what anyone does.

## v125 (Oct 30, 12:40 PM): rain chart reads like the others · chat screen
- **The chat bench sounds like people (test build).** Five meteorologists — Emma, Matthew, Lily, Miller, Anne — each with their own way of opening and closing; one picks up a thread and stays with it. Rhythm varies: sometimes a hello then the answer, sometimes the answer straight away, sometimes two short messages, sometimes the picture first. Phrase banks for every fact so no two answers read the same. Follow-up questions when the weather warrants ("Is this for the morning crew or the afternoon?"), close-outs that ask for Got it, sign-offs that sometimes close the thread. No sample labels anywhere on the client side; SAMPLE / DAY / AFTER HRS toggles removed from the client (admin side later). Chris will tell testers it's a test.
- **Emma v2:** attachments follow what was asked — "rain totals for the week" gets a 7-day table (chance · most likely · high end); "hourly for tomorrow" gets an hourly card (temperature line, rain bars, gusts); "severe outlook" gets the outlook map; radar questions get the radar. Week answers add up the totals. Weekend questions answer Saturday and Sunday together. More phrasing variety; the hello only mentions radar when you asked about radar. Header reads ● LIVE CHAT · Meteorologist team.
- **Emma, the sample meteorologist, answers for real.** Ask anything about the forecast and the reply is drafted from that site's live dashboard — the day you named, rain chance and amounts (middle half of the models), thunder window, wind and gusts, frost, heat, the severe outlook level, what's on radar right now, any warning in effect — in the team's voice, agreement in words, signed Emma · Meteorologist, with a "sample · drafted from your dashboard by the SDR assistant" note. She attaches pictures when they help: the severe-outlook or rainfall map from the Map Room, the live radar, and her own rain-by-hour chart for the day. Testers (Al, Lauren) can ask real questions now.
- **CHAT tab opens the client chat** (the iMessage-style "Message the team" build) as a full screen on every site, back arrow returns to the dashboard. It runs on sample data with its own SAMPLE / DAY / AFTER HRS bar until Andrew's desk server is wired (contract in the chat build's HANDOFF.md). It ships as chat.html beside each page so its styles can't collide with the dashboard.
- **Every bar labeled on phones** (computers every third hour, like temperature). The old rule skipped bars that matched the peak, which left a row of 50% bars blank.
- **Thunder rides with rain:** a bolt above any hour with a 20%+ thunder chance (yellow at 30%+), and the chart title says when — "RAIN CHANCE · ⚡ THUNDER 1–9 PM". Bars already turn yellow/orange at 30%+ thunder, so color and bolt agree.
- Hero: UV out; WBGT appears only at 82°+ (yellow) / 87°+ (red).

## v124 (Oct 30, 11:55 AM): Greenville County
- Full-screen radar bar sits below the phone's status bar again (a v122 rule had undone it); CLOSE is a bigger pill.
- Hourly header no longer says "wind mph". Wind row cells are a fixed two lines so Calm and "5 / ENE" line up.
- Day charts: band names (SLIGHT / CHANCE / LIKELY) live in a gutter past the last bar; they can't sit on a tag anymore.
- **New site: Greenville County, SC** at /greenville/. County-wide framing ("No watches or warnings for Greenville County"), Greer radar (KGSP), Upstate towns on Around You, and a schedule built for crews and events — "YOUR JOBS & EVENTS": mowing and landscaping, concrete pour, roofing, spray application, event setup, evening event. Clients can upload their own list the same way as the other sites.
- Hero subtitle keeps the state code upper: "Greenville County, SC", "Bay County, FL" (it read "Sc" / "Fl").
- Blend hours now survive the NWS hourly reload (they were being wiped when the NWS feed arrived after the tile).

## v123 (Oct 30, 10:40 AM): the hourly goes to day 10
- **Hourly strip past the NWS feed.** Days 7–10 now carry the Blend's own time steps (3-hourly to day 8, 6-hourly after) for temperature, dew point, wind, gusts, sky, rain chance and thunder. Hours between steps are filled by straight lines and marked as estimates; the strip header reads "BLEND · 3-HR" while you're in that stretch. Same source as the 10-day row above it, so the two agree by construction.
- Day charts and the day detail work on those days once there are 6 or more steps.
- **Data job (nbm_ranges.py):** pulls the step fields, writes them into each tile as `h` (times + arrays), writes `steps` and the real `spread` used this run into latest.json. The 18Z step doubles as the afternoon snapshot the 10-day rows already used. About 180 more GRIB messages per run; expect the job to take 5–10 minutes longer.
- **cameras.py:** rebuilds the camera list once a day (cache stamp), tolerant parsing for the 511 feeds, and plain status wording ("no key (FL511_KEY not set in GitHub Secrets)").

## v122 (Oct 30, 9:45 AM): the morning list
- **Hero, TV style:** icon · temp · FEELS LIKE · WIND · GUSTS in one row. Wind is "8 mph" with an arrow pointing the way it blows and the direction small beside it; GUSTS is its own labeled number (turns amber at 25, red at 35; "—" when there is no real gust). Calm at 0. mph after every number.
- **Clean radar.** Every reflectivity tile is scrubbed before it's drawn: nothing under about 18 dBZ (the pale blues — clutter, bugs, virga) and no lone speckles. The "light returns" line still reads the raw picture, so the words stay honest while the map stays clean. Velocity is untouched. (`?clean=0` is not a thing; if you ever want raw back, say so.)
- **Radar on Home is just the map on phones** — plaque, zoom, play button, one line under it. Computers keep the view buttons, overlays and the ⛶ on the home radar (there's room). Tap the map or the RADAR tab for full screen, which has the outlook-style bar: RADAR · view buttons · CLOSE. Alert chips and the overlay menu are there too.
- **Tabs:** HOME · RADAR · BRIEFING · CHAT · LIVE. CHAT opens the team chat (the floating pill is gone). Schedule and Maps live on Home.
- **Day detail:** the night sentence sits right under the day sentence and names its night ("Saturday night."). OUTDOOR WORK & FARMS is one row of verdict chips (Work · Spray · Soil · Water · Heat units) — tap the row for the tiles; remembered per device.
- **Pushes:** titles carry a color square — 🔴 TAKE ACTION · 🟡 HEADS UP · 🟢 ALL CLEAR · 📋 NEW BRIEFING — since iPhone won't color the banner itself. "SDR" no longer repeats (iPhone already shows the app name).
- Map viewer: the tap card sits above town labels; county-equivalents filtered from its labels too. Rain chart band names moved to the right edge, away from the first bar's tag.

## v121 (Oct 30, 12:50 AM): clean boxes, clean lines, fewer words
- **Closing a day leaves you where you were.** The row you closed stays put on screen (or comes back under the top bar if you'd scrolled past it) instead of the page jumping to whatever was below.
- **Hourly WIND label** is just WIND; the unit sits once in the panel header ("wind mph").
- **Page-width guard:** the page can never be wider than the screen, whatever a section inside tries to do — this is the real fix for the chart that looked like it bled on the desktop at high zoom.
- **First screen:** the 24/7 bar is gone (the LIVE pill and WATCH LIVE tab do that job). ALERTS moved behind a bell in the top bar — tap it for on/off and SEND A TEST; it opens itself once on first launch as an app so TURN ON is in view. Two boxes gone before the radar.
- **Under the radar:** the timestamp box and VECTOR MAP tag are gone (the plaque has the time). One line stays.
- **Map room:** small thumbnails, one caption each, no paragraph; ALL MAPS is a link in the header. **Alerts near you:** explainer sentence gone.
- **Day detail:** every number in its own box with one label; three columns on phones; model-disagreement line is one short sentence; rain-amount heading is "RAIN AMOUNT" with the spread as a quiet tag. Farm intro is one line.
- **Hourly strip:** 7 columns on phones so the midnight line sits in the gap, not through the degree sign; the tapped hour is one clean highlight column instead of jagged cell shading.
- **Full screen fixes:** CLOSE sits above the +/− (they drop below it); nothing hides under the phone's status bar in full-screen radar or Around You.
- **Around You:** the city card is a bottom sheet in full screen (it was rendering off-screen below the map, which looked like a dead tap); dots are bigger tap targets on phones.

## v120 (Oct 29, 11:00 PM): the app
- **Real app on the home screen.** Each site now has a manifest, the real SDR icon (white tile, SDR letters) and a service worker. Added from Safari → Share → Add to Home Screen, it opens full screen with no browser bar. Delete and re-add the icon after this upload — iPhone reads the icon and name only when the shortcut is made.
- **Notifications.** An ALERTS bar under the hero (shows in the home-screen app, or with ?alerts=1 in a browser). TURN ON asks the phone once; then it reads ALERTS ON · SEND A TEST. The test fires a real notification 8 seconds later — lock the phone and watch. Real triggers, while the app is open: the call changes from ALL CLEAR to HEADS UP or TAKE ACTION (and back to ALL CLEAR after a warning); a new briefing for the site; a morning (6:45–8:00) and afternoon (3:45–5:00) update with the What's Next headline. Titles are short: "SDR · TAKE ACTION", "SDR · NEW BRIEFING · SEVERE", "SDR · MORNING UPDATE". Tapping one opens the dashboard — a warning lands on the radar, a briefing on the Briefing tab.
- **Honest limit:** pushes arrive while the app is open or just backgrounded. Pushing with the app closed, or to other people's phones, needs a push service (next decision, not in this build).
- **Full-screen radar has a way out.** A big ✕ CLOSE pill top-right of the map, and the phone's back swipe closes it too.
- **A day closes when you tap its row again**, whichever column you tap, and a ▴ CLOSE bar sits at the bottom of the detail.

## v119 (Oct 29, 10:40 PM): the late-night round
- **Virga guard.** Light green returns alone no longer trip HEADS UP. Radar makes the call only when echoes are yellow or stronger (about 35 dBZ+) within 30 miles, or green echoes within 30 miles *and* a reporting site within 35 miles measured rain in the last hour (up to six nearest NWS stations, checked every 10 minutes). Green with nothing at the ground stays ALL CLEAR and reads "light radar returns 24 miles northeast, nothing measured at the ground" — under the hero and under the radar. When a site is reporting rain, the radar line names it.
- **The phone page was 597px wide, not 393.** The 24/7 bar under the hero refused to shrink, so Safari zoomed the whole site out to fit it — every number and label was about 28% smaller than designed. That's the "smidge small" you felt. Fixed; no separate type bump, because everything just got bigger. Look at it fresh before asking for more.
- **Top bar:** logo 34px on phones (was 26), 44px on computers; the rule under the bar runs edge to edge.
- **Radar plaque, TV style:** one plaque top-left of the map — small logo · pulsing dot · LIVE RADAR · frame time under it in orange. The title follows the view (RAIN · SNOW, LOCAL RADAR · KGSP, VELOCITY). The dot stops pulsing and the line says LAST FRAME when the picture is more than 12 minutes old. The old header row (second logo, LIVE badge) and the watermark logo are gone; the play/stop button stays bottom-right.
- **Mesoscale outline:** no "SEVERE STORMS FORMING" plaque (it covered too much map); the dashed box pulses softly instead. Tap it for the details as before.
- **A day opens clean.** No chart until you tap a tile; the chart then lands at 6 AM (today at now).
- **What's Next:** the chip row is gone. A chip appears only for a TAKE ACTION-level day the headline doesn't already name.
- **Cloud cover follows the sentence.** "Mostly sunny" on top means Mostly sunny on the tile, with the icon and percent to match. The hourly average is used only when the sentence says nothing about the sky.
- **Right Now wind says Calm** at 0 instead of "0 N · gusts 3"; gusts show only from 10.
- **Wind tile** in the day detail spans two columns on phones ("ENE 10-15 mph" no longer runs into GUSTS). "mph" sits under the WIND label in the hourly strip; a strip with no rain at all says "Dry through these hours" once instead of an empty row.
- **Wide-zoom labels are real cities** — no more "Anaconda-Deer Lodge County", "Greeley County" or towns outside the lower 48 on the outlook map or the national radar.
- Crawl label read "CLEMSON0" (the zero was the alert count); the count only shows when there is one.
- Supporting lines (farm intro, "No measurable rain expected") one step smaller than the forecast sentence.

## v118i (Oct 29, 8:05 PM): your last three notes
- **CLOUD COVER, not SKY.** The tile is a sun/cloud icon, the percent, and the word under it ("mostly sunny"). Nobody reads 30% as a rain chance now. The chart title says CLOUD COVER too.
- **Rain amount says which spread it is.** The heading reads "RAIN AMOUNT · middle half of the models" when the blend job publishes 25th–75th, or "full model spread" if it is still on 10th–90th. The page reads that from the job's meta.json, so it is never a guess.
- **Charts stay in their box.** A chart box now clips anything inside it, and a chart built for a wide window is rebuilt if the window shrinks (zoom in) or grows. Chart titles are bigger (20px, 18px on phones); on computers a day chart is capped at 820px wide and the day's stats run in one column so nothing bleeds.
- **Fewer outlook briefings.** A monthly/seasonal outlook only makes a briefing when its lean changes (wet → dry, warm → cool) or a week has passed, instead of every refresh.
- Page reads the blend job's `latest.json` (not meta.json — my slip) for the spread tag; a newer job can write `spread` and the page honors it.
- Radar credit reads "radar: NEXRAD/IEM · map: © OpenStreetMap contributors · OpenFreeMap" once the vector map is on (it was still naming the old base map).

## v118h (Oct 29, 7:40 PM): radar tap card
- **Tap card sits beside what you tapped** (right of it, else left, below, above, else next to the tap), picking the spot that covers the least of the shape. It was pinned top-right. Phones keep it across the top. Card is a little narrower on computers.
- **Overlays answer a tap.** With a severe outlook, rainfall or tropics overlay on, tapping inside it adds a card: "SEVERE OUTLOOK · DAY 3 — Level 2 of 5 · Slight: scattered severe storms possible…", plus our rule (level 2+ is HEADS UP; TAKE ACTION only with a warning or lightning). Days 4–8 explain the 15% / 30% bands; rainfall gives the inches for the band; tropics gives the formation chance or the cone. Any warning or watch under the same tap still comes first; the dots flip between them.
- Town labels keep clear of the 10-mile and 30-mile ring plaques (a city name was sitting on the lightning ring).

## v118g (Oct 29, 7:30 PM): clean-up sweep from the phone test
- **Live chat:** the floating pill says LIVE CHAT (not "MT"), and chat has its own section at the bottom of the Overview with an OPEN LIVE CHAT button.
- **Nothing bumps:** TONIGHT fits its column; calm wind reads "Calm" once (not "calm" over "CALM") in the 10-day rows and the hourly strip; wind numbers in rows are the top of the range, direction and gust under them.
- **Day charts on phones show 6 hours at a time**, big and bold, every hour labeled, swipe for the rest; today opens at now, other days open at 6 AM. Computers keep the whole day.
- **No stub charts:** a day only offers charts (and the ▸ arrows) when it really has hours — today needs 3, any other day needs 12. The last day of the hourly feed no longer shows a two-hour sliver.
- Radar: the loop button is ▶ / ■ (play / stop). Alert chips and the Map Overlay pull-down share one toolbar under the map. On phones the ⛶ leaves the header (the on-map "Tap to pan" button does that job). A small VECTOR MAP tag appears in the radar footer when the GPU basemap is the one on screen.
- Georgia DOT: 4,300 cameras thinned by screen spacing until you zoom in (all of them from zoom 12), so turning cameras on over Atlanta doesn't crawl.
- Phone top bar: smaller logo and LIVE pill so the site name isn't cut to "Me…".
- Phones: a slim **24/7 CHANNEL · WATCH ▸** bar sits right under the hero (the call stays first; the channel is one tap away). Computers keep the channel panel beside the radar.

## v118f (Oct 29, 6:20 PM): the five design flags
- Chat bubble is just the MT circle (it covered the right third of phone screens).
- WHAT'S NEXT lists the next days worth planning around under the story line: "SAT Storms 60% · Gusts 32", "THU Rain 40%" (up to three), or "Nothing to plan around".
- SKY in the opened day is an icon and a number ("☀ 30% cloud"), one line like the rest of the row.
- Computers: Precipitation gets an equal column beside Conditions (it was squeezed into a narrow one).
- Hourly strip: dry hours show nothing in the RAIN row instead of a row of dashes.
- Georgia DOT cameras are live (4,332); the "ok 0" was the once-a-day camera cache, not the key.

## v118e (Oct 29, 11:10 AM)
- Hour-by-hour reasons sit in boxed groups of five hours (6–10 AM · 11 AM–3 PM · 4–7 PM), tighter rows.
- Days beyond the hourly forecast (8–10 on the live site) get a **real call from the blend's day and night numbers**: "Likely a go · Daytime rain only 20% · Wind N 10, gusts 22 mph", "Rain chance 50%", "Hold · Rain 70% in the daytime". A two-block day / night bar replaces the hour bar, and the tile opens to a DAYTIME box (rain, storms, wind, high) and a NIGHT box (rain, low, rain amount range). Spray Window does the same. No more "Plan around it" with nothing behind it.

## v118d (Oct 29, 10:20 AM)
- Hour-by-hour reasons read **down, then over** (6, 7, 8 AM in the first column…), in plain words with units: "Gusts 16 mph", "Rain 40%", "Lightning 50%", "Nearly calm, drift risk".
- Outdoor Work and Spray Window now show on **every day**: days without hourly data (the hourly feed runs about a week out) get a verdict from the day's own numbers and say so when opened. A stormy day reads "Storms after 1pm" (it said "Cold").
- Tapping a day in the 10-day scrolls that day to the top of the screen.
- Wind charts: every labeled bar says mph ("7 mph"), not just the peak.

## v118c (Oct 29, 9:55 AM)
- Section is **OUTDOOR WORK & FARMS**. An opened tile bumps out to full width so every hour's reason reads in full (they were clipped to "G…" in the narrow tile); ✕ in the corner bumps it back.

## v118b (Oct 29, 9:30 AM): Chris's desktop review of v118
- Test ⚡ button gone from the top bar (the lightning engine and the `LTG.feed()` hook are untouched). Jump-chip row (RADAR · BRIEFINGS · MAPS …) gone; the bottom bar does that job.
- **Order (Overview):** Right Now → What's Next → new-briefing strip → Live Radar (+ the rolling channel on computers) → Hour by hour → 10-day → Briefings → Map Room → Alerts near you → Around You → Schedule.
- **Briefings** panel has tabs over the dated list: ALL · SEVERE · TROPICAL · OUTLOOKS · WINTER · GENERAL, so a missed seasonal or winter outlook is one tap away.
- **Around You is locked** (it never grabs your scroll on a phone or a mouse wheel on a computer). EXPAND in the header, or the "Tap to pan the map" button, opens it full screen with pan and zoom; ✕ / Esc closes.
- **Hourly strip:** the day divider at midnight is one continuous orange line (it was broken into pieces); time labels bolder and bigger (12.5px, 800, light); day names 12px orange. Small type bumped across the page: sub-labels 12px, section labels 13px, panel titles 18px.
- **Precipitation:** a dry day shows a plain **RAIN · Dry** stat (no more "Rain dry day and night"). Rain amount is one small RAIN AMOUNT label, then MOST LIKELY as the big number with LOW END / HIGH END smaller beside it.
- **Day charts:** soft gradient under the temperature line, calmer grid, bigger axis text.
- **FARM & OUTDOOR WORK** is its own clearly marked section (green rule, title, one line saying who it's for). New **OUTDOOR WORK** tile for mowing, concrete, roofing and crews (no rain, no lightning, gusts under 30, bearable temperatures) with its own hour bar. **Every tile opens to a deeper dive** (tap the tile): spray and outdoor work list every hour with the reason it's yellow or red ("2 PM · gusts 18", "4 PM · lightning 40%"); soil temp lists the week against the planting marks (50° corn, 55° pre-emergent, 65° warm-season seed); crop water lists each day's use vs rain in inches and the shortfall; heat units shows the season total vs normal and the next 7 days.
- Kept as is, on purpose: the day chart shows the whole day at once (it answers "when" at a glance; the hourly strip is where you scroll), and one graph per tap (temp, wind) rather than stacking them.

## v118 (Oct 29, 9 AM): the design pass, built as one piece
- **One type scale, everywhere.** Numbers people act on (highs, lows, wind, gusts, rain %, amounts) are one size: 28px on computers, 24px on phones, weight 800, white. Same number looks the same in Right Now, the 10-day rows, the opened day, the hourly strip and Farm & Ag. Section labels (CONDITIONS, PRECIPITATION, FARM & AG) one size, letter-spaced, muted; sub-labels (HIGH, LOW, SKY, RAIN) one size, bold. Chart headlines 16px display 800 white on every screen; "hour by hour" beside them hidden on phones. 10-day rows: the high, the rain % and the wind number are the big ones (direction and gust under the wind number; the full range shows in the opened day). Right Now: wind number big, direction small.
- **Hourly strip, new.** 8 hours visible on phones (10–12 on computers), swipe for more, orange day markers at midnight. TEMP / RAIN / WIND row names are buttons: tap one for a graph under the strip that scrolls with it; tap again or the ✕ to close. Only one graph open at a time. Tap an hour for its detail tiles (✕ closes). The 12H/24H/72H buttons are gone; the strip has every hour.
- **Charts, one design.** Every bar chart (rain, thunder, sky, snow, ice, wind) labels its value at the 3-hour marks like the temperature line, plus the peak tag ("GUSTS 32 MPH", "60%"); labels step aside near the peak so nothing overlaps. Rain keeps the SLIGHT / CHANCE / LIKELY bands.
- **Spray window:** hour marks under the bar (6a · 9a · noon · 3p · 6p · 8p; from the current hour on today). Verdict in words ("Go · 1–6pm · Light winds", "Maybe · …", "Hold"). Help text describes only what's on screen.
- **Page order (Overview):** Right Now → What's Next → Live Radar → Alerts near you → Briefings → Map Room → Around You → Hour by hour → 10-day → Schedule. Jump tiles follow. Computers: radar + channel, alerts, briefings + map room, around you, hour by hour, 10-day.
- **Around You, calmer:** the biggest towns only, spread out, title case; the name is part of the tap target. Legend is one small line; "Tap a town" goes away after the first tap (remembered). The band list under the map is one calm line: "ALL CLEAR in all 20 cities on screen" or "TAKE ACTION Savannah · HEADS UP Charlotte, Atlanta… · 14 of 20 towns all clear".
- **Radar header (live files):** one row on computers (logo · NATIONAL · RAIN · SNOW · LOCAL · VELOCITY · SITE · STATE · REGION · U.S. · ⛶); tidy stacked rows on phones. **LOOP / LATEST left the header**: one play/pause button on the map, bottom-right beside the time stamp. Default LATEST, remembered per device. **"Tap to pan the map" is itself the button** that opens full screen. Tap card top-right on phones too. Alerts chip row quieter.
- **24/7 channel:** a red "● LIVE" pill in the top bar, always on, one tap opens WATCH LIVE. Floating mini player (phones, bottom-right above the chat bubble) keeps playing while you scroll; tap to expand, ✕ closes it for the session. It appears only once the YouTube channel ID is set (it is still blank). Computers keep the channel panel beside the radar. Nothing sits above the hero.
- **Vector basemap (live files):** MapLibre GL + OpenFreeMap tiles (free, no key, OpenStreetMap data) drawn once on the GPU under the radar map: gray land, navy water, rivers, black state lines that thicken as you zoom, county lines from zoom 7, blue interstates with a dark edge, pale-yellow U.S./state highways. Radar, alerts, tracks, cameras, rings and the Map Room untouched. Town labels and interstate shields stay ours (title case, sized by city, our font), so no duplicate labels and no font downloads. **Fallback:** if the scripts or tiles don't load within 15 s, or nothing renders, the layer removes itself and the hand-built basemap (still in the file) stays. Once the vector layer is confirmed on screen, the hand-built terrain, lakes, rivers and roads stop drawing and stop downloading; county lines and shields stay on top. `?gl=0` turns it off, `?gl=1` forces it on. **Not yet tested with real tiles** (the build workspace can't reach the CDN or the tile server): the first real look is Chris's phone. The data job is unchanged for now; shed counties/roads/lakes only after the vector map is confirmed.
- Demo (dashboard.html) carries the same strips module as the live files now (it was a version behind on v115–v117).

## v117 (Oct 28, 11:15 PM)
- Rain amount is three labeled numbers in the same style as the conditions: **LOW END · MOST LIKELY · HIGH END** (Trace · 0.02" · 0.10"). No sentence, no "little or none". Low/high are the middle half of the models (25th/75th) once the v115 data job has run; the median is the most likely.

## v116 (Oct 28, 11:10 PM): phone test of v115
- **False HEADS UP (virga / speckle):** rain-on-radar now counts only real rain: green or stronger (about 20 dBZ+; the pale-blue drizzle/clutter colors are ignored) and at least 10 such pixels in a 2-mile block. Stray pixels can't trip the card.
- **Phones: the map no longer hijacks scrolling.** One finger scrolls the page; the map pans only in full screen (⛶). Small "Tap ⛶ to pan the map" hint on the map. Computers unchanged.
- **City labels at every zoom:** the biggest towns on screen always show (no population cutoff), small towns from zoom 8. Rural areas (west Texas, New Mexico) were blank before.
- **SITE button** goes straight to the 30-mile ring (it was failing silently).
- **Charts open under their own section:** HIGH / LOW / FEELS LIKE / SKY / WIND / GUSTS charts open right under CONDITIONS; RAIN / THUNDER / SNOW / ICE charts under PRECIPITATION.
- Still owed, in the design pass (DESIGN-PASS-HANDOFF.md): the hourly strip (6–8 hours visible, swipe, graph under it) replacing today's charts-in-the-day, and the typography system.

## v115 (Oct 28, 10:45 PM): second desktop test
- Tap card (warning details) always opens top-right; a new tap replaces it.
- LATEST radar frame comes from the radar cache (same source as the loop); the 1-km MRMS export was coming up blank on the live site. Rain-on-radar reads the same cache (zoom-7 tiles re-projected around the site), MRMS as fallback.
- Rain-on-radar tightened per Chris: scan 45 miles. Clear = ALL CLEAR with nothing said about rain. Inside 45: "Rain 38 miles to your southwest." Inside 30: HEADS UP "Rain within 30 miles: 22 miles to your southwest. Have the plan ready." Line under the radar: "Radar quiet within 45 miles".
- Radar quick views: SITE · STATE · REGION · U.S. buttons in the radar bar.
- Map Room's LIVE RADAR card now jumps to the live radar (U.S. view) instead of a static copy.
- Spray-window help no longer describes bars that aren't there.
- **Blend ranges are the middle half of the models now** (25th–75th percentile, in nbm_ranges.py) instead of 10th–90th, so a 40% day reads "Most models land between a trace and 0.6"" instead of "a trace to 2.54"". Falls back to 10/90 only if 25/75 are missing from a run. Model-agreement thresholds rescaled to match. Takes effect on the next data run after nbm_ranges.py is uploaded.

## v114 (Oct 28, 10:30 PM): rain on radar feeds the top card
- Until now the top card (ALL CLEAR / HEADS UP) read warnings, watches and the forecast only; it never looked at the radar picture. Now, every 2 minutes, the page reads the newest radar image for 60 miles around the site, finds the nearest echo, its direction and how heavy it is (green = rain, yellow/orange = heavy, red/purple = storms).
- Wording (ours):
  - clear: "Nothing on radar within 60 miles of Memorial Stadium"
  - in range: ALL CLEAR · "Light rain 38 miles southwest. Nothing near Memorial Stadium yet."
  - inside 30 miles: HEADS UP · "Rain 14 miles west of Memorial Stadium. Have the plan ready; we'll call it if it gets inside 10." / "Storms 18 miles west…, closing in."
  - at the site: HEADS UP · "Rain at Memorial Stadium right now."
  - TAKE ACTION stays reserved for warnings and lightning.
- The line under the radar says the same ("Rain 30 miles east"). If the radar image can't be read, the card falls back to the old warning-based wording.

## v113 (Oct 28, 10:15 PM): smoother loop
- Time stamp is just the day and time (no LATEST tag).
- Loop is the full hour again (12 frames, 5 minutes apart), ends on now, holds 2 seconds, repeats. Default stays LATEST (still).
- Smoothness: the loop doesn't start stepping until every frame's tiles have loaded (shows the newest picture while it waits), and the 2-minute refresh swaps in the new set only after it has fully loaded. No more stepping through half-downloaded frames.
- Two hours of loop needs a paid radar feed (the free cache keeps one hour); on the Xweather list.

## v112 (Oct 28, 10:10 PM): phone fixes from the first phone test
- Charts draw at phone width on phones, so WIND 8 / GUSTS 32 MPH and the hours are readable (they were desktop charts shrunk to a third). Phone axis labels every 6 hours.
- Radar legend row ("Storms organizing" box) removed.
- DOT cameras is the first choice in the MAP OVERLAY pull-down; the separate button is gone.
- Camera dots: shown from zoom 8 (was 9), thumb-sized on phones, and they grow as you zoom in (they were shrinking).
- Still to do in the design pass (tomorrow, with the new map): type sizes across the app after the front page, the alerts chip row, and an hourly strip that scrolls with a graph under it.

## v111 (Oct 28, 8:25 PM): outlook wording firms up with the odds
- Outlook briefings use a ladder, never "we favor" and never "our lean":
  - 33–40%: "We're leaning toward…" / "Better chance of…" / "The odds tilt toward…"
  - 40–50%: "A good chance of…" / "Pretty good chance of…"
  - 50–60%: "Expect…" / "Most likely,…" / "Look for…"
  - 60%+: "Plan on…" / "Count on…"
  Rotates within each rung so briefings don't open the same way twice. Normal-rain line follows the same rule ("Expect more than that" vs "Better chance of more than that").
- Timing lines (day detail, briefings) say when, not "we favor": "Rain most likely 2–6 PM · best chance 3–5 PM".

## v110 (Oct 28, 8:10 PM)
- SKY value ("Mostly cloudy · 80%") was bleeding into the WIND cell; it now wraps inside its own cell at a smaller size.
- Outlook briefings no longer say "We favor…" (BAM's phrasing). Ours: "The SDR Weather Intelligence Division is tracking a warmer pattern… Our lean is toward above-normal temperatures…" / "The lean is toward more than that."
- Confirmed: DOT cameras are still pictures (refresh every 1–2 min) in every state except Tennessee, which plays video.

## v109 (Oct 28, 8 PM): radar LOOP / LATEST, on-map time stamp, feels like, sky cover, snow / ice charts
- **Radar: LOOP or LATEST**, nothing else (RadarScope style). LATEST = newest picture only (one layer, fast) and is the default; LOOP builds the 45-minute loop. Choice remembered per device. The small pause button is gone.
- **On-map time stamp**, bottom-left, big: "WED 7:31 PM", with LATEST under it on the newest frame. Every mode (national, rain · snow, local, velocity).
- Chart headlines big, bold, white ("WIND & GUSTS", "TEMPERATURE & FEELS LIKE"); "hour by hour" small beside it (hidden on phones).
- Rain amount wording: "The models range from as little as a trace to as much as 1.68"" (Chris's line).
- **FEELS LIKE** in conditions when it differs from the high by 3°+ (daytime extreme), with a dashed line on the temperature chart and a "FEELS 42°" tag.
- **SKY** in conditions ("Mostly cloudy · 70%", daytime average) with a sky-cover chart (gold = sun, gray = cloud).
- **SNOW** and **ICE** charts (hourly inches) appear only on days that have them; the live page now pulls hourly ice accumulation from the NWS grid.
- Cameras: stills everywhere except Tennessee (video). Confirmed working live in NC / SC / GA / TN.

## v108 (Oct 28, 7:45 PM)
- Rain chart: SLIGHT / CHANCE / LIKELY bands on the y-axis (dashed lines at 20 / 40 / 60%), no legend. Charts a bit taller.
- The "when" line scales with the odds: 60%+ "Rain on and off all day", 40–50% "A chance of rain possible any time of day", under 40% "Spotty showers…". No more "on and off all day" on a 40% day.
- Rain amount says "Little or none" when the most likely is nothing (instead of 0" next to "as much as 1.68"").
- MODEL AGREEMENT sits right under the rain amount (it's about the rain), not below Farm & Ag.

## v107 (Oct 28, 7:40 PM): cameras, first live test
- Cameras tap and load on the live site (v100's fix worked).
- North Carolina's stream addresses sit behind an NCDOT login, so the video attempt popped a sign-in box before falling back to the still. Video is now tried only for public streams (Tennessee); every 511 state is stills only. cameras.py no longer carries stream addresses for the 511 states.
- Camera card shows the nearest town under the road: "I-26 Eastbound · near Asheville".

## v106 (Oct 28, 7:35 PM)
- Chart labels in the display font, bold, uppercase: "GUSTS 32 MPH" above the peak, "WIND 8" on the solid bar. No legends under the charts; the labels on the chart do the explaining.

## v105 (Oct 28, 7:30 PM)
- Today's charts run from NOW to 11 PM (the hourly forecast starts at the current hour; past hours aren't forecast), so the chart fills the box instead of a sliver on the right. Other days stay midnight to 11 PM.
- Wind chart shows both: solid bar = sustained wind, faded cap above it = gust. Peak gust tagged. Title "WIND & GUSTS".

## v104 (Oct 28, 7:20 PM)
- Opened day order: CONDITIONS, then PRECIPITATION, then the chart (opens right under the numbers you tapped, above Farm & Ag), then Farm & Ag, then MODEL AGREEMENT. Before this the chart opened above the numbers, off the top of a phone screen, which read as "tapping does nothing."

## v103 (Oct 28, 7:10 PM)
- Tapping HIGH / LOW / WIND / GUSTS on **today** did nothing: the hourly forecast starts at the current hour, so today had too few hours for a chart. Now any day with 3+ hours charts what's left of it.
- MODEL AGREEMENT moved to the bottom of the opened day.
- Wind number no longer spans two columns on phones.

## v102 (Oct 28, 7:15 PM): charts readable, amount is one line
- Rain amount: the slider is gone. One line: RAIN AMOUNT **0.45"** · as little as 0.15" · as much as 1.20" (Chris's range wording).
- Charts: time axis every 3 hours in bold white (12 AM, 3 AM … 9 PM) with faint hour lines. Temperature line thick gold with a soft fill, a temperature printed at every 3-hour mark, and a dot on the high. Wind-gust chart (the one Chris liked best) unchanged apart from the axis.
- Wind number no longer runs into the gusts number.

## v101 (Oct 28, 7 PM): day detail, cleaner and tappable
- RAIN · DAY / RAIN · NIGHT gone (which night? too confusing). One **RAIN** number, then **when**: "Rain most likely 2–6 PM · best chance 3–5 PM" from the hourly forecast. That answers the "40% but when?" problem.
- Numbers in an opened day are bigger and bolder. UV moved to the end of the conditions row (it was wrongly put third in v96).
- **Tap a number for its hour-by-hour chart**: HIGH / LOW → temperature line with the high and low tagged; WIND / GUSTS → gust bars with the peak tagged; RAIN → rain-chance bars (storm hours in gold); THUNDER → thunder bars. Closed until tapped (the v92–95 lesson); ✕ closes. Tapping rain / temp / wind in a collapsed day row opens that day on that chart. Days 8–10 have no hourly data, so no charts there.
- Demo (dashboard.html) carries the same change.

## v100 (Oct 28, 6:45 PM): first live test of v99, fixes
- Radar time stamp shows the day: "WED 6:31 PM" (national loop and RAIN · SNOW).
- **Watches are one box** when zoomed out (the outline around all the counties, TV style); the counties show at zoom 8+.
- **Storms-organizing card** rewritten: titled STORMS ORGANIZING (no agency name, no number); shows the threats (tornadoes / damaging wind / large hail…), the timing window, and the watch outlook in words (likely soon / possible / not expected right now) rather than a percentage, per the locked rule. Towns inside and a "Full text" link stay. Legend and "NEW" pop-up say "Storms organizing" too.
- "NEW tornado warning / watch / storms organizing" pop-ups only for alerts within ~300 miles of the client; far-away ones still draw on the map, quietly.
- Tap card (warning / watch details) now always sits in the corner of the map away from the storm, never on top of it. It's still draggable.
- DOT camera dots moved to the top of the stack with their own click handler (they were under other map layers on the live site and couldn't be tapped).
- Smoother radar: loop frames you can't see are no longer painted, terrain at standard detail everywhere, loop is 10 frames (45 min) instead of 12.

## v99 (Oct 28, 6 PM): map look closer to WeatherFront, RAIN · SNOW loops
- **City labels:** title case (Greenville, not GREENVILLE), Helvetica-style bold white with a black halo, centered on the town, no dots; three sizes (metro 19px, big city 16px, town 13.5px).
- **Lakes** dark navy (#2A3052) instead of blue; rivers blue. **Interstates** blue (#4A8BE8) with a dark edge; **US / state highways** thin pale yellow. **County lines** get a soft light bevel under a dark line; **state lines** thicken as you zoom in (1.2 → 1.8 → 2.6).
- **RAIN · SNOW loops** (last hour, ~6-minute steps) using the frame times the government service publishes; LOOP / PAUSE work in that mode too. If the service doesn't list its times from the browser, it shows the latest picture only, as in v97. Not verifiable from here; check on the live site.
- Keys: NC / GA / FL / LA via each 511 site's developer page (secrets DRIVENC_KEY, GA511_KEY, FL511_KEY, LA511_KEY); Tennessee via the SmartWay site's own ApiKey (TDOT_KEY).

## v98 (Oct 28, 5:30 PM): live video in the camera card
- Where a state streams its cameras (Tennessee: all 667; NC / GA / FL / LA 511 feeds: most; SC: where offered), the camera card plays **live video** instead of a picture that refreshes every minute or two, so rain, snow and traffic actually move. Red "Live video" dot in the card. Safari/iPhone play it natively; other browsers load a small player (hls.js) only when a video camera is opened. If a stream won't play, the card drops back to the still picture on its own.
- Kentucky stays stills (no streams published).
- Permission: Chris's call, these are public government feeds used by EMA and city leaders for decisions; no consent emails needed.

## v97 (Oct 28, 10 AM): rain · snow · ice radar, and DOT cameras
- **RAIN · SNOW button on the radar** (next to NATIONAL / LOCAL / VELOCITY): the government's live precipitation-type mosaic (same source radar.weather.gov uses, updates every 2 min). Rain in greens and yellows, snow in blues, hail in pink, with a small key under the map. Latest picture only (no loop). If that service is down it falls back to the HRRR model's precipitation type from Iowa State (hourly; that one also shows freezing rain and sleet). Not yet seen on live data from here; check it the first snowy day.
- **DOT CAMERAS button** under the map overlay: camera dots at zoom 9+ for the area on screen; tap one for the live picture (refreshes every minute while open). Off by default, remembered per device.
  - The GitHub job (cameras.py, once a day) builds the camera list: **Kentucky** works with no key; **North Carolina, Georgia, Louisiana** need a free developer key each (DriveNC, 511GA, 511LA), stored in GitHub Secrets as DRIVENC_KEY, GA511_KEY, LA511_KEY.
  - Not included on purpose: **Florida** (FL511's terms exclude commercial use; needs written FDOT consent), **South Carolina / Virginia** (no documented feed; SC looks keyless but has to be captured from the site, then ask SCDOT), **Alabama / Tennessee / Mississippi** (streaming only, no public feed).
  - A paid aggregator (Road511, from about $29/mo) could fill the gaps later, but it's re-serving DOT pictures and says nothing about rights.

## v96 (Oct 28, midnight): clearer day details
- Precipitation chances are labeled like the conditions: RAIN · DAY 60% · RAIN · NIGHT 30% · THUNDER 50% (thunder, snow, ice only when they matter).
- Conditions: humidity removed (doesn't change operations). Two clean rows: HIGH · LOW · UV, then WIND · GUSTS · DEW POINT.
- Open question (Saturday trick-or-treat): a 40% day needs a simple answer to "when?". To decide when rested; not the v92–v95 charts.

## Back to v91 (Oct 28, 12:15 AM)
- v92–v95 (per-day timing lines and hour-by-hour charts) were rolled back: too busy for the clean look. The hourly section already shows timing. Live files and the demo are v91 again. The v95 files are kept in attic/ in case any piece is wanted later.

## v95 (Oct 28, 12:15 AM): charts only when you tap a product
- Opening a day shows the short timing lines only; no chart.
- Tap a product to see it hour by hour: the rain chance line or the storm/rain timing line → rain chart; WIND, GUSTS or the wind line → gust chart (shows when it ramps up); HIGH, LOW or a temperature line → temperature chart. A small blue ▸ marks what's tappable. Tap again or ✕ to close. One chart at a time.
- Tapping the rain %, wind or temps in the 10-day row opens the day straight to that chart.
- The tab row from v94 is gone.

## v94 (Oct 28, midnight): the day opens on an hour-by-hour chart
- Rain timing shows for any chance at all (10%+), so if we mention rain, the timing is there.
- Opening a day shows the timing lines plus an hour-by-hour chart, open by default, with tabs: RAIN · TEMP · WIND (+ STORMS when thunder is in play).
  - Rain: lit bars by chance (Slight / Chance / Likely, orange for storms), peak % labeled.
  - Temp: the temperature line with the high and low.
  - Wind: gust bars (Breezy 15+, Windy 25+, Strong 35+), peak labeled.
  - Storms: chance of thunder by hour.
- Tapping the rain %, the temperatures or the wind in a day row opens that day on that tab.
- The thin rain strip is gone (the chart replaces it).

## v93 (Oct 27, 11:45 PM): clearer rain timing + "See the day" chart
- Rain timing now shows on any day with a real chance (daily 30%+ or any hour 20%+), so a 40% "spotty showers" day gets it too: "Spotty showers possible · most likely 2–6 PM · peak 30% around 3 PM".
- The 24-hour bar uses clear steps instead of a faint fade, with a small key: Slight (20–39%) · Chance (40–59%) · Likely (60%+) · Storms (orange).
- **See the day ▸** (closed until tapped): one simple chart with the temperature line (high and low marked) and rain-chance bars, the peak % labeled. Wind stays in words, not on the chart.

## v92 (Oct 27, 11:30 PM): "what changes & when" inside each day
- Opening a day shows a small box at the top, only when something stands out (days 1–7, where hourly data exists):
  - **Rain / storm timing:** one plain line ("Mainly after 8 PM · heaviest 10 PM–2 AM", "Showers early, dry by noon", "On and off all day") plus a 24-hour bar (blue rain, yellow storms). Tap the bar to jump to that day in the hourly.
  - **Wind ramping up:** "Picks up after 3 PM · gusts to 35 mph, easing by 11 PM" (gusts 25+ and at least 12 mph above the morning).
  - **Odd temperatures:** "Falling fast: 72° at noon, 58° by 5 PM" (a 10°+ afternoon drop) or "Rising overnight: 52° at 6 PM, near 60° by 2 AM".
- Quiet days show nothing new.

## v91 (Oct 27, 10:30 PM): TV-style map labels
- Every map label (briefings, Map Room cards, full-screen maps) follows the TV rule: big bold uppercase top line ("SEVERE OUTLOOK · TOMORROW"), smaller uppercase second line (the date), bigger SDR Weather Intelligence logo.
- Demo's Live Radar card shows the lower 48 like the live files.

## VERSION 1.1 (Oct 27, 2026, 10 PM) = v90: phone fixes from the first real test
- **Radar on phones:** the header wraps so full screen and loop are always reachable; the map is taller (62% of the screen); full screen truly fills the screen; bigger +/− buttons; the alert card is a bottom sheet instead of covering the map.
- **Smoother on phones:** standard terrain detail on phones and tablets (the sharp 2× version stays on computers). Less work for the phone, same clean look.
- **Map overlay is one pull-down** ("Map overlay: None ▾" → Severe storms today/tomorrow/day 3/days 4–8, Rainfall today … next 7 days, Tropics) instead of a wall of buttons. Overlay notes no longer name agencies. The alert chip "SPC DISCUSSIONS" is now "STORMS ORGANIZING".
- **Our logo on every map:** every Map Room card and the full-screen map carry the SDR Weather Intelligence logo with what the map is ("Flooding rain risk · Today"), same frosted label as the briefings.
- Full-screen Map Room on phones opens on the region (the whole U.S. is too small to read there; U.S. is one tap away) and the header buttons wrap.

## VERSION 1 (Oct 27, 2026) = v89. Packaged for Andrew with HANDOFF-ANDREW.md (Version 1) and CHAT-HANDOFF.md.

## v89 (Oct 27, 5:30 PM): Map Room fits the screen
- The Maps tab grid was overflowing the screen (the first map stretched wide and pushed the second off the edge, so maps looked cut off). Two even columns now, every map fully visible.
- Live Radar card shows the whole lower 48 too, and opens on the U.S. (REGION zooms in).

## v88 (Oct 27, 5:30 PM): outlook briefings say what changed
- A new 6–10 / 8–14 day outlook writes a new briefing whenever the odds move 10% or more, and says so up front:
  - Higher: "Even higher odds of warmer and wetter days ahead" / "Odds climb for a wetter stretch". Intro: "The new outlook shows even higher odds of wetter than normal weather." Bullet: "What's changed: even higher odds of above-normal rain (now 60%, up from 50%)."
  - Lower: "Odds ease for a wetter stretch", "lower odds of above-normal rain (now 40%, down from 50%)".
  - Flip: "Pattern flip: now leaning cooler".
- Replaces v87's "only re-brief on a flip or leaning→strong"; a change is news, so we say it.
- Grammar fix: "Damaging wind gusts are possible" (was "is").

## v87 (Oct 27, 5:15 PM): map rules, storms-forming label, full-country Map Room, briefings that don't repeat
- **Map rules:** highways and interstate shields now sit above county lines. Interstates bolder (2 px, half see-through), U.S. routes a bit bolder, county lines bolder (1.35 px). State lines and terrain unchanged.
- **Storms forming:** the label is a small box off to the side of the area with an arrow pointing at it, reading "SEVERE STORMS FORMING", instead of a banner across the area.
- **Map Room:** every outlook map shows the whole lower 48 (nothing cut off). Opening one starts on the U.S.; REGION zooms to the client's area. The radar card stays on the region.
- **Briefings never read the same twice:**
  - Headlines, sub-headline endings and closing paragraphs rotate through several wordings by day and topic, and never reuse the last one for that topic.
  - The 6–10 / 8–14 day outlook only writes a new briefing when the lean flips or moves between "leaning" (40–50%) and "strong" (60%+), not every 10% wiggle. That's why Oct 26 and Oct 27 had the same pattern briefing.
- Local radar shows the latest scan only (no loop); the loop is on NATIONAL. Unchanged.

## v86 (Oct 27, 5 PM): TV-style headlines
- Headline = the threat + when, conversational, then the level: "Severe storms possible tomorrow afternoon: Level 2 risk", "Flooding rain possible tonight: Level 2 risk", "Downpours could flood low spots tonight: Level 1 risk".
  - Severe: A few strong storms possible (1) · Severe storms possible (2) · Severe storms likely (3) · Dangerous storms likely (4) · Major severe weather outbreak (5).
  - Flooding rain: Downpours could flood low spots (1) · Flooding rain possible (2) · Flash flooding likely (3) · Dangerous flooding (4).
  - Storms organizing: "Storms could turn severe this afternoon" (watch unlikely) / "Severe storms organizing nearby: watch likely soon".
  - When, in words: this afternoon / this evening / tonight / tomorrow afternoon / Saturday evening.
- Sub-headline: "Level 2 of 5, up from 1. Most likely 3 to 7 PM. Damaging wind gusts and lightning are the main concerns. Not everyone gets a storm."

## v85 (Oct 27, 5 PM): threat-first headlines, farmer-proof crop water
- Headlines lead with the threat and the window, then the level: "Flood threat tonight, 10 PM–3 AM · Level 1 of 4". The sub starts with "Raised from level 1." when it changed.
  - Flooding rain: "Flood threat tonight, 10 PM–3 AM" (1) → "Flash flooding possible…" (2) → "Flash flooding likely…" (3) → "Dangerous flash flooding…" (4).
  - Severe: "Strong storm threat" (1) → "Severe storm threat" (2) → "Severe storms likely" (3) → "Dangerous severe storms likely" (4) → "Major severe weather outbreak" (5).
  - Sub example: "Low roads, creeks and poor drainage flood first under the heaviest rain. About 0.57", up to 1.45"."
- Crop water is a verdict, no math: green "Covered" (rain this week covers what crops need), yellow "Partly covered" (rain covers part of it; add about 0.3" of water this week), red "Water needed" (crops need about 0.7" of water this week). No percentages. Tap ⓘ for how it's figured.

## v84 (Oct 27, 5 PM): slimmer Farm & Ag
- Tiles are tighter: less padding, one short line each, thinner spray-hour bar. Same four tiles, same green/yellow/red spray bar, tap (ⓘ) for the explanation.
- Crop water: "This week · rain covers it" / "covers ~80%" / "irrigate". Heat units: "5% ahead of normal".

## v83 (Oct 27, 5 PM): headlines that get people to look and act
- **Headline = what's happening + when, in plain words.** Strength scales with the level:
  - Severe: "Isolated strong storms possible" (1) → "Severe storms possible" (2) → "Severe storms likely" (3) → "Dangerous severe storms likely" (4) → "Major severe weather outbreak expected" (5), plus the day and the window: "Severe storms possible tomorrow, 3–7 PM".
  - Flooding rain: "Heavy downpours" (1) → "Heavy rain could cause flooding" (2) → "Flash flooding likely" (3) → "Dangerous flash flooding expected" (4): "Heavy downpours tonight, mainly 10 PM–3 AM".
  - Removed: "Storm threat is over for Saturday" / "Flood threat is over for Saturday".
  - Heat: "Dangerous heat Thursday, heat index near 106°". Freeze: "Hard freeze Saturday night, low near 26°". Frost and wind carry their number too.
- **Sub-headline carries what didn't fit:** the level (and raised / lowered), the main concern, what to do, the amount. Never repeats the headline.
  - "Threat raised to level 2 of 5. Damaging wind gusts and lightning are the main concerns. Not everyone gets a storm."
  - "Level 1 of 4 flooding risk. Most spots handle it; low roads and creeks are the concern. About 0.57", up to 1.45"."
- Regional headlines say "in the region" (no more "across the Southeast").
- Storms-organizing headlines (v82) unchanged.

## v82 (Oct 26, midnight): "storms organizing" briefings, the team's way
- Triggers when a storms-organizing area (the government's mesoscale discussion) covers the site **or comes within 25 miles**.
- Reads the discussion itself for the watch odds, the hazards (tornado, damaging wind, hail, flash flooding, winter) and the valid window.
- **Never names the product and never quotes the percent.**
  - Watch likely (50%+): "Storms organizing: a watch is likely soon."
  - Watch unlikely (under 50%): keeps the urgency. "Strong storms possible 4–6 PM. A watch is unlikely, but a tornado or two and damaging wind gusts are still possible in the Clemson area between 4 and 6 PM. Be ready to move people indoors quickly." Adds "Tornado: isolated, but possible. Know where you'd shelter." when tornadoes are mentioned.
  - Bullets: What we're watching · When · Next.
- Map banner: WATCH LIKELY SOON / STRONG STORMS STILL POSSIBLE.
- Radar, Map Room and legends now say "Storms organizing · area we're watching" instead of "SPC is watching · MD #".
- Severe outlook issued / raised / lowered / removed (days 1–3) still triggers its own briefing, as before.

## v81 (Oct 26, 11:45 PM): Farm & Ag explains itself
- Tap any Farm & Ag tile (ⓘ) for a one-line plain explanation of what it is and why it matters.
- Spray window gets an hour-by-hour bar (green good, yellow borderline, red no) with the start and end hours.
- Plainer lines: "Short window, plan carefully", "Too windy", "Too calm, drift risk", "Rain chances too high".
- Crop water: "rain covers it" only when the rain really covers the use; otherwise "rain covers about 80%", or "irrigate" under half.

## v80 (Oct 26, 11:30 PM): threat meters in the automatic briefings
- **Threat meters (1–5)** under the intro on local threat briefings, same look as the team's: Damaging wind, Lightning, Flooding, Heat. Only meters above zero show, and only when two or more apply.
  - Damaging wind: our severe level at the site, or the blend's gusts (25/35/45/58 mph → 1/2/3/4).
  - Lightning: thunder chance (15/30/50/70% → 1–4), at least one above the severe level.
  - Flooding: flooding-rain level (1/2/3/4 → 1/2/4/5), or 2 if the high-end rain is 2"+.
  - Heat: heat index 95/100/105/110° → 1–4.
- **"Heat first, storms later"** bullet when heat (2+) and storms (2+) land on the same day.
- **"Looking ahead"** bullet: the next day's severe or flooding level at the site, or "looks quieter here." Skipped when the briefing already covers that day.
- Team-written briefings keep their own meters.

## v79 (Oct 26, 11 PM): smoother radar, smarter Map Room, cleaner map
- **Local radar** is drawn from a coarser tile and blended up, so it's smooth (no "8-bit" speckle). Velocity keeps more detail.
- **Map Room**
  - Tap any color: a query box pops out **beside the spot**, says what the level means there, then **our blend's numbers for that spot**:
    - Flooding rain and severe outlooks: chance of rain, "about 0.57". The models range from as little as 0.16" to as much as 1.45"", gusts.
    - Rainfall: the total for the period, with the models' range.
    - 6–10 / 8–14 day: our blend's highs, lows and rain for those days.
    - Winter: snow from the blend. Drought: rain in the next 7 days.
  - **REGION / U.S.** buttons on every map, so you can see the whole country (Carolinas, Northeast) from anywhere.
  - **Cities on every map**, the biggest ones in view and spread out, anywhere in the U.S. Thumbnails too.
- **Around You:** dots for the biggest towns on screen anywhere (no fixed population cutoffs), so rural areas like Dodge City get dots. Names show whenever they fit.
- **Briefings**
  - A short intro paragraph up top (what's happening + our forecast), then the details, then the bottom line.
  - Closing tag: "SDR Weather Intelligence Division · issued … · next update by 7 AM, sooner if anything changes."
  - Range wording: "The models range from as little as 0.16" to as much as 1.45"."
  - Flood outro now matches the level (level 1 no longer says "even on a level 2 day").
- **Live files show no fake content:** sample briefings and build notes are hidden (add ?samples=1 or ?notes=1 to see them). The alert crawl no longer starts with sample warnings.
- **Farm & Ag:** full width, four even tiles with plain words (Spray window, Soil temp, Crop water use, Heat units). Season heat units now add up every day since Apr 1 (it was returning a single day, e.g. "4").
- **Map detail (zoomed in)**
  - County lines a little bolder.
  - Highways nearly invisible (thin, faint white); U.S. routes even fainter.
  - Real interstate shields (red and blue), interstates only, at most 10 on screen, spread out, one per route per area.
  - Detailed lakes: new water.py builds Census lake and wide-river outlines (about 60 acres and up) for the lower 48. Small lakes like Keowee and Jocassee show with crisp shorelines. Until it's built, the old lakes stay.
- **GitHub job:** new water.py step (built once, cached as water-v1), job time limit 90 min for that first build.
- **Wording kept:** "Model agreement" (ours, plain, not "confidence").

## v78 (Oct 26, 6:30 PM): the same experience anywhere in the U.S.
- **"Your region" is computed for any location:** the site's state plus every state within ~300 miles. Examples:
  - Clemson: SC, NC, GA, TN, AL, FL, KY, VA, WV, OH, IN
  - Bay County: FL, AL, GA, MS, LA
  - Columbus OH: the Ohio Valley states
  - Las Vegas: NV, AZ, CA, UT
  - Minneapolis: the Upper Midwest
- **It replaces the fixed 11-state Southeast list everywhere:**
  - alerts list and crawl
  - watches and storm-discussion checks
  - regional briefings
  - Map Room framing and the radar picture
  - Around You (the "Southeast" button is now "Region")
- **Around You** starts on the site and, once places.json exists, uses the national town list (~30,000 places), so towns show up anywhere.
- **County lines and zoomed-in detail are national** (lower 48):
  - counties.py and basemap.py now build the whole country, cut into 5-degree squares
  - the map loads only the squares on screen
- **Removed from the live files:** the Maps tab's "Southeast status map." It ran on sample city statuses (made-up warnings). Around You shows real status for any location. The prototype keeps it as sample.
- **Still regional by nature:**
  - Alaska, Hawaii and Puerto Rico aren't covered (the National Blend files are lower 48).
  - The tropics trigger watches the Atlantic and Gulf.
  - The 24/7 channel is its own build.

## v77 (Oct 26, 6 PM): zoomed-in detail + the dashboards get real web addresses
- **Zoomed-in detail, never on wide views:**
  - crisp county lines from zoom 7
  - lakes, rivers and interstates from zoom 8
  - U.S. routes and small navy route shields from zoom 9
  - Zoomed out it's our gray with terrain and the standard county lines.
  - Built by basemap.py (Census TIGER roads + Natural Earth lakes/rivers) in the GitHub job, cached once.
- **Hosting:** the GitHub job now also publishes a `site` folder. The dashboards live at
  `https://chrisjustuswx2026.github.io/nbm-ranges/clemson/` and `.../bay/`.
  - Real links that work on a phone with live data, and what a Baron push can open.
  - Pages carry "noindex" so search engines skip them.
  - Still public to anyone with the link, so treat them as test links until the legal review.
- To update a dashboard later: upload the new file into site/clemson/ (or site/bay/) as index.html, and the next job run publishes it.

## v76 (Oct 25, 11:59 PM): just crisp terrain + crisp county lines, on our gray
Chris: keep our gray and our colors; borrow only Brad's crisp terrain and county lines. Highways, shields, lakes and rivers removed.
- **Terrain:**
  - neutral shading (soft black shadows, soft white light) laid over our gray, so the gray stays ours
  - double resolution on Retina screens (phone, Mac) so it's sharp, not soft
  - tile-edge seams fixed
  - source: AWS Terrain Tiles, free and credited on the map
- **County lines:** from zoom 7 up, the national county outlines are swapped for Census detailed outlines (1:500k), drawn thin and sharp. Zoomed out, the national outlines stay.
  - The detailed file comes from a new GitHub job step (counties.py, replacing basemap.py), built once.
  - Until it's uploaded, the map just looks as before.
- Local radar and Around You.

## v75 (Oct 25, 11:55 PM): terrain, highways and lakes on our maps
- **Shaded terrain** on the local radar and Around You:
  - drawn in the browser from AWS Terrain Tiles (free open data, credited on the map)
  - our palette (navy shadows, soft highlights), sitting under watches and radar so storms still jump
  - water is left clear
- **Highways, route shields, lakes and rivers** from a new file the GitHub job builds once (basemap.py, from Census TIGER primary roads and Natural Earth lakes/rivers):
  - interstates always (thin, light)
  - U.S. routes and shields from zoom 8
  - rivers from zoom 7
  - lakes filled in our water color
  - shields are small navy chips in our style (not TV-style shields)
- Ingredients like Brad Panovich's map (terrain + roads + water), in our own look.
- The prototype viewer blocks outside map images, so the terrain shows only in the live files.
- To turn on the highways and lakes, upload basemap.py and the updated nbm.yml to the GitHub repo (same steps as places.py).
- Shading strength will be tuned once it's seen on real terrain.

## v74 (Oct 24, 11:55 PM): Farm & Ag back to clean tiles, with our own content
- Back to four simple tiles under the heading FARM & AG: one big value and one short line each.
  - **SPRAY:** the window itself, colored green / yellow / red ("6 – 11am · Wind after 11am"; "Hold · Windy"). No "Caution".
  - **SOIL:** "60° · ↓3° by Thu"
  - **CROP WATER:** "0.64 in · 7 days · rain 0.80" (adds "irrigate" when rain covers less than half)
  - **HEAT UNITS:** "3,412 · +5% vs normal" (season since Apr 1)
- Same logic as v73, fewer words. What's different from BAM is the content: a spray window instead of a rating, a soil trend, weekly crop water against rain, and the season against normal.

## v73 (Oct 24, 11:45 PM): "On the farm" replaces Field & Ag (our own design, not BAM's)
Review finding: the old Field & Ag block had BAM's exact bundle (spray, soil temp, ET, GDU tiles) and even their spray word "Caution". It's replaced with our own read for growers, in plain sentences:
- **Spray window** (from our hourly): a Go / Watch / Hold chip plus the actual window, e.g. "Good to spray 6 – 11 AM. Winds pick up after 11 AM."
  - Good hours: daylight, wind 2–10 mph, gusts under 15, rain chance under 30%.
  - Dead-calm air is flagged for drift and inversion risk.
  - Beyond the hourly range it falls back to the daily read.
- **Soil (0–4 in)** with the trend: "60°, cooling 3° by Thu" (for planting timing).
- **Water use** as irrigation: "Crops use about 0.10 in today and 0.64 in over the next 7 days; about 0.80 in of rain expected," adding "so irrigation may be needed" when rain covers less than half.
- **Heat units (GDD)** as a season total against normal: "Season: 3,412, 5% ahead of normal (since Apr 1)."
  - Source: NOAA station data via ACIS, base 50°F.
  - If that can't load, it shows today plus the next 7 days.
  - The prototype uses demo numbers.
- Unchanged and fine as ours: the rain range slider, model agreement x of 5, the day row and the conditions grid.

## v72 (Oct 24, 11:30 PM): "your area" includes 25 miles around the site
- A severe risk (any level, including level 1) or flooding rain risk within 25 miles of the site now counts as the client's own area and gets the full local briefing. Before, the outline had to cover the exact site point.
- Example: a level 1 stopping 12 miles short of the stadium gives "Severe risk today: level 1 of 5", with:
  - storm window from our hourly ("SAT 3 – 9 PM · MOST LIKELY AT CLEMSON 5 – 7 PM")
  - rain and thunder chances
  - rain range
  - gusts
  - model agreement
- Regional "nearby" notes skip anything already counted as your area.
- Playbook section 00 records the day-to-day flow: the dashboard writes the routine briefings, Chris writes the big multi-page ones, and the Baron push deep-links each client to their own latest severe briefing.

## v71 (Oct 24, 11:15 PM): regional briefings only for what's near the client (no Texas noise)
- Regional severe and flooding rain briefings now count only areas within 200 miles of the client's site, at level 2 or higher. Texas changes never reach Clemson or Bay County.
- An area covering the site itself is left to the local briefing.
- The wording says how close ("about 120 miles from Clemson at the closest") and that plans don't change.
- A drop from level 2 to level 1 nearby reads "eases" instead of "ends".
- New storage keys, so the old footprint-wide regional history doesn't carry over.
- The prototype demo now shows a nearby Georgia/Alabama change instead of Texas.
- The 24/7 channel keeps the whole footprint (it's a broadcast); the team side will too.

## v70 (Oct 24, 11 PM): briefing maps saved as written; cleaner top; calmer banner
- **Each briefing keeps the map it was written with.** Before, an older briefing ("raised to level 2") showed today's map (only level 1), which made it look made up. Now the risk map is saved with the briefing.
- **Top of the page is two clear halves:** "RIGHT NOW · Memorial Stadium" and "WHAT'S NEXT", same style label. The "Updated 10:50 PM" line is gone.
- **New briefings no longer sit inside What's Next:**
  - a slim strip under the top cards ("NEW BRIEFING · Storms organizing nearby… · Read →"), only for threats (severe, flood, tropical, heat, winter, wind, freeze), until it's been read
  - a red dot on the Briefing tab for anything new
  - outlooks and seasonal updates only get the dot
- **Map banner pill:** no more orange. It's a clean glass pill with a small dot: red for raised or watch possible, green for lowered or removed.
- "Severe storms tomorrow–Mon" (lowercase "tomorrow" in the middle of a headline).
- Note: the two "Southeast" severe briefings Chris saw in v65 were real SPC changes during the day (a level 2 somewhere touching the footprint, lowered in the evening). Since v67 these are named by state.

## v69 (Oct 24, 10 PM): modern map banner
- Replaced the blocky TV banner with one frosted card top-left: SDR logo, title in sentence case ("Flooding rain risk · Texas") and the date ("Today · Oct 24").
- A small orange pill appears only when something changed: Risk raised / Risk lowered / Risk removed / What's changed / Watch possible.
- The legend shows only when the map has risk levels or a watch: a small "Level ● 1 ● 2" pill (top-right on desktop, bottom-right on phones). The outlook maps no longer have a Cooler/Warmer key, and the bottom caption is gone.
- When storms organizing and a risk change arrive together, the headline now matches the map ("Storms organizing nearby: a watch may follow").

## v68 (Oct 24, 9:45 PM): the prototype gets the briefing engine; one briefing per threat
- **Prototype (the page you open on your phone)** now runs the same automatic briefing engine as the live files, on demo data. It opens with:
  - Clemson: "Severe risk raised to level 2 for tomorrow" (in What's Next, with what changed)
  - Clemson: "Flooding rain risk raised to level 2 for tomorrow" (heaviest-rain window)
  - Clemson: "Pattern change ahead: turning warmer and wetter"
  - Region: "Flooding rain risk raised for Texas today" and "Severe risk raised for Oklahoma and Texas Monday"
  - Plus the three sample team briefings, TV-style maps, flooding rain cards in the Map Room, and Copy link.
  - Demo data is only in the prototype; the live files use real data.
- **One briefing per threat (all files):** when several things change at once, severe, flooding rain, outlook, tropics, each alert type and each regional change get their own briefing and tile. The most urgent sits on top.
- The live Clemson file was also published as its own page for testing. The artifact viewer blocks live weather feeds, so it can't load real data there; use the prototype on the phone.
- The Leaflet map styles are now built into the live files (no outside stylesheet).
- On phones the Copy link button reads "🔗 Link".

## v67 (Oct 24, 9:30 PM): flooding rain risk, every trigger, state-by-state regional briefings
- **Map Room:**
  - Four new FLOODING RAIN RISK cards (WPC excessive rainfall, days 1–4), right after the severe outlooks.
  - Each card shows the level at the site and the states affected; tap for the full map.
  - Data: WPC's GeoJSON, with the NOAA map service as backup. If a day isn't published, its card is skipped.
- **New automatic briefings, all in the SDR Weather Intelligence Division voice with TV-style maps:**
  - **Flooding rain risk at the site**, days 1–4 (new / raised / lowered / removed):
    - HEAVIEST RAIN window from our hourly
    - an outro about low spots, creeks and roads
    - an operations bottom line
  - **Severe risk days 4–8** at the site ("Early look").
  - **Tropics:** a cone that includes the site (takeover-level), a cone reaching the footprint, or an area to watch near the Gulf/Southeast coast.
  - **Official alerts at the site:** flood, heat, freeze/frost, winter, wind, tropical.
  - **From our forecast:** first freeze of the season, frost possible, heat index 105+, snow or ice signal, gusts 45+.
- **Regional briefings, state by state:**
  - Severe and flooding rain changes are written up per state ("Severe risk raised for Texas tomorrow"), with a map zoomed to that state.
  - Two states are named; three or more becomes "the Southeast". The client's own state is handled by the local briefing.
- **Organization:**
  - Local and regional changes are always separate briefings; the page opens on the newest local one.
  - One tile per threat per day (a newer update replaces the older tile).
  - New FLOOD filter.
  - Timing strips only where they belong (storm window, heaviest rain).
- **CHANNEL-247-UPDATE.md:** the message to paste into the 24/7 channel's chat. Same change logic, TV branding, flooding rain pages, lower thirds, and SDR and CJWX versions.
- BRIEFING-PLAYBOOK.md section 4 lists every trigger.

## v66 (Oct 24, 8:45 PM): TV-style briefing maps, "what changed", storm window from the blend
- **What changed (automatic, every time):**
  - Raises, lowers and removals each get a "What's changed" first bullet.
  - The headline says it: "Severe risk raised to level 3 for tomorrow", "…lowered to level 1…", "Severe risk removed for Saturday".
  - The sub starts "The threat has increased." or "The threat has come down."
  - A drop to general thunderstorms only counts as removed ("General thunderstorms are still possible").
  - General thunderstorms alone never trigger a briefing.
- **Storm window from our hourly (National Blend based)** on severe, storms-organizing and watch briefings:
  - Example: "STORM WINDOW · SUN 2 – 8 PM · MOST LIKELY AT CLEMSON 4 – 6 PM"
  - Broad window = hours with a real storm chance; most likely = the peak hours.
  - The timing bullet now uses the same end time.
- **TV-style branding on every briefing map:**
  - logo top-left
  - a title bar with an orange sub-banner (e.g. SEVERE WEATHER RISK / TOMORROW · OCT 25 · RISK RAISED)
  - the legend under the logo, showing only the levels on the map
  - Outlook: one banner across both maps ("PATTERN OUTLOOK / TURNING WARMER AND WETTER"), plus a small key on each map.
  - Samples use the same look.
- BRIEFING-PLAYBOOK.md section 1b records all of this as locked in.

## v65 (Oct 24, 8:15 PM): automatic briefings know what matters where
- **New automatic trigger:** regional severe risk.
  - When the highest SPC risk anywhere in the client's footprint goes up, down or ends (days 1–3), a briefing is written on its own.
  - Example: "Severe risk lowered across the Southeast tomorrow: now up to a level 1 of 5 (Marginal), down from level 2."
  - Map: the whole region.
- **Relevance decides where it lives:**
  - Changes at the client's own spot: lead the briefing page and show in What's Next ("New briefing · … →") right away; tagged YOUR AREA.
  - Changes only elsewhere: filed in the library as a tile tagged REGION; they don't touch What's Next.
- **Library tiles:**
  - show the real kind (SEVERE, OUTLOOK…) instead of "UPDATE"
  - new OUTLOOK filter
  - only one LATEST tag
- Briefings name the town ("severe risk for Clemson"), not the venue.
- What's Next updates the moment a local briefing posts (before: up to 2 minutes later).

## v64 (Oct 24, 8 PM): automatic briefings speak as the SDR Weather Intelligence Division
- No agency names in client-facing briefing text. Before: "New outlooks from the Climate Prediction Center lean…" / "SPC has Clemson in a level 2…". Now:
  - Outlooks: "The SDR Weather Intelligence Division is monitoring a warmer and wetter pattern for Clemson. We favor above normal temperatures and rainfall from Oct 29 through Nov 6." If temperatures and rain cover different dates, each gets its own dates.
  - Severe risk: "New: the SDR Weather Intelligence Division is monitoring a level 2 of 5 (Slight) severe risk for Clemson Saturday."
  - Storms organizing (mesoscale discussion): "Storms are organizing near Clemson. The SDR Weather Intelligence Division is monitoring closely; a watch may follow."
  - Map captions: "Severe risk", "Area we're monitoring", "Outlook".
- Footer is "SDR Weather Intelligence Division · issued SAT 7:45 PM"; the header label is UPDATE (no more "intermediate").
- When a severe risk and an outlook change together, the severe risk leads the headline and map; the outlook goes in the details.
- "Most likely between 7 PM and 7 PM" now reads "most likely around 7 PM".
- Sample team briefings use the same voice.
- BRIEFING-PLAYBOOK.md v2 adds a "Who writes what" section:
  - The dashboard writes the routine ones: SPC risk, storms organizing, watches, outlooks.
  - Chris writes the judgment ones: model trends, hurricane and snow signals, seasonal.
  - Both follow the voice rules and the push-link steps.

## v63 (Oct 24, 7:50 PM): briefing playbook written down
- New file BRIEFING-PLAYBOOK.md covers:
  - the six parts every briefing has
  - what goes in the details for severe, outlook, tropical, seasonal, winter and after-action briefings
  - our words (odds, SPC levels, ranges, normals)
  - when automatic briefings fire and expire
  - links for push alerts
- A short version is on the Build Notes panel (bottom of the dashboard) in the prototype and both live files.

## v62 (Oct 24, 7:45 PM): sample team briefings; a link for every briefing
**Sample team briefings (Clemson file):** tap these in the library and they open in the full format (headline → intro → map → details → outro → bottom line). They're marked "TEAM BRIEFING · SAMPLE".
- **Severe weather threat · Saturday:**
  - Level 2 of 5 risk map with a key.
  - Storm window 3–7 PM.
  - Threat, timing, rain range, lightning and model agreement.
  - Outro: "Not every spot sees a severe storm on a level 2 day…"
  - Bottom line: tarp on and teams in by 4:15.
- **Tropics: what we're watching:**
  - Map of the two areas (40% and 20%).
  - What each area means and what it means for Clemson.
  - The late-season note.
- **November outlook:**
  - Monthly temperature map.
  - Normals for the month, first frost, about 4" normal rain, and Thanksgiving week.
  - Outro: "A mild month still brings cold snaps…"

**Briefing links (for the push alert):**
- A "🔗 Copy link" button on the briefing page.
- The link opens the dashboard straight to that briefing:
  - `?brief=latest` for the newest briefing
  - `?brief=severe` / `outlook` / `tropical` / `seasonal` for the newest of that kind
  - `?brief=sample-severe` etc. for the samples
- Each client's dashboard writes the briefing for its own location, so the same "severe" link opens Daytona's version for Daytona and Clemson's for Clemson.
- In production, Andrew gives one short link per kind that sends each signed-in client to their own dashboard.
- A briefing you open stays on screen; the 10-minute refresh no longer swaps it out.

## v61 (Oct 24, 7:30 PM): outlook briefing gets an intro and an outro; no repeated location
**Outlook briefing format:** headline → intro paragraph → two maps → the details → outro paragraph → bottom line.
- Intro: "A pattern change is on the way. New outlooks from the Climate Prediction Center lean warmer and wetter than normal for Clemson from Oct 29 through Nov 6. Closer in, our forecast: dry through next Saturday…"
- Outro, in plain words for whichever way it leans:
  - Warmer: "Warmer than normal doesn't mean every day is warm. A pattern like this can still bring a cool day or two, especially behind a passing front."
  - Wetter: "Wetter than normal is about the total over the period, not rain every day…"
  - Same idea for cooler and drier.
  - Ends with "We'll keep you posted as the details come into focus."
- The separate "Our forecast" bullet is folded into the intro.
- Stored briefings rebuild once more in this format.

**Right Now card:** removed the extra line under the temperature ("Clear · Clemson, Clemson-Oconee County Airport · 6:50 PM"). The card already says where and when.

**Version in the browser tab:** live files now show "(Live · v61)" in the tab title, so the newest download is easy to tell apart.

## v60 (Oct 24, 6 PM): back to "Model agreement"
- 10-day label is MODEL AGREEMENT again (Chris: "confidence" reads like we're not confident). Same bars and 1–5 number.
- Day detail: "MODEL AGREEMENT ▮▮▮▯▯ 3 of 5". At 2 or below: "Models disagree on rain amounts. Expect changes; we will update as it comes into focus."
- Briefing detail line: "Model agreement: 3 out of 5."
- The data hook for the chat is unchanged (`window.SDR_CONF`).

## v59 (Oct 24, 2 PM): smarter outlook briefings; Overview order
**Outlook briefings (CPC)**
- When outlooks are issued together, they're written up together. There's no more separate line for each one.
- Headline tells the story:
  - Both lean: "Pattern change ahead: turning warmer and wetter" (or cooler/drier).
  - One leans: "Warmer pattern ahead".
- Subhead: "New outlooks for Oct 29–Nov 6 lean warmer and wetter than normal."
- The details, in plain words:
  - Temperatures: "Strong odds of warmer than normal (70% for Oct 29–Nov 2, 60% for Oct 31–Nov 6)."
  - What's normal: "Highs near 66° and lows near 43° in Clemson this time of year. Warmer than normal means days, nights or both running above that."
  - Rain: "Leaning wetter than normal (40% …)."
  - Normal rain: "Normal rain for Oct 29–Nov 6 is about 1.0". Odds favor more than that."
- Odds words: 60%+ strong odds · 50%+ good odds · 40%+ leaning · under 40% slight lean.
- Normals: NOAA's official 1991–2020 normals from the nearest weather station with data (free, from the ACIS climate data service). If they can't be loaded, those two lines are left out.
- Two maps side by side (temperature and rain); they stack on a phone.
- Bottom line adds what's coming: "Normal operations all week. Watching a warmer, wetter pattern starting Oct 29."
- Briefings are rebuilt once in the new format (new storage key), so today's outlooks show the new write-up right away.

**Overview order**
- Map Room and Briefings now sit above Around You and Your Schedule.
- Phone order: Alerts → Around You → Map Room → Briefings → Schedule.
- Desktop: Map Room | Briefings, then Around You | Schedule.

## v58 (Oct 24, 9:15 AM): no sample flash; switched locations switch everything
- What's Next no longer opens with sample text in yellow. It shows a neutral "Checking the forecast…" until the real forecast loads, then updates immediately (before, it could wait up to 2 minutes for its next check).
- After switching location (search or "Full forecast for…"), these now follow the new place:
  - the radar centers on it and uses the nearest radar
  - the alert crawl label
  - the 10-day title
  - the browser tab title
  Before, they stayed on Clemson.

## v57 (Oct 24, 12:20 AM): location switch in the prototype too
- The prototype now has the search box in the location drop-down, the "Full forecast for [city] →" button on Around You cards, and the "Viewing [city] · sample data · ← Back" bar.
  These had only been in the live files.
- In the prototype the city name changes but the weather stays sample data. The live files load that city's real forecast, radar and alerts.

## v56 (Oct 24, 12:15 AM): confidence is the backbone; every U.S. town searchable
**Confidence**
- 10-day header now reads CONFIDENCE ▮▮▮▯▯ 3 (was "MODEL AGREEMENT GOOD"). It shows on phones too.
- The header uses the lowest of the next 3 days, so a shaky day isn't averaged away.
- Each day's detail shows "CONFIDENCE ▮▮▮▯▯ 3 of 5". At 2 or below, a plain line follows: "Lower confidence in rain amounts. Expect changes; we will update as it comes into focus."
- How it's measured: the National Blend spread for that day.
  - Rain: the gap between the low end and the high end compared with the expected amount.
  - Snow: same approach as rain.
  - The high temperature: how far the models disagree.
  - The weakest of these sets the score.
- Feeds the chat: `window.SDR_CONF` gives each day's confidence and what's driving it, so replies can say "confidence 2 out of 5; models are struggling with rain amounts."

**National place list**
- The search box covers every U.S. city, town and named community (about 30,000) plus every ZIP code. Type "29631" or "clemson nc".
- Built by the GitHub job from the Census Bureau (free), once, then reused.
- Loads only when someone starts typing.
- If the list isn't there yet, search falls back to the built-in list.

## v55 (Oct 23, 11:55 PM): clean 10-day
- Green days show no words at all. The icon, temps and rain % tell the story.
- Yellow and red days show one short word in color: Storms, Rain, Windy, Frost, Freeze, Hard freeze, Hot, Fog, Snow, Ice. No more cut-off sentences ("Sunny, high ne…") or doubled reasons.
- The full NWS wording is still there when you tap a day.

## v54 (Oct 23, midnight): hourly colors, change location
**Colors do the talking**
- Hourly: each hour has a green / yellow / red bar across its top.
  - Red: storms at 70%+, gusts 45+, or heat 100°+.
  - Yellow: rain at 40%+ (60% Jun–Sep), any storm chance at 20%+, gusts 30+, temps 34° or colder (frost), fog, or visibility under 1 mile.
  - Green: everything else.
- 10-day: the ALL CLEAR / HEADS UP / TAKE ACTION words are gone; the color bar and the colored reason ("Storms 60%", "Frost possible") say it.
- 10-day rules match the hourly:
  - Storms at 70%+ are red (under 70% yellow).
  - Heavy rain (80%+ and 1"+), ice, gusts 45+, and heat 100°+ are red.
  - Frost (36° or colder), fog, gusts 30+, and heat 95°+ are yellow.

**Change location (live files)**
- The location drop-down has a search box: type a city ("ashe" → Asheville NC) and tap it.
- When viewing another place, the whole dashboard switches to it: Now, What's Next, hourly, 10-day, radar centered there, and alerts for that state.
- A bar at the top shows "Viewing [city] · ← Back to your location".
- Around You: tapping a city dot shows a "Full forecast for [city] →" button.
- How it works: the link gets ?place=lat,lon,Name,ST, so a viewed location can be bookmarked or texted.
- Search covers the cities in our place list; small unincorporated spots may not show.

**Radar "flash the newest"**: already in place from v44. New watches, tornado and severe warnings, and SPC discussions pop a toast on the radar and pulse their outline. No change.

## v53 (Oct 23, 11:35 PM): let the colors speak
- Removed the ALL CLEAR / HEADS UP / TAKE ACTION legend from the top of the 10-day; the words on each day already say it.
- Around You explainer is now a compact key: ● All clear ● Heads up ● Take action · Tap a dot for what's next.
- Removed the leftover "CHANNEL MAP ENGINE" tag under the radar (prototype).

## v52 (Oct 23, 11:30 PM): What's Next engine, section headings
**What's Next (the gold) now reads all 10 days and tells one story:**
- Next 12 hours always leads if rain/storms are coming ("Storms possible by 4 PM · Winding down by 8 PM").
- Otherwise every day is checked for things worth planning around: SPC severe risk (level 2+), storms, rain (40%+, 60% Jun–Sep), heavy rain (1"+), snow, ice, freeze (32°, or 20° in Dec–Feb), heat (97°+), wind (gusts 35+), and big cool-downs (15°+ drop).
- Each gets a score; small chances never lead. Back-to-back days merge into one stretch ("Rain Mon–Tue").
- 0 events: "Dry for the next 10 days" / "Dry through Saturday · Only a small rain chance Sunday (20%)." (green)
- 1 event: "Severe storms Sunday · Level 2 of 5 (Slight) severe risk. Dry until then."
- 2 events: "Rain tomorrow, more rain Thursday · Thursday: 70% chance, around 0.60"." (the bigger one gets the detail)
- 3+ rain chances: "Unsettled stretch ahead · 3 rain chances in 10 days, starting tomorrow. Biggest: rain Monday."
- Only days 8–10: green "Quiet this week · Watching rain next Saturday: 60% chance."
- A "New briefing · [title] →" line appears in the card for 12 hours after an intermediate briefing posts.
**Sections:** bigger white section titles; one-line explainers under Alerts and Around You. Around You opens zoomed on the client's area.

## v51 (Oct 23, 11:15 PM): briefing cleanup
- Briefing video is a compact strip (play button + label) instead of a full-width player, so the briefing is readable right away.
- Intermediate briefings expire on their own when what triggered them is no longer valid: SPC day outlook → the morning after that day; mesoscale discussion → 3 hours; watch → when the watch ends; CPC outlook → the end of its period. Team briefings (seasonal, monthly, severe recaps) stay in the library.

## v50 (Oct 23, 11 PM): status icons
- ALL CLEAR: clean green check. HEADS UP: yellow warning triangle. TAKE ACTION: red warning triangle. No pulsing.

## v49 (Oct 23, 11 PM): intermediate briefings get the full format
- Layout: video (if any) → HEADLINE → subheadline (one sentence: "Scattered severe storms are possible Sunday.") → hero map (the outlook that triggered it, zoomed on the site, with a caption) → THE DETAILS bullets → timing window → BOTTOM LINE.
- Details come from our own forecast for that day: chance of rain/thunder, timing window, rain amount and range, gusts, confidence x out of 5.
- Hero map by trigger: SPC outlook, mesoscale discussion, active watches, or the CPC outlook (U.S. view).

## v48 (Oct 23, 11 PM): intermediate briefings
- Briefings are now **intermediate briefings**, written automatically only when something official changes for the site: SPC Day 1–3 severe level issued/raised/lowered, an SPC mesoscale discussion over the site, a watch for the site, or a CPC 6–10 / 8–14 day flip (warmer/cooler, wetter/drier at 40%+).
- Content = what was issued + our existing forecast numbers. No new forecasting. Max 3 per day (more triggers update the latest one).
- Each one is saved in the briefing library tagged UPDATE (newest marked LATEST). Bottom line reads "Intermediate briefing · issued Fri 10:55 PM".
- The team's own briefings (pattern, monthly, big storm) always lead. Production note for Andrew: store these on the server so every viewer sees the same list.

## v47 (Oct 23, late night): Chris's review list
**Top of page**
- Bigger SDR logo; bigger "RIGHT NOW" and "WHAT'S NEXT" labels; bigger conditions numbers.
- Wind reads "N 8 gusts 14" (the little "g" is gone).
- WHAT'S NEXT picks the BIGGEST thing in the next 7 days (a 60% storm day beats a 30% shower day sooner). Quiet days get one short line, no temperature ranges.
- Chat button: "Message the team".

**Radar**
- One brand: bigger SDR logo + red LIVE RADAR in the header; the second small logo on the map and the extra "WEATHER INTELLIGENCE" text are gone.
- Loop controls: "▶ LOOP" and "❚❚ PAUSE" side by side, the active one lit.
- Frame time shows the clock time of each frame (10:05 PM … NOW · 10:25 PM) instead of "−35 MIN".
- Detailed coastline: Florida Keys, Outer Banks and barrier islands now drawn as land.
- Warning card order: hazards (what / tornado / hail / wind) → tags (damage, radar indicated or confirmed) → Valid until (countdown) → Moving → Counties → track times → More (cities included + full text).
- Card opens clear of both the warning and its storm track; drag it by the colored header if it's still in the way.

**Map Room**
- What, then when: "SEVERE OUTLOOK · TODAY" (date + SPC underneath), "SEVERE OUTLOOK · DAYS 4–8", "LIVE RADAR · Latest scan".
- Around You wording: "Each dot is a city's status right now. Tap one to see what's next there."

**Briefing (live files)**
- Drafted from live data in our voice: headline (= What's Next), summary, timing window, bullets, BOTTOM LINE, "Issued Fri 10:39 PM · next update Sat 7:00 AM or sooner". A new SPC outlook that includes the site leads the bullets ("New: SPC has Bay County in a level 2 of 5 (Slight) severe risk Sunday"). Refreshes every 30 min. The team's written briefing overrides it (window.BRIEF_OVERRIDE).
- Video box: "No video update necessary at this time" when the latest video is more than 36 hours old.

## v46 (Oct 23, late): small polish
- ALL CLEAR shows a check mark instead of a dot. When it's clear and dry, no line under it (the card speaks for itself); a line only appears when there's something to say (rain nearby, a reason for yellow/red).
- Hour by hour always shows every hour; just scroll. The 12H/24H/72H buttons are gone.
- Rain gauge: EXPECT number lifted so the tick no longer covers it.
- Chat playbook written (CHAT-PLAYBOOK.md) and added to the build notes.

## v45 (Oct 23, night): one clear message
- Under ALL CLEAR, one line instead of two: "No warnings · no rain within 30 miles" (or "No warnings · rain 15 miles NW"). The separate rain pill is gone. If the rain check can't load, the old line shows instead. In HEADS UP / TAKE ACTION the reason line shows as before.
- WHAT'S NEXT rewritten in a forecaster's voice: "Rain arrives Tuesday afternoon · 60% chance, around 0.45" for most. Dry until then." / "Storms possible by 4 PM · Lightning is the main concern." / "Dry for the next 10 days · Highs in the low 70s, lows in the 40s." Yellow tint on the card a little stronger.
- Around You: removed the count badges at the top (they repeated the grouped list underneath).

## v44 (Oct 23, evening): opening screen cleanup
- Status card now holds current conditions: temperature, feels-like/wind chill/heat index, wind with gusts, "No rain within 30 mi". Humidity removed from the top (still in hourly and 10-day details).
- WHAT'S NEXT is now the live weather story, written from the hourly and 10-day every 2 minutes. Its color is separate from the status: green = quiet ("Dry for the next 10 days", "Quiet through Thursday"), yellow = something to plan around ("Storms ~4 PM", "Rain Tuesday", "Frost & freeze Monday night"). Team override: window.STORY_OVERRIDE.
- Alert ticker and quick-jump buttons hidden on phones (still on desktop/monitor).
- Fix: prototype was showing hidden items (the countdown row, the venue menu).

## v43 (Oct 23): rain gauge
- Rain amount on a real inch scale: 0" to a round top value, EXPECT over its tick, low end / high end under the end dots; tight ranges collapse to "could be X to Y".

## v42: rain bar end points
## v41 (Oct 23, 12:20 AM): removed WPC Today's/Tomorrow's Setup (fronts) from the Map Room
## v40 (Oct 22, late): Map Room additions
- CPC 6–10 and 8–14 day temperature and rain, Drought Monitor (weekly), Winter Impacts (Nov–Mar only).
- Rainfall cards each open their own period; Days 4–8 card opens properly.
- Rain amount wording: AT LEAST / EXPECT / UP TO.

## v39: precipitation section trimmed
- One line of chances (rain day/night, thunder 20%+, snow/ice 10%+); "No measurable rain expected" on dry days.

## v38: rain range simplified; model agreement fixed for light amounts (0" vs 0.4" no longer reads "Poor")

## Radar (live files, Oct 22–23)
- Shading under the radar, outlines on top (TV style).
- Tap card opens beside the storm: hazards, damage tags, expires, counties, storm track, More = cities included + full text.
- Dashed storm track + arrow on every warned/strong storm; times appear when tapped. Neutral wording ("on its current track ... if it holds together"). No automatic banner.
- Alerts: STORMS, SEVERE WATCHES, SPC DISCUSSIONS on by default; + MORE = other warnings, other watches, advisories, statements.
- NATIONAL / LOCAL / VELOCITY (nearest radar site, tries both velocity product names), PAUSE button, full screen, smoothing when zoomed in.
- County lines for every state (zoom 8+), small towns from the Census when zoomed in, lightning rings hide when zoomed out.
- New-alert pop-ups (new SPC discussion, watch, tornado warning). Branded header: SDR logo, WEATHER INTELLIGENCE, LIVE RADAR.
- Overlays: SPC Day 1/2/3/4–8, WPC rain Day 1/2/3, 1–3, 1–5, 1–7, tropics.

## 10-day (Oct 22)
- 10 days: NWS days 1–7, National Blend days 8–10 (no on-screen source credits). Stoplight call per day + legend. Model agreement (3–5 green, 2 orange, 1 red). Field & Ag: spray GO/CAUTION/NO-GO, soil temp, water use (ET), GDU.

## Data jobs
- GitHub (chrisjustuswx2026/nbm-ranges): National Blend ranges + 10-day guidance + soil temp, every 3 hours. Monthly phone reminder set (starts Nov 20).

## v208
- Chat: site uploads no longer blank out the chat server address (channel.json now carries it, and chat defaults to it). Chat server gets forecast_for_place (any town or stadium), event lookups (Dog Walk = about two hours before kickoff), dressing/comfort advice, 4 searches, and /health.
- Rain totals: within ~2.5 days the likely amount is anchored on the official forecast amount, with the model spread scaled around it.
- Daily briefing: one page. Removed At a Glance, looking ahead, timing/model-agreement repeats, page 2 header; at most 2 maps, no repeat of the hero map.
- Hunt & Fish: rebuilt from the scored outlook (deer/fishing chooser, 10 days scored /10, morning/midday/evening, peak window, hour bars, reasons, how to play it, explainer, rut by area).
- What's Next and briefing headlines name the main rain window, not the first sprinkle.

## v209
- Model agreement drops one point when the official rain amount and the models' middle differ by more than 2x (within ~2.5 days).

## v210
- Tropics: development areas now load (the outlook layer is named "Seven-Day: Potential Development Region"; the old name match never found it). Tropics maps widen to show areas far out in the Atlantic.

## v211
- Briefings: "What it means for you" (how much, what it does, what to do) replaces robotic lines; flood briefings never say flooding isn't the concern; the tallest rain bar is always labeled; event briefings carry the hero map plus at most one more; no pattern map; printing scales to one letter page and can't spill.
- Flood sub-headline no longer quotes its own rain amount (one number on the sheet, from one source).
- Chat: the message box grows as you type (up to about 5 lines).
- Hunt & Fish opens full screen on computers (Esc or Close to exit).
- Tropics map always opens on its wide Atlantic view.

## v212
- Model agreement rebuilt: temperature spread judged against what's normal for that lead time; rain judged two ways (will it rain; how much, in decision bands, not a ratio); amounts only count when they matter; factors blended, not the single worst; official-vs-models gap still costs a point. 10-day header = average of the next 3 days. Reasons say "whether it rains", "how much rain" or "temperatures".
- Rain anchor no longer stretches the high end above the models when the official amount is the higher one.
- International maps: full country map loads in the background (Central/South America, Caribbean islands, Bermuda, Africa's coast) with borders; zoomed-out maps label countries, oceans and major cities instead of small U.S. towns.

## v213
- Tropical briefings: their own sheet (tropics map, each area with its chance and exact location, what it means), no local rain content. Only start when an area is within ~700 miles of the client (~1,100 for medium/high). Wording names the spot ("about 300 miles south of Bermuda") and distance from the client.
- Every event briefing draws its own map for that briefing (flood, severe, tropics); never copies whatever map was on screen.
- Print happens in place (no new window, so the home-screen app can't get stuck); only the sheet prints, scaled to one letter page, white page.
- Risk strip says "RISKS · THURSDAY" instead of "TODAY'S RISKS · TOMORROW".

## v214
- Tropical briefings go out for any Atlantic, Caribbean or Gulf activity, near or far, with the exact location and distance from the client.

## v215 — briefings rebuilt and tested
- Briefing test run (lab/run.js): 15 scenarios (quiet, storm day, flood L1/L2, severe L2/L3, storms organizing, tornado watch, flood warning, freeze warning, winter storm, tropics far/Gulf high/cone over us, regional severe) through the real code; 29 pages; all one page; banned-phrase scan clean.
- Each briefing reads by threat: severe (when, main threat, what to do, shelter), flood (how much, what it does, flood actions), winter (snow amounts, start, roads), freeze (how cold, freezing hours, a second freeze), heat, wind, regional ("not at Greenville"), tropical.
- One main threat per page (subhead, panel and tiles agree); tornado tile under tornado threats; flood tile 4+ under a Flood Warning; snow & ice tile on winter pages.
- Daily briefings lead with an active watch/warning; freeze/heat/wind days read as such; evening label and "tonight" after 5 PM; no "now" in titles.
- Bottom lines fit the threat. Warnings say when they end in plain words. Noon and midnight everywhere.
- Event maps are drawn for the briefing (storms-organizing area, watch box, winter area, flood/severe outlook, tropics); no repeated maps.
- Print rebuilds the sheet at full letter width (phones no longer print a skinny page) and fits it to one page.
- One briefing per threat (alert + forecast merged; winter absorbs freeze).
- Chat: never uses the sample Schedule Watch events; never assumes a job or event; no slogans; doesn't open with a status word.

## v216
- Naked radar: until tapped it shows only the weather, ring and logo (slightly smaller); tap/click opens it with +/-, warnings, play and layers.
- Core check (lab/core.js): phone + desktop, quiet + storm day: no errors, no sideways scroll, no empty cards.

## v217
- Jumping to a warning from the warnings list opens the full branded warning card (hail, wind, damage tags like CONSIDERABLE, timing, motion, track), the same card as tapping it on the map. Test: lab/warn.js.

## v218
- The highlight around a warning you jumped to never catches taps, so tapping a warning always opens the branded card (no more stuck-in-generic).

## v219
- A level 1 (marginal) severe risk is now a HEADS UP in What's Next and on the Around You dots, worded "Isolated severe storms possible… Level 1 of 5: a few storms could turn severe; not everyone gets one." Level 1 never gets the bare "Severe storms" headline. Map Room rule note updated.

## v220
- Print: one page when it fits, using the full page width. When it would shrink too far, page 2 is "MAPS & DETAILS" with its own header; pages say PAGE 1 OF 2 / PAGE 2 OF 2.
- Chat: pictures follow the whole conversation (a game/work/event question gets the hour-by-hour for that day, not the 10-day). Worker: coaches/crews get operational info, fans get comfort tips.

## v221
- Executive briefing look matched to the SDR manual briefings: clean bold sans headline, letterspaced green kicker, centered letterspaced section bars, map hero with "what it means" beside it on full-width sheets, wider side margins used, stronger bottom line and footer.

## v222
- Radar rings labeled on the ring lines: "10 MI · LIGHTNING" and "30 MI · HEADS UP". The small radar shows only the orange dot for the site (no name plaque covering towns); the name still shows in full-screen radar.

## v223
- Right Now: any rain on radar inside the 30-mile ring (light rain included) is HEADS UP, worded "Rain in the area: 10 miles southwest." ALL CLEAR only when nothing is inside 30 miles.

## v224
- Warning card, our look: dark card with a thick left edge in the official warning color, the warning name in that color, a time-left bar that drains, threats as chips (HAIL 1.00", WIND 70 mph, CONSIDERABLE DAMAGE). Motion, counties, track and More unchanged.

## v225–v226
- Briefing maps zoom in: storms-organizing areas and watch boxes are framed around the area and the site; flood/severe outlook maps use a regional frame; bigger towns labeled.
- Storms-organizing briefings: "When" uses the official organizing window, same as the subhead.
- Tornado tile now comes from the official tornado probability outlook: 2% = 1/5, 5% = 2/5, 10% = 3/5, 15% = 4/5, 30%+ = 5/5 (at least 3/5 under a Tornado Watch).
- Map Room: TORNADO RISK · TODAY / TOMORROW cards appear only when there is a tornado risk.

## v227
- Map Room tornado cards show any 2%+ tornado risk anywhere in the country, framed to include the whole risk area and the site; the full-screen map draws the areas in the official colors (tap for the chance and level).

## v228
- Right Now never shows a time that has passed or "likely likely": when the rain hour has started it reads "Light rain now or starting soon."

## v229
- Right Now HEADS UP matches What's Next: navy card, thick yellow left edge, yellow HEADS UP (no brown). TAKE ACTION gets a red left edge.

## v230
- Tornado outlook: if the main tornado map file can't load in the browser, it now pulls the same day 1/day 2 tornado outlook from the backup map service, so the Map Room tornado card shows up.

## v231
- Briefings redesigned: navy masthead with the logo on a white chip and a hazard-colored top edge (same on SDR and the CJWX preview), smaller headline, soft section cards instead of solid blocks.
- Briefing maps in the Map Room style: title plaque with logo, readable town labels, site name pill, wider framing; taller on phones.
- One timing window everywhere (subhead, hour panel, what to do, bottom line).
- Hour-by-hour charts (briefing and chat picture): times and temps in their own rows; nothing floats over the bars.
- Phones can no longer get stuck in the squeezed two-column layout after printing.
- Print: letter width with no clipping on iPhone; fits one page (page 2 only for extra maps).
- Radar: site name plaque removed (orange dot + rings mark it); ring tags hide when zoomed out, rings hide below state level.
- Warning card on radar: slightly bigger text and always opens below the logo plaque, inside the frame.

## v232
- Storms organizing: the strongest expected gust, hail size and tornado strength from the notice now show as chips on the radar card ("DAMAGING WIND up to 60 mph", "HAIL up to 1.75\"", "TORNADO brief, EF1 strength") and as one "Strongest expected" line in the briefing. "Damaging" only at 58+ mph; tornado strength given as EF number, no mph.
- Briefing "Main threat" no longer shows a lower model gust number next to the notice's number.

## v233
- Tornado wording: "brief, up to EF1 strength" (chips and briefing line).
- Chat worker: questions about storms anywhere (an emergency manager asking about Rome or Whitfield) now get that place's live severe picture: outlook level, tornado/wind/hail chances, flooding rain risk, alerts there, warnings and watches within 60 miles with distance and direction, and storms-organizing areas with watch chance, end time and strongest expected values.

## v234
- Storms-organizing card: one card, no scrolling. One row of chips with the numbers ("TORNADO Isolated, brief, up to EF1", "DAMAGING WIND Up to 60 mph"), then the time window and watch odds. "Isolated" when a watch chance is under 40%. Capitalized.
- Home: What's Next no longer repeats Right Now. When it's wet now it says how long ("Storms until 1 AM"); tonight's bullet is dropped when the headline covers it; no start times that already passed.
- Chat: asking about another place now attaches a severe-risk map centered on that place (Map Room look, towns, storms-organizing areas). Asking "pic?" afterward re-sends it. The chat never says it can't attach an image.

## v235
- Warning card time bar fills up as the warning runs (nearly full = almost over), instead of emptying. A long warning with 22 minutes left now reads as nearly done.

## v236
- Print: a phone now measures the pages in the real letter-width layout (it was measuring its narrow phone layout, which broke pages in the wrong places). Tighter print layout fits one page at normal size; extra maps go to a labeled page 2. No shrink tricks that iPhone ignores.
- Daily headline uses the same window as the rest ("Storms possible tonight, mainly 8–10 PM", not "by 7 PM").
- Storm days show the severe outlook map when a risk area is close, even if the site is just outside ("Just outside the risk area. Level 1 of 5 starts about 20 miles southwest.").
- Maps under the sheet are framed on our area with towns labeled, not the whole Southeast.
- Rain "By the numbers" box only when rain is the story.
- Slimmer masthead. Footer: "NEXT BRIEFING: BY 7 AM TOMORROW" / "BY 3 PM" / "AS NEEDED".
- Bottom line no longer assumes "outdoor work".
- CJWX preview worker: no closing slogan ("We're here to help" removed).

## v237
- Warning/watch card: More opens a full-screen reader with big type and the official text laid out cleanly (Hazard / Source / Impact on their own lines).

## v238
- What's Next: 'Rain arriving now' style headlines also switch to how long it lasts ('Storms until 4 AM'), so it never repeats Right Now.

## v239
- Briefing maps: towns now show (they come from the app's built-in town list; the downloaded list had bad population numbers, so no city passed the cutoff).
- Hour by hour: temperatures sit on the orange line again (no separate row).
- "Most likely" covers the real rain hours (not just the peak hour), so the bottom line matches the chart.
- Severe bottom line: "Rain and storms on and off 10 PM–4 AM; move indoors at the first thunder and stay off flooded roads."
- Map Room storms-organizing popup matches the radar card: chips, timing, watch odds, first 4 towns.
- Map Room thumbnails: no unnamed white town dots.
- Map Room: the storms-organizing box and watches only show on the storm maps (storms organizing, watch, radar, today's severe and tornado outlooks), not on every map.

## v240
- Storms-organizing briefing: the notice drives the bullets. When = now through the notice's end time. Main threat = the notice's numbers in one line (Isolated damaging gusts up to 60 mph and a brief tornado (up to EF1). A watch is unlikely (20%).). The separate Strongest expected line is gone.
- Briefing maps: towns spread out (no cluster of suburbs).
- Subhead no longer cut off mid-sentence.

## v241
- Map Room tropics thumbnail: clean yellow/orange/red outlook areas (were muddy brown), only our site dot (no U.S. city labels crammed in a corner), no agency name in the subtitle.

## v242
- Automatic (intermediate) briefings are facts only, styled as a clean fact card (label / fact rows), no advice:
  - Severe outlook: "Level 1 severe risk added for Greenville today"; risk level with the outlook's own definition; threats within 25 miles (tornado/wind/hail %); most likely hours here from the hourly forecast; higher level nearby.
  - Flooding rain outlook: same pattern with the level definition, rain here, heaviest hours here.
  - Storms organizing: area towns, valid time, concerning line with watch chance, most likely strongest gust/hail/tornado, a two-sentence summary of the discussion.
  - Watches, warnings, advisories: in effect until, WHAT, area, IMPACTS, expected gusts/hail.
  - Tropics: chance of development (2- and 7-day) and where; active storms and advisory number. No comparison to the site.
  - Nearby outlook changes: where and how far only.
- No risk meters, no "what it means for you", no extra maps on these; the hour-by-hour stays.

## v243
- Alerts near you: tapping an alert opens the full radar zoomed to that alert's area, outlines it in its color, and opens its card. Alerts with no outline still expand their details.

## v244
- Automatic briefings use the 24/7 channel's card: a small tag (WHAT WE'RE WATCHING / STORMS ORGANIZING / IN EFFECT / TROPICS), a big plain title (MARGINAL RISK · FLOODING RAIN), the level bar, one plain line, then two or three short rows. No 'The facts' label, no '(hourly forecast)' tags.

## v245
- Automatic briefings: short headlines (Marginal flood risk tomorrow / Level 2 severe risk today / Storms organizing nearby / Tornado Watch until 9 PM / Tropics: 30% chance in 7 days) with one plain intro line; risk meters back on severe and flood ones; no what-to-do.
- Fixed: an issued time like 8:12 AM printed as 8:midnight.

## v246
- New SKI CONDITIONS section (next to Hunt & Fish): 39 resorts grouped Southeast / Mid-Atlantic & Northeast / Rockies / West Coast; defaults to the nearest; summit forecast; 10-day score out of 10 with reasons (fresh snow overnight, snowmaking hours by wet-bulb, rain on the slopes, lift wind holds, warm/slushy, bitter cold, bluebird); link to the resort's own snow report.
- New BEACH & BOATING section: 23 beaches from Cape Cod to Waikiki; Beach / Boating toggle; 10-day scores (storms, rain, wind, temperature, surf / wind, gusts, seas); water temperature, waves and period, official tide times, UV; rip current, high surf and small craft alerts shown when in effect.
- Sponsor slot ("PRESENTED BY") on Ski, Beach & Boating, and Hunt & Fish — set in channel.json under "sponsors" (name, optional logo link, website). Blank = nothing shows.

## v247
- Ski: simpler. Each day shows the score and "Fresh powder: 3"" (or "No new snow"); tap a day for summit temps, wind and snow, with the score breakdown tucked under "Score breakdown". No day opens by itself.
- Lakes in Beach & Boating: Lake Hartwell, Lake Keowee, Lake Murray, Lake Norman, Lake Lanier — boating/beach scores from wind, gusts, storms, temps; lake level and its change this week from the nearest USGS gauge when one is reporting. Coastal beaches stay the default.
- Hunt & Fish day details: dawn and dusk wind (direction and speed) for picking a stand, legal light window (30 minutes before sunrise to 30 after sunset, most states) for deer, and the pressure trend (falling / rising / steady) for fishing.

## v248
- Quiet daily briefing headline: 'Dry stretch ahead' (or 'Drying out, dry stretch ahead' when it's raining now or just did), never 'Dry stretch continues'.

## v249
- Wildfire check:
  - FIRE DANGER section on the home screen (next to Hunt & Fish): 7 days rated Low / Moderate / High / Very high / Extreme from lowest humidity, peak gusts, days since a quarter inch of rain, and the official fire weather outlook; tap a day for the numbers; Red Flag Warning / Fire Weather Watch shown when in effect; sponsor slot ("fire" in channel.json).
  - Map Room: FIRE WEATHER · TODAY / TOMORROW cards when the fire weather outlook has an area (Elevated / Critical / Extreme, dry thunderstorm areas dashed), framed on the area and the site.
  - Red Flag Warnings and Fire Weather Watches at the site now create a FIRE briefing (facts card), and FIRE is a library filter.
- Quiet daily briefing: one "Looking further out" line from the 6–10 / 8–14 day temperature outlook, only when the lean at the site is 40%+ and it's new or changed (or a week has passed). Says "a change from the last outlook" when it flips.

## v250
- New sign-up page at /start/ (what someone sees after scanning the conference QR code): welcome screen (what we are, ALL CLEAR / HEADS UP / TAKE ACTION, four benefits), Get started or Sign in; Step 1 name, organization, role, email, phone; Step 2 type (city/county/agency, school/university, business/utility) and main location; Step 3 alerts (warnings, lightning, briefings, schedule watch) and optional schedule upload; Step 4 membership: $2,500 crossed out, partner code SDR2027 makes it $0, Complimentary, SDR Preferred Partner; then Welcome screen and Open my dashboard. Sign in uses a 6-digit code (demo: any code). Demo only: nothing is saved to a server yet (Andrew's accounts plug in here).
- /start/ is now a full landing page in the showcase deck's look (hero with the phones, See Clearly / Decide Confidently / Plan Ahead with the deck's phone screens, cost stats, partner membership card, Confidence in chaos.), with the sign-up flow restyled to match.

## v251
- Landing page (/start/): cleaner and crisper. Headline no longer runs under the phones; clean line icons instead of emoji; softer glow; phone images blend into the page with no visible boxes.
- Ski: branded map card on top. "Snow on the ground" (official snow analysis) first, then Day 1 / Day 2 / Day 3 chances of 4"+ snow; resorts in the region labeled, the selected one highlighted.
- Fire Danger: branded map card on top with active wildfires (sized by acres, colored by containment) and today's fire weather outlook; list of active fires within 200 miles — tap one for percent contained (bar), acres, when it started, county.

## v252
- Landing page (/start/) rebuilt as Why / What / How: short hero; 'A rain icon isn't a plan'; six features with real dashboard screens in phone frames (your call right now, advanced technology, Schedule Watch, live chat with real meteorologists, briefings, live Q&A sessions); three setup steps; partner membership card. Disaster-cost stats removed.
- Landing: each feature's words come before its screen (reads top to bottom on a phone); feature numbers removed.
- Landing simplified to two screens: hero (headline, one line, Get started, the phones) then four features in one line each, the membership offer and the tagline.
- Landing: hero, then the three pillars (See clearly / Decide confidently / Plan ahead) with the deck's phone screens and three highlights each, then Get started today with the partner offer.
- Landing: real SDR Weather Intelligence logo (on a white chip); hero shows the real dashboard on a laptop and a phone; the three pillars show real dashboard screens (radar with warning, meteorologist chat, Schedule Watch). Words come before each screen on phones.

## v253
- Landing page (/start/): bigger logo, light design, Mac-style laptop, bigger phone.
- Written for emergency managers, cities, counties and leaders.
- Cleaner phone screens: radar shows just the map and warning; Schedule Watch shows event examples (festival, parade, road crews, football, shelter).
- Offer: $2,500 crossed out, "Complimentary for SDR partners."
- Sign-up now has a real desktop layout (side panel + form card); phone layout unchanged in flow.
- Dashboard Schedule Watch preview now uses festival / football / road crew examples.

## v254
- Ski: rebuilt on the 24/7 channel's logic. Official point forecast per resort, new snow read from the forecast wording, snowmaking hours from the wet-bulb (27° or colder). No scores.
- Ski: branded hero map by zone (Southeast, Northeast, Rockies, West Coast). Each resort shows new snow or tonight's snowmaking hours. Tap a resort for 7 days. Snow pack / snow forecast layers kept.
- Ski: resort list now matches the 24/7 channel (added Wolf Ridge, Bryce, Timberline; fixed Killington's location).
- Beach & Boating: no scores. Branded hero map by zone with waves as 2-foot ranges (2–4 ft, 3–5 ft) and lake water (Glassy / Light chop / Choppy / Rough). Tap a spot for 7 days of waves, wind, tides and sky icons. Lake notes match the 24/7 channel.
- Real icons on the Ski and Beach bars (they showed as blank squares).
- Wind and gust hour-by-hour charts: numbers only above the bars, so they stop running into each other.
- Forecast Desk: demo mode at desk.html?demo (no password, sample questions).

## v255
- Icons for Schedule Watch, Around You and Fire Danger (they showed as blank squares).
- LIVE tab in the bottom bar is red with a pulsing dot whenever the 24/7 channel is connected.
- Ski: "14 hrs" now says what it means: "14 hrs · snowmaking" (hours cold enough to make snow tonight). "Too warm to make snow" spelled out.
- Ski: resort report box (Open/Closed, trails, lifts, base, new snow, surface) when the 24/7 channel's helper publishes site/resorts.json. Until then, a link to each resort's snow report. See RESORT-REPORT-for-247-channel.md.

## v256
- Tropics: Atlantic, Caribbean and Gulf only. Eastern/central Pacific areas no longer lead tropical briefings or maps.
- Fire danger recalibrated: humid days (60%+) and wet days (0.1"+) are Low; humidity counts at 30% or lower; the official fire weather outlook only raises the level on a dry day (Elevated → Moderate, Critical → High, Extreme → Very high).
- Wildfire map: tap a fire on the map to open its details.
- Rain bucket: early in the month (first 14 days) compares with a full normal month instead of "to date" (Orlando showed 734%).
- Briefing print: a sheet that runs a little long is scaled to fit one page on iPhone too (iPhone ignored the old method, spilling the bottom line to page 2).

## v257
- Ski map: clean dots instead of word pills. Blue dot with a snowflake = cold enough to make snow tonight; gray = too warm; purple with a number = new snow.
- Ski wording: "Snowmaking · 9 of 9 hrs" (hours tonight, 6 PM–8 AM, cold and dry enough to run snow guns). Day rows say it in a sentence.
- Snow on the ground layer drawn in strong blue so thin early-season snow shows on the gray land.

## v258
- Ski resort reports now come from the GitHub job: site/tools/ski_reports.js opens each resort's snow report in a real browser (same reader as the 24/7 channel's ski.js) and publishes /resorts.json every run, Nov–Mar. Needs the updated workflow file (nbm.yml in this zip → .github/workflows/nbm.yml).
- Ski board: TV-style rows: resort, OPEN / opening date, trails, base, new snow. Open resorts first.
- Tap a spot on the Ski, Beach & Boating or Wildfire map: a warning-style card pops up (status, the "what" line, big numbers) with a button for the 7-day forecast.
- Ski map dots: green = open, gray = closed, snowflake = cold enough to make snow, purple number = new snow.

## v259
- Right Now: the official observation in full: conditions (Fog and mist, Dense fog), visibility when under 7 miles (yellow under 3, red at ¼ mile or less), humidity and dew point. Fog icon.
- Radar map: nearby official stations reporting under 5 miles of visibility show a small fog chip with the number ("Fog 1¾ mi", "Dense fog under ¼ mi").

## v260
- Right Now during a warning: "12 MIN LEFT" next to the end time and a progress bar from start to end. Lightning keeps its mm:ss all-clear countdown (no bar), so the two never look alike. During warnings the card drops humidity/dew point to stay focused.
- Briefings: tapping a briefing in the list opens exactly that one (the list re-sorts as new ones arrive, which could open a different one). Home "Read ›" opens the newest briefing.
- Briefing hour-by-hour: no more "Rain expected: None" with a 90% storm chance. Shows "Storms" / "Showers" (heavier where storms hit) or "Spotty".
- Radar: frost, freeze, wind and other non-storm products draw as a soft tint with no county outlines until you zoom in close.

## v261
- Right Now redesigned: the call as a big pill (✓ ALL CLEAR green, ⚠ HEADS UP yellow with the reason under it), then big readable conditions: temperature, conditions, feels-like and wind, the weather icon, and a strip of humidity / dew point / visibility. Shows which official station it's observed at.
- Take Action keeps the red warning layout (reason, end time, minutes left, bar) with the conditions underneath.

## v262
- Right Now, TV-simple: temperature, conditions, wind and feels like (when it differs). Gusts (20+ mph), visibility (under 5 mi) and WBGT (80°+) pop up only when they matter.
- Heat stress drives the call: WBGT 87°+ → HEADS UP, 90°+ → TAKE ACTION (warnings and lightning still come first).
- Night icon shows the real moon phase, tucked behind a cloud when partly cloudy, with the phase name.

## v263
- 10-day reads left to right: day · icon with rain % · morning low ——bar—— afternoon high · rain (or snow) total. The bar is scaled to the coldest and warmest of the 10 days, so warmer/colder days are easy to see. Tap a day for the full details (unchanged).
- Right Now: sky spelled out ("Clear night", "Clear skies", "Fog and mist", "Dense fog"); feels like / gusts / visibility / WBGT appear as bubbles only when they matter. Moon shows its phase with no label.
- Phones: on a quiet (All Clear) day the radar sits below the hour-by-hour and 10-day; on Heads Up / Take Action it moves right under Right Now.

## v264
- Hour by hour redesigned: one card per hour, read left to right: time · icon · temp · rain chance (⚡ when thunder) · rain amount with a small bar (snow in white). Day breaks marked. Tap a card for full details.
- "Ask the forecast desk" bar right under Right Now / What's Next; Chat tab highlighted green.
- Fixed: on phones the old small conditions could show above the new Right Now.

## v265
- LIVE CHAT bar: polished (pulsing LIVE CHAT label, green Chat › button). Wording follows chatMode in channel.json: "review" → "Chat with our certified meteorologists"; "auto" → "Ask the SDR forecast desk".
- New tiles near the bottom: Rain gauge (past 24 hours at the official station, with a filling glass) and Air quality (dial, 0–300+, Good → Hazardous).

## v266
- LIVE CHAT bar slimmed to one line: "● LIVE CHAT  Ask the forecast desk ›" ("Ask our meteorologists" in review mode).
