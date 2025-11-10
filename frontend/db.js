// IndexedDB setup for offline capability
const DB_NAME = 'CampaignRegDB';
const DB_VERSION = 5;
const STORE_NAME = 'registrations';
const PREF_STORE = 'preferences';

let db;

// Open/create database
function openDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    
    req.onupgradeneeded = (e) => {
      db = e.target.result;
      
      // Create registrations store
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        const store = db.createObjectStore(STORE_NAME, { keyPath: 'id', autoIncrement: true });
        store.createIndex('phone', 'phone', { unique: false });
        store.createIndex('state_id', 'state_id', { unique: false });
        store.createIndex('district_id', 'district_id', { unique: false });
        store.createIndex('mandal_id', 'mandal_id', { unique: false });
        store.createIndex('village_name', 'village_name', { unique: false });
        store.createIndex('created_at', 'created_at', { unique: false });
      }
      
      // Create preferences store
      if (!db.objectStoreNames.contains(PREF_STORE)) {
        db.createObjectStore(PREF_STORE, { keyPath: 'key' });
      }
    };
    
    req.onsuccess = (e) => {
      db = e.target.result;
      resolve(db);
    };
    
    req.onerror = (e) => reject(e.target.error);
  });
}

// Queue registration for offline sync
export async function queueRegistration(payload) {
  if (!db) await openDB();
  
  return new Promise((resolve, reject) => {
    const tx = db.transaction([STORE_NAME], 'readwrite');
    const store = tx.objectStore(STORE_NAME);
    const req = store.add({ ...payload, created_at: Date.now() });
    
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

// Get all queued registrations
export async function getQueuedRegistrations() {
  if (!db) await openDB();
  
  return new Promise((resolve, reject) => {
    const tx = db.transaction([STORE_NAME], 'readonly');
    const store = tx.objectStore(STORE_NAME);
    const req = store.getAll();
    
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

// Delete registration after successful sync
export async function deleteRegistration(id) {
  if (!db) await openDB();
  
  return new Promise((resolve, reject) => {
    const tx = db.transaction([STORE_NAME], 'readwrite');
    const store = tx.objectStore(STORE_NAME);
    const req = store.delete(id);
    
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

// Save preference
export async function savePref(key, value) {
  if (!db) await openDB();
  
  return new Promise((resolve, reject) => {
    const tx = db.transaction([PREF_STORE], 'readwrite');
    const store = tx.objectStore(PREF_STORE);
    const req = store.put({ key, value });
    
    req.onsuccess = () => resolve();
    req.onerror = () => reject(req.error);
  });
}

// Get preference
export async function getPref(key) {
  if (!db) await openDB();
  
  return new Promise((resolve, reject) => {
    const tx = db.transaction([PREF_STORE], 'readonly');
    const store = tx.objectStore(PREF_STORE);
    const req = store.get(key);
    
    req.onsuccess = () => resolve(req.result?.value);
    req.onerror = () => reject(req.error);
  });
}

// Initialize DB on load
openDB();
