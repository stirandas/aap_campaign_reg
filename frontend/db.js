export const DB_NAME = 'app_campaign_reg';
const STORE = 'registrations';
const PREFS = 'prefs';
const VERSION = 2;

export function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, VERSION);
    req.onupgradeneeded = () => {
      const db = req.result;
      if (!db.objectStoreNames.contains(STORE)) {
        const os = db.createObjectStore(STORE, { keyPath: 'id' });
        os.createIndex('by_synced', 'synced', { unique: false });
        os.createIndex('by_createdAt', 'createdAt', { unique: false });
      }
      if (!db.objectStoreNames.contains(PREFS)) {
        db.createObjectStore(PREFS, { keyPath: 'key' });
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

export async function queueRegistration(reg) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    tx.objectStore(STORE).put(reg);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

export async function listUnsynced(limit = 20) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const out = [];
    const tx = db.transaction(STORE, 'readonly');
    const idx = tx.objectStore(STORE).index('by_synced');
    const req = idx.openCursor(IDBKeyRange.only(false));
    req.onsuccess = (e) => {
      const cursor = e.target.result;
      if (cursor && out.length < limit) { out.push(cursor.value); cursor.continue(); }
      else { resolve(out); }
    };
    req.onerror = () => reject(req.error);
  });
}

export async function markSynced(ids) {
  if (!ids.length) return;
  const db = await openDB();
  await new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, 'readwrite');
    const os = tx.objectStore(STORE);
    ids.forEach((id) => {
      const g = os.get(id);
      g.onsuccess = () => { const v = g.result; if (v) { v.synced = true; os.put(v); } };
    });
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

export async function savePref(key, value) {
  const db = await openDB();
  const tx = db.transaction(PREFS, 'readwrite');
  tx.objectStore(PREFS).put({ key, value });
  return new Promise((resolve, reject) => {
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

export async function getPref(key) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(PREFS, 'readonly');
    const req = tx.objectStore(PREFS).get(key);
    req.onsuccess = () => resolve(req.result?.value ?? null);
    req.onerror = () => reject(req.error);
  });
}
