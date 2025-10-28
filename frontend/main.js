import { queueRegistration } from '/frontend/db.js';

const API_BASE = 'http://127.0.0.1:8000';
const form = document.getElementById('regForm');
const quickBtn = document.getElementById('quickBtn');
const manualLink = document.getElementById('manualLink');
const successEl = document.getElementById('success');
const errorEl = document.getElementById('error');

const params = new URLSearchParams(location.search);
const utm = {
  utm_source: params.get('utm_source') || null,
  utm_medium: params.get('utm_medium') || null,
  utm_campaign: params.get('utm_campaign') || null
};

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/frontend/sw.js');
  });
}

function showSuccess(msg = 'Saved locally. Will sync when online.') {
  successEl.textContent = msg;
  successEl.style.display = 'block';
  errorEl.style.display = 'none';
}
function showError(msg) {
  errorEl.textContent = msg;
  errorEl.style.display = 'block';
  successEl.style.display = 'none';
}

function oneTapAutofillHint() {
  document.getElementById('name').focus();
}

async function getGeoAndFill() {
  if (!('geolocation' in navigator)) return;
  return new Promise((resolve) => {
    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        try {
          // Placeholder: plug real reverse geocoding later
          // For now, we leave fields editable and do nothing if API not set.
          // You can integrate Google/Mappls here.
          resolve(pos.coords);
        } catch {
          resolve(null);
        }
      },
      () => resolve(null),
      { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
    );
  });
}

quickBtn.addEventListener('click', async (e) => {
  e.preventDefault();
  oneTapAutofillHint();
  await getGeoAndFill();
});

manualLink.addEventListener('click', (e) => {
  e.preventDefault();
  document.getElementById('district').focus();
});

function normalizePhone(v) {
  return (v || '').replace(/\D/g, '').slice(-10);
}

async function tryOnlinePost(payload) {
  try {
    const res = await fetch('/api/http://127.0.0.1:8000/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.ok;
  } catch {
    return false;
  }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('name').value.trim();
  const phone = normalizePhone(document.getElementById('phone').value);
  const email = document.getElementById('email').value.trim() || null;
  const district = document.getElementById('district').value.trim();
  const mandal = document.getElementById('mandal').value.trim();

  if (!name || !phone || phone.length !== 10 || !district || !mandal) {
    showError('Please complete required fields and ensure phone has 10 digits.');
    return;
  }

  const reg = {
    id: crypto.randomUUID(),
    name, phone, email, district, mandal,
    ...utm,
    createdAt: Date.now(),
    synced: false
  };

  await queueRegistration(reg);
  showSuccess();

  const onlineOK = await tryOnlinePost(reg);
  if (!onlineOK) {
    if ('serviceWorker' in navigator && 'SyncManager' in window) {
      const regSW = await navigator.serviceWorker.getRegistration();
      if (regSW) await regSW.sync.register('sync-registrations');
    } else if (navigator.onLine && navigator.serviceWorker?.controller) {
      navigator.serviceWorker.controller.postMessage('flush');
    }
  }
  form.reset();
});
