import { queueRegistration, savePref, getPref } from '/frontend/db.js';
const API_BASE = 'http://127.0.0.1:8000';

const el = (id) => document.getElementById(id);
const form = el('regForm');
const quickBtn = el('quickBtn');
const successEl = el('success');
const errorEl = el('error');
const toastEl = el('toast');

const consent = document.getElementById('consent');
const submitBtn = document.getElementById('submitBtn');

// Enable Submit only when consent is checked
function checkConsentGate() {
  submitBtn.disabled = !consent.checked;
}
consent.addEventListener('change', checkConsentGate);
checkConsentGate(); // initial check

const params = new URLSearchParams(location.search);
const utm = {
  utm_source: params.get('utm_source') || null,
  utm_medium: params.get('utm_medium') || null,
  utm_campaign: params.get('utm_campaign') || null
};

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('/frontend/sw.js'));
}

function showSuccess(msg = 'Saved locally. Will sync when online.') {
  successEl.textContent = msg; successEl.style.display = 'block';
  errorEl.style.display = 'none';
}
function showError(msg) {
  errorEl.textContent = msg; errorEl.style.display = 'block';
  successEl.style.display = 'none';
}
function toast(msg) { toastEl.textContent = msg; setTimeout(() => toastEl.textContent = '', 2500); }

function focusAutofill() { el('name').focus(); }

const pcInput = el('pc'); const acInput = el('ac'); const wardInput = el('ward');
const pcList = el('pcList'); const acList = el('acList'); const wardList = el('wardList');

async function fetchJSON(url) {
  const r = await fetch(url, { headers: { 'Accept': 'application/json' } });
  if (!r.ok) throw new Error('Network');
  return r.json();
}

async function loadPC() {
  const pcs = await fetchJSON(`${API_BASE}/list/pc`);
  pcList.innerHTML = pcs.map(p => `<option value="${p.name}" data-id="${p.id}" data-code="${p.code}"></option>`).join('');
  const last = await getPref('pc_id');
  if (last) {
    const item = pcs.find(x => x.id === last);
    if (item) pcInput.value = item.name;
  }
}

async function loadAC(pc_id) {
  const acs = await fetchJSON(`${API_BASE}/list/ac?pc_id=${encodeURIComponent(pc_id)}`);
  acList.innerHTML = acs.map(a => `<option value="${a.name}" data-id="${a.id}" data-code="${a.code}"></option>`).join('');
}

let wardSearchAbort = null;
async function loadWard(ac_id, q = '', page = 1) {
  if (wardSearchAbort) wardSearchAbort.abort();
  wardSearchAbort = new AbortController();
  const pg = await fetchJSON(`${API_BASE}/list/ward_gp?ac_id=${encodeURIComponent(ac_id)}&page=${page}&page_size=20&q=${encodeURIComponent(q)}`);
  wardList.innerHTML = pg.items.map(w => `<option value="${w.name}" data-id="${w.id}" data-code="${w.code}"></option>`).join('');
}

function idFromList(datalist, value) {
  const options = Array.from(datalist.querySelectorAll('option'));
  const match = options.find(o => o.value === value);
  return match ? match.getAttribute('data-id') : null;
}

pcInput.addEventListener('change', async () => {
  const pc_id = idFromList(pcList, pcInput.value);
  if (pc_id) {
    await savePref('pc_id', pc_id);
    acInput.value = ''; wardInput.value = '';
    await loadAC(pc_id);
  }
});

acInput.addEventListener('change', async () => {
  const pc_id = idFromList(pcList, pcInput.value);
  const ac_id = idFromList(acList, acInput.value);
  if (pc_id && ac_id) {
    await savePref('ac_id', ac_id);
    wardInput.value = '';
    await loadWard(ac_id);
  }
});

let wardDebounce;
wardInput.addEventListener('input', () => {
  const ac_id = idFromList(acList, acInput.value);
  clearTimeout(wardDebounce);
  wardDebounce = setTimeout(() => {
    if (ac_id) loadWard(ac_id, wardInput.value.trim());
  }, 250);
});

// Auto-detect: if denied or unavailable, auto-fallback to manual cascade and focus PC
quickBtn.addEventListener('click', async (e) => {
  e.preventDefault();
  focusAutofill();
  if (!('geolocation' in navigator)) { await loadPC(); pcInput.focus(); return; }
  navigator.geolocation.getCurrentPosition(async (pos) => {
    try {
      const res = await fetchJSON(`${API_BASE}/lookup?lat=${pos.coords.latitude}&lng=${pos.coords.longitude}`);
      // hydrate PC / AC / Ward
      const pcs = await fetchJSON(`${API_BASE}/list/pc`);
      pcList.innerHTML = pcs.map(p => `<option value="${p.name}" data-id="${p.id}" data-code="${p.code}"></option>`).join('');
      const targetPC = pcs.find(x => x.id === res.pc_id);
      if (targetPC) pcInput.value = targetPC.name;

      await loadAC(res.pc_id);
      const acs = await fetchJSON(`${API_BASE}/list/ac?pc_id=${encodeURIComponent(res.pc_id)}`);
      const targetAC = acs.find(x => x.id === res.ac_id);
      if (targetAC) acInput.value = targetAC.name;

      await loadWard(res.ac_id);
      const wards = wardList.querySelectorAll('option');
      const match = Array.from(wards).find(o => o.getAttribute('data-id') === res.ward_gp_id);
      if (match) wardInput.value = match.value;

      toast('Detected from your location. You can change.');
    } catch {
      await loadPC(); pcInput.focus();
    }
  }, async () => {
    await loadPC(); pcInput.focus();
  }, { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 });
});

function normalizePhone(v) {
  const digits = (v || '').replace(/\D/g, '');
  return digits.slice(-10);
}

async function tryOnlinePost(payload) {
  try {
    const res = await fetch(`${API_BASE}/api/register`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
    });
    return res.ok;
  } catch { return false; }
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  // Check consent first
  if (!consent.checked) {
    showError('Please accept consent to proceed.');
    return;
  }

  const name = el('name').value.trim();
  const phone10 = normalizePhone(el('phone').value);
  const email = el('email').value.trim() || null;

  const pc_id = idFromList(pcList, pcInput.value);
  const ac_id = idFromList(acList, acInput.value);
  const ward_gp_id = idFromList(wardList, wardInput.value);

  if (!name || name.length < 2 || !phone10 || phone10.length !== 10 || !pc_id || !ac_id || !ward_gp_id) {
    showError('Complete required fields and ensure phone has 10 digits.');
    return;
  }

  const payload = {
    id: crypto.randomUUID(),
    name, phone: phone10, email,
    pc_id, ac_id, ward_gp_id,
    ...utm,
    createdAt: Date.now(),
    synced: false
  };

  await queueRegistration(payload);
  showSuccess();

  const ok = await tryOnlinePost(payload);
  if (!ok) {
    if ('serviceWorker' in navigator && 'SyncManager' in window) {
      const r = await navigator.serviceWorker.getRegistration();
      if (r) await r.sync.register('sync-registrations');
    } else if (navigator.onLine && navigator.serviceWorker?.controller) {
      navigator.serviceWorker.controller.postMessage('flush');
    }
  }
  form.reset();
  checkConsentGate(); // re-disable submit after form reset
});

// initial population (helps users who skip auto-detect)
loadPC().catch(() => {});
// Mark fields as touched on blur to enable validation styling
document.querySelectorAll('input[required], select[required]').forEach((field) => {
  field.addEventListener('blur', () => {
    field.classList.add('touched');
  });
});
