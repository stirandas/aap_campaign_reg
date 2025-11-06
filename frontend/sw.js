/* global self, caches, fetch */

const CACHE = 'acr-shell-v2';

const SHELL = [
  './',
  './index.html',
  './main.js',
  './db.js',
  './manifest.webmanifest'
];

// Detect environment dynamically
const API_BASE_URL = self.location.hostname === 'localhost' || self.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000'
  : self.location.origin;  // This will be https://aapreg.web.app from Firebase

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
  const { listUnsynced, markSynced } = await import('./db.js');
  const items = await listUnsynced(20);
  if (!items.length) return;
  const idsSynced = [];
  for (const item of items) {
    try {
      const res = await fetch(`${API_BASE_URL}/api/register`, {
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
