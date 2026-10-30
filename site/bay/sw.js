// SDR Weather Intelligence — service worker (v120)
// Does two things only: lets the page show real system notifications, and opens the dashboard when one is tapped.
// No caching: the dashboard is always the live page.
self.addEventListener("install", e => { self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(self.clients.claim()); });

self.addEventListener("notificationclick", e => {
  e.notification.close();
  const data = e.notification.data || {};
  e.waitUntil((async () => {
    const all = await self.clients.matchAll({ type: "window", includeUncontrolled: true });
    const here = all.find(c => c.url.indexOf(self.registration.scope) === 0) || all[0];
    if (here) { try { await here.focus(); } catch (x) {} here.postMessage({ sdr: "open", pane: data.pane || "overview", target: data.target || "" }); return; }
    const url = self.registration.scope + (data.pane ? "#" + data.pane : "");
    await self.clients.openWindow(url);
  })());
});

// a future push service lands here; the page's own notifications don't need it
self.addEventListener("push", e => {
  let d = {}; try { d = e.data ? e.data.json() : {}; } catch (x) { d = { body: e.data ? e.data.text() : "" }; }
  e.waitUntil(self.registration.showNotification(d.title || "SDR Weather Intelligence", {
    body: d.body || "", icon: "./icons/icon-192.png", badge: "./icons/badge-96.png", tag: d.tag || "sdr", renotify: true, data: { pane: d.pane || "overview" }
  }));
});
