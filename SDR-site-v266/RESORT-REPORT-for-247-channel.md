# Resort report → SDR dashboards (for the 24/7 channel's resort helper)

The dashboards' Ski section now shows each resort's own report (open/closed, trails, lifts, base) when it is fresh.
The channel's Mac helper already reads every resort's snow report hourly. Have it also write ONE file:

**Where:** `site/resorts.json` in the GitHub repo `chrisjustuswx2026/nbm-ranges` (served at `https://chrisjustuswx2026.github.io/nbm-ranges/resorts.json`).

**Format:**
```json
{
  "updated": "2026-11-05T19:00:00Z",
  "resorts": {
    "Beech Mountain": { "open": true, "trails_open": 6, "trails_total": 17, "lifts_open": 3, "lifts_total": 7,
                        "base": "18–30\"", "new24": 0, "surface": "Machine groomed", "updated": "2026-11-05T18:40:00Z" },
    "Cataloochee":    { "open": false, "opening": "2026-11-21", "updated": "2026-11-05T18:40:00Z" }
  }
}
```

Rules:
- Resort names must match the channel list exactly (Cataloochee, Sugar Mountain, Beech Mountain, App Ski Mountain, Wolf Ridge, Ober Mountain, Wintergreen, Massanutten, Bryce, Snowshoe, Canaan Valley, Timberline, Winterplace, Killington, Stowe, Okemo, Jay Peak, Mount Snow, Sugarloaf, Sunday River, Hunter, Whiteface).
- Every field is optional except `updated`. Leave out anything the resort page doesn't give.
- The dashboard ignores any resort report older than 36 hours (same rule as the channel) and shows a link to the resort's snow report instead.
- `opening` is a date (YYYY-MM-DD) for resorts not open yet.
