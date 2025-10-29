/* global self, caches, fetch */
const CACHE = 'acr-shell-v2';
const SHELL = [
  '/frontend/index.html',
  '/frontend/main.js',
  '/frontend/db.js',
  '/frontend/manifest.webmanifest'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  const { request } = e;
  if (request.method === 'GET' && request.destination !== 'document' && !request.url.includes('/api/')) {
    e.respondWith(
      caches.match(request).then((cached) => cached || fetch(request).catch(() => cached))
    );
  }
});

async function flushQueue() {
  const { listUnsynced, markSynced } = await import('/frontend/db.js');
  const items = await listUnsynced(20);
  if (!items.length) return;
  const idsSynced = [];
  for (const item of items) {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item)
      });
      if (res.ok) idsSynced.push(item.id);
    } catch (_) { break; }
  }
  if (idsSynced.length) await markSynced(idsSynced);
}

self.addEventListener('sync', (e) => {
  if (e.tag === 'sync-registrations') e.waitUntil(flushQueue());
});

self.addEventListener('message', (e) => {
  if (e.data === 'flush') e.waitUntil(flushQueue());
});
