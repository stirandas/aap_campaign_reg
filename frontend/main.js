import { queueRegistration, savePref, getPref } from './db.js';

// API Base URL - Checks for localhost, 127.0.0.1, OR 192.168.x.x
const API_BASE = (
  window.location.hostname === 'localhost' || 
  window.location.hostname === '127.0.0.1' ||
  window.location.hostname.startsWith('192.168.')  //This accesses only FE, backend will fail as it is on 127.0.0.1
) 
  ? 'http://127.0.0.1:8000'  // Local dev backend  //Can't keep DHCP IP address here as it might change frequently
  : 'https://aap-campaign-reg-backend-444299072309.asia-south1.run.app';  // Production backend

// DOM Elements
const el = (id) => document.getElementById(id);
const form = el('regForm');
const successEl = el('success');
const errorEl = el('error');
const submitBtn = el('submitBtn');

// Form Fields
const nameInput = el('name');
const phoneInput = el('phone');
const emailInput = el('email');
const stateSelect = el('state');
const districtSelect = el('district');
const mandalSelect = el('mandal');
const villageInput = el('village');
const consentAccuracyCheckbox = el('consentAccuracy');
const consentShareCheckbox = el('consentShare');

// UTM Parameters
const params = new URLSearchParams(location.search);
const utm = {
  utm_source: params.get('utm_source') || null,
  utm_medium: params.get('utm_medium') || null,
  utm_campaign: params.get('utm_campaign') || null,
};

// ========== ERROR MANAGEMENT ==========
function clearError() {
  errorEl.style.display = 'none';
  errorEl.textContent = '';
}

function showError(message) {
  errorEl.textContent = '❌ ' + message;
  errorEl.style.display = 'block';
}

// ========== VALIDATION & SUBMIT BUTTON CONTROL ==========
function validateForm() {
  const isNameValid = nameInput.value.trim().length >= 2;
  const isPhoneValid = /^[0-9]{10}$/.test(phoneInput.value);
  const isStateValid = stateSelect.value !== '';
  const isDistrictValid = districtSelect.value !== '';
  const isMandalValid = mandalSelect.value !== '';
  const isVillageValid = villageInput.value.trim().length >= 2;
  const isConsentChecked = consentAccuracyCheckbox.checked && consentShareCheckbox.checked;

  // Add visual feedback for valid fields
  nameInput.classList.toggle('valid', isNameValid);
  phoneInput.classList.toggle('valid', isPhoneValid);
  stateSelect.classList.toggle('valid', isStateValid);
  districtSelect.classList.toggle('valid', isDistrictValid);
  mandalSelect.classList.toggle('valid', isMandalValid);
  villageInput.classList.toggle('valid', isVillageValid);
  
  // Enable submit only if ALL mandatory fields valid + consent checked
  const allValid = isNameValid && isPhoneValid && isStateValid && 
                   isDistrictValid && isMandalValid && isVillageValid && 
                   isConsentChecked;
  
  submitBtn.disabled = !allValid;
  
  return allValid;
}

// Add validation listeners to all mandatory fields
nameInput.addEventListener('input', validateForm);
phoneInput.addEventListener('input', validateForm);
stateSelect.addEventListener('change', validateForm);
districtSelect.addEventListener('change', validateForm);
mandalSelect.addEventListener('change', validateForm);
villageInput.addEventListener('input', validateForm);
consentAccuracyCheckbox.addEventListener('change', validateForm);
consentShareCheckbox.addEventListener('change', validateForm);

// ========== LOAD STATES ON PAGE LOAD ==========
async function loadStates() {
  try {
    const res = await fetch(`${API_BASE}/list/state`);
    if (!res.ok) throw new Error('Failed to load states');
    const states = await res.json();
    
    stateSelect.innerHTML = '<option value="">-- Select State --</option>';
    states.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s.state_id;
      opt.textContent = s.state_name;
      stateSelect.appendChild(opt);
    });
  } catch (err) {
    showError('Failed to load states: ' + err.message);
  }
}

// ========== STATE CHANGE: LOAD DISTRICTS & RESET CHILDREN ==========
stateSelect.addEventListener('change', async () => {
  const stateId = stateSelect.value;
  
  // Clear any previous errors immediately
  clearError();
  
  // Reset all child fields
  resetDistrict();
  resetMandal();
  resetVillage();
  
  if (!stateId) {
    validateForm();
    return;
  }
  
  // Show loading state
  districtSelect.innerHTML = '<option value="">-- Loading districts... --</option>';
  districtSelect.disabled = true;
  
  try {
    const res = await fetch(`${API_BASE}/list/district?state_id=${stateId}`);
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Server returned ${res.status}`);
    }
    const districts = await res.json();
    
    if (!districts || districts.length === 0) {
      throw new Error('No districts found for this state');
    }
    
    districtSelect.innerHTML = '<option value="">-- Select District --</option>';
    districts.forEach(d => {
      const opt = document.createElement('option');
      opt.value = d.district_id;
      opt.textContent = d.district_name;
      districtSelect.appendChild(opt);
    });
    districtSelect.disabled = false;
    validateForm();
  } catch (err) {
    districtSelect.innerHTML = '<option value="">-- Error loading districts --</option>';
    showError(`Failed to load districts: ${err.message}`);
  }
});

// ========== DISTRICT CHANGE: LOAD MANDALS & RESET CHILDREN ==========
districtSelect.addEventListener('change', async () => {
  const districtId = districtSelect.value;
  
  // Clear any previous errors immediately
  clearError();
  
  // Reset all child fields
  resetMandal();
  resetVillage();
  
  if (!districtId) {
    validateForm();
    return;
  }
  
  // Show loading state
  mandalSelect.innerHTML = '<option value="">-- Loading mandals... --</option>';
  mandalSelect.disabled = true;
  
  try {
    const res = await fetch(`${API_BASE}/list/mandal?district_id=${districtId}`);
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Server returned ${res.status}`);
    }
    const mandals = await res.json();
    
    if (!mandals || mandals.length === 0) {
      throw new Error('No mandals found for this district');
    }
    
    mandalSelect.innerHTML = '<option value="">-- Select Mandal --</option>';
    mandals.forEach(m => {
      const opt = document.createElement('option');
      opt.value = m.mandal_id;
      opt.textContent = m.mandal_name;
      mandalSelect.appendChild(opt);
    });
    mandalSelect.disabled = false;
    validateForm();
  } catch (err) {
    mandalSelect.innerHTML = '<option value="">-- Error loading mandals --</option>';
    showError(`Failed to load mandals: ${err.message}`);
  }
});

// ========== MANDAL CHANGE: ENABLE VILLAGE INPUT ==========
mandalSelect.addEventListener('change', () => {
  const mandalId = mandalSelect.value;
  
  // Clear any previous errors immediately
  clearError();
  
  // Reset village field
  resetVillage();
  
  if (mandalId) {
    villageInput.disabled = false;
    villageInput.focus();
  }
  
  validateForm();
});

// ========== RESET HELPER FUNCTIONS ==========
function resetDistrict() {
  districtSelect.value = '';
  districtSelect.innerHTML = '<option value="">-- Select State First --</option>';
  districtSelect.disabled = true;
  districtSelect.classList.remove('valid');
}

function resetMandal() {
  mandalSelect.value = '';
  mandalSelect.innerHTML = '<option value="">-- Select District First --</option>';
  mandalSelect.disabled = true;
  mandalSelect.classList.remove('valid');
}

function resetVillage() {
  villageInput.value = '';
  villageInput.disabled = true;
  villageInput.classList.remove('valid');
}

// ========== FORM SUBMISSION ==========
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  // Clear any previous errors
  clearError();
  
  if (!validateForm()) {
    showError('Please fill all mandatory fields');
    return;
  }
  
  const formData = new FormData(form);
  const payload = {
    name: formData.get('name').trim(),
    phone: formData.get('phone').trim(),
    email: formData.get('email')?.trim() || null,
    state_id: parseInt(formData.get('state')),
    district_id: parseInt(formData.get('district')),
    mandal_id: parseInt(formData.get('mandal')),
    village_name: formData.get('village').trim(),
    ...utm,
  };
  
  submitBtn.disabled = true;
  submitBtn.textContent = 'Submitting...';
  
  try {
    if (!navigator.onLine) {
      await queueRegistration(payload);
      showSuccess('✅ Offline: Queued for sync when online');
      resetFormAfterSubmit();
      return;
    }
    
    const res = await fetch(`${API_BASE}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Registration failed');
    }
    
    const result = await res.json();
    showSuccess(`✅ Registration successful!\nID: ${result.registration_id}`);
    resetFormAfterSubmit();
    
  } catch (err) {
    showError(`Registration failed: ${err.message}`);
  } finally {
    submitBtn.textContent = 'Register';
    validateForm();
  }
});

// ========== RESET FORM AFTER SUBMIT ==========
function resetFormAfterSubmit() {
  form.reset();
  resetDistrict();
  resetMandal();
  resetVillage();
  document.querySelectorAll('.valid').forEach(el => el.classList.remove('valid'));
  window.scrollTo({ top: 0, behavior: 'smooth' });
  clearError();
  validateForm();
}

// ========== HELPER FUNCTIONS ==========
function showSuccess(msg) {
  clearError();
  successEl.textContent = msg;
  successEl.style.display = 'block';
  setTimeout(() => { successEl.style.display = 'none'; }, 7000);
}

// ========== INITIALIZE ==========
loadStates();
validateForm();

// Register service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js');
}
