import { queueRegistration, savePref, getPref } from './db.js';

// API Base URL - Checks for localhost, 127.0.0.1, OR 192.168.x.x
const API_BASE = (
  window.location.hostname === 'localhost' ||
  window.location.hostname === '127.0.0.1'
)
  ? 'https://aap-campaign-reg-backend-444299072309.asia-south1.run.app' //'http://127.0.0.1:8000' // Local dev backend
  : 'https://aap-campaign-reg-backend-444299072309.asia-south1.run.app'; // Production backend

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
  
  // Email validation: optional but if entered must be valid
  const emailValue = emailInput.value.trim();
  const isEmailValid = emailValue === '' || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue);
  
  const isStateValid = stateSelect.value !== '';
  const isDistrictValid = districtSelect.value !== '';
  const isMandalValid = mandalSelect.value !== '';
  const isVillageValid = villageInput.value.trim().length >= 2;
  const isConsentChecked = consentAccuracyCheckbox.checked && consentShareCheckbox.checked;

  // Add visual feedback for VALID fields (green checkmark)
  nameInput.classList.toggle('valid', isNameValid);
  phoneInput.classList.toggle('valid', isPhoneValid);
  emailInput.classList.toggle('valid', isEmailValid && emailValue !== '');
  stateSelect.classList.toggle('valid', isStateValid);
  districtSelect.classList.toggle('valid', isDistrictValid);
  mandalSelect.classList.toggle('valid', isMandalValid);
  villageInput.classList.toggle('valid', isVillageValid);

  // Add visual feedback for INVALID fields (red border) - only if user has touched the field
  nameInput.classList.toggle('invalid', nameInput.value.trim().length > 0 && !isNameValid);
  phoneInput.classList.toggle('invalid', phoneInput.value.length > 0 && !isPhoneValid);
  emailInput.classList.toggle('invalid', emailValue.length > 0 && !isEmailValid);
  villageInput.classList.toggle('invalid', villageInput.value.trim().length > 0 && !isVillageValid);

  // Enable submit only if ALL mandatory fields valid + consent checked + email valid (if entered)
  const allValid = isNameValid && isPhoneValid && isEmailValid && isStateValid &&
    isDistrictValid && isMandalValid && isVillageValid &&
    isConsentChecked;
  
  submitBtn.disabled = !allValid;
  return allValid;
}

// Add validation listeners to all mandatory fields
nameInput.addEventListener('input', validateForm);
nameInput.addEventListener('blur', validateForm); // Check on focus out

phoneInput.addEventListener('input', validateForm);
phoneInput.addEventListener('blur', validateForm); // Check on focus out

emailInput.addEventListener('input', validateForm);
emailInput.addEventListener('blur', validateForm); // Check on focus out

stateSelect.addEventListener('change', validateForm);
districtSelect.addEventListener('change', validateForm);
mandalSelect.addEventListener('change', validateForm);

villageInput.addEventListener('input', validateForm);
villageInput.addEventListener('blur', validateForm); // Check on focus out

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
    
    // Auto-select Andhra Pradesh and trigger district load; State field is hidden on UI
    // Remove this auto-selection for mult-state implementation and display state on UI
    const apState = states.find(s => s.state_name === 'Andhra Pradesh');
    if (apState) {
      stateSelect.value = apState.state_id;
      stateSelect.dispatchEvent(new Event('change')); // Load districts
    }
    
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
  villageInput.classList.remove('invalid');
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
  
  // Safe extraction with null checks for ALL fields
  const nameValue = formData.get('name');
  const phoneValue = formData.get('phone');
  const emailValue = formData.get('email');
  const villageValue = formData.get('village');
  const stateValue = formData.get('state');
  const districtValue = formData.get('district');
  const mandalValue = formData.get('mandal');
  
  const payload = {
  name: nameInput.value.trim(),
  phone: phoneInput.value.trim(),
  email: emailInput.value.trim() || null,
  state_id: parseInt(stateSelect.value, 10),
  district_id: parseInt(districtSelect.value, 10),
  mandal_id: parseInt(mandalSelect.value, 10),
  village_name: villageInput.value.trim(),
  utm_source: utm.utm_source,
  utm_medium: utm.utm_medium,
  utm_campaign: utm.utm_campaign,
};

// Debug log
console.log('Payload:', payload);

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
      console.error('Backend validation error:', err);

      // Handle FastAPI validation errors (422)
      if (err.detail && Array.isArray(err.detail)) {
        const errorMessages = err.detail.map(e => {
          const field = e.loc ? e.loc.join(' → ') : 'Unknown field';
          return `${field}: ${e.msg}`;
        }).join('\n');
        throw new Error(errorMessages);
      }

      throw new Error(err.detail || JSON.stringify(err) || 'Registration failed');
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
  document.querySelectorAll('.invalid').forEach(el => el.classList.remove('invalid'));
  //window.scrollTo({ top: 0, behavior: 'smooth' });
  clearError();
  validateForm();
  loadStates()    // This hard codes state to AP
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
  navigator.serviceWorker.register('/sw.js')
    .then(() => console.log('Service Worker registered'))
    .catch(err => console.error('SW registration failed:', err));
}
