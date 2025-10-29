# Campaign Registration PWA

> Mobile-first Progressive Web App for rapid citizen onboarding at campaign events with offline support and auto-fill capabilities.

## Overview

A high-performance, offline-capable PWA designed for campaign volunteers to quickly register citizens at events via QR code or direct URL. Features intelligent auto-detection of governance units via geolocation, seamless offline queuing, and automatic sync when connectivity returns.

### Key Features

- 🚀 **Instant Loading**: SSG shell with sub-second first paint
- 📱 **Mobile-First**: Optimized for one-handed operation on smartphones
- 🔌 **Offline-Capable**: Service Worker + IndexedDB queue with Background Sync
- 📍 **Smart Auto-Fill**: Geolocation-based governance field detection
- ♿ **Accessible**: WCAG-compliant with keyboard navigation and screen reader support
- 🎨 **Modern UI**: Gradient design with smooth animations and touch-based validation
- 🔒 **Privacy-First**: No raw coordinate storage; consent-gated submissions

---

## Tech Stack

### Frontend
- **HTML5** + **CSS3** (modern gradient UI with Inter font)
- **Vanilla JavaScript** (ES modules, no framework overhead)
- **Service Worker** (offline caching and Background Sync)
- **IndexedDB** (local queue and preferences)

### Backend
- **FastAPI** (Python 3.11+)
- **Pydantic** (validation and serialization)
- **Uvicorn** (ASGI server)

### Infrastructure (Current: Local Dev)
- **Static Server**: Python `http.server` on port 8080
- **API Server**: Uvicorn on port 8000
- **Storage**: In-memory (PostgreSQL planned for Phase 2)

---

## Project Structure

```
aap_campaign_reg/
├── frontend/
│   ├── index.html           # SSG shell with embedded styles
│   ├── main.js              # Client islands (dropdowns, geolocation, validation)
│   ├── db.js                # IndexedDB helpers (queue, prefs)
│   ├── sw.js                # Service Worker (cache + Background Sync)
│   └── manifest.webmanifest # PWA manifest
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app, routes, and stub data
│   │   ├── schemas.py       # Pydantic models for validation
│   │   ├── models.py        # (placeholder for SQLAlchemy models)
│   │   └── db.py            # (placeholder for DB session)
│   ├── pyproject.toml       # Poetry dependencies
│   └── poetry.lock
├── .gitignore
└── README.md
```

---

## Data Model

### Captured Fields

#### Identity
- **Name** (required): 2–120 chars; letters, spaces, hyphens, apostrophes, local scripts
- **Phone** (required): 10 digits (India); normalized to E.164 (+91...) server-side
- **Email** (optional): strongly recommended; validated if present

#### Governance (all required)
- **Parliamentary Constituency (PC)**: auto-detected or manual selection
- **Assembly Constituency (AC)**: cascades from PC
- **Ward / Gram Panchayat (Ward/GP)**: cascades from AC; typeahead search

#### Metadata
- **UTM Parameters**: utm_source, utm_medium, utm_campaign (from QR code or URL)
- **Timestamp**: createdAt (client-generated)

#### Consent
- **UI-Only**: Mandatory checkbox gates submission; **not stored server-side**

### Schema (POST /api/register)

```json
{
  "id": "uuid-v4",
  "name": "string",
  "phone": "string (10 digits)",
  "email": "string | null",
  "pc_id": "string",
  "ac_id": "string",
  "ward_gp_id": "string",
  "utm_source": "string | null",
  "utm_medium": "string | null",
  "utm_campaign": "string | null",
  "createdAt": 1730000000000
}
```

---

## User Flows

### Flow 1: Auto-Detect (Happy Path)

1. User scans QR code → PWA opens instantly
2. User taps **"Quick Register with Auto-Fill"**
3. Browser requests location permission
4. **If granted**: 
   - Frontend calls `/lookup?lat=...&lng=...`
   - Backend resolves Ward/GP → AC → PC
   - All three dropdowns pre-select; user reviews and optionally edits
   - User checks consent and submits
5. **If online**: POST to `/api/register` → 201 Created
6. **If offline**: Queued in IndexedDB → syncs when online

### Flow 2: Manual Cascade (Location Denied)

1. User taps **"Quick Register with Auto-Fill"**
2. Browser denies location or times out
3. **Auto-fallback**: PC list loads automatically; focus moves to PC input
4. User selects **PC** → AC list populates filtered by PC
5. User selects **AC** → Ward/GP list populates filtered by AC; typeahead search available
6. User types to filter large Ward/GP lists (debounced 250ms)
7. User checks consent and submits
8. Online/offline handling same as Flow 1

### Flow 3: Offline Queue & Sync

1. User fills form while offline
2. Submission queued in IndexedDB with `synced: false`
3. **When online**:
   - Service Worker Background Sync event fires
   - Queued items POST to `/api/register` in batches
   - Successfully synced items marked `synced: true`
4. User sees success message with sync status

---

## API Reference

### Public Endpoints (Edge-Cacheable)

#### `GET /list/pc`
Returns all Parliamentary Constituencies.

**Response**:
```json
[
  { "id": "pc-1", "code": "PC01", "name": "Sample PC One" },
  { "id": "pc-2", "code": "PC02", "name": "Sample PC Two" }
]
```

**Cache**: Long max-age + ETag

---

#### `GET /list/ac?pc_id=<id>`
Returns Assembly Constituencies filtered by parent PC.

**Response**:
```json
[
  { "id": "ac-1", "code": "AC01", "name": "Sample AC A", "pc_id": "pc-1" }
]
```

**Cache**: Long max-age + ETag

---

#### `GET /list/ward_gp?ac_id=<id>&page=1&page_size=20&q=<search>`
Returns Ward/GPs (paged, searchable) filtered by parent AC.

**Response**:
```json
{
  "items": [
    { "id": "w-1", "code": "W001", "name": "Ward Alpha", "ac_id": "ac-1" }
  ],
  "page": 1,
  "page_size": 20,
  "total": 50
}
```

**Cache**: Long max-age + ETag

---

#### `GET /lookup?lat=<float>&lng=<float>`
Reverse geocode coordinates to governance units.

**Response**:
```json
{
  "ward_gp_id": "w-1",
  "ward_gp_name": "Ward Alpha",
  "ac_id": "ac-1",
  "ac_name": "Sample AC A",
  "pc_id": "pc-1",
  "pc_name": "Sample PC One",
  "source": "stub"
}
```

**Cache**: Short TTL (60s)

**Note**: Current implementation returns stub data; Phase 2 will integrate real reverse geocoding (Google Maps API or Mappls).

---

### Registration Endpoint

#### `POST /api/register`
Create or update a registration (dedupe by phone).

**Request**: See schema above

**Response** (201 Created):
```json
{
  "id": "uuid-v4",
  "status": "created" | "updated"
}
```

**Validation**:
- Phone normalized to E.164
- PC/AC/Ward-GP IDs validated against master lists
- Dedupe by normalized phone (upsert behavior)

**Errors**:
- `422 Unprocessable Entity`: Invalid phone format or unknown governance IDs

---

## Local Development

### Prerequisites

- **Python 3.11+** (backend)
- **Poetry** (dependency management)
- **Modern browser** (Chrome/Edge/Safari with Service Worker support)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/stirandas/aap_campaign_reg.git
   cd aap_campaign_reg
   ```

2. **Install backend dependencies**:
   ```bash
   cd backend
   poetry install
   ```

3. **Start the API server** (in `backend/`):
   ```bash
   poetry run uvicorn app.main:app --reload --port 8000
   ```
   Backend runs at http://127.0.0.1:8000  
   API docs at http://127.0.0.1:8000/docs

4. **Start the static server** (from repo root):
   ```bash
   python -m http.server 8080 --bind 127.0.0.1
   ```
   Frontend serves at http://127.0.0.1:8080

5. **Open the PWA**:
   - Navigate to http://localhost:8080/frontend/index.html
   - Service Worker will register automatically

### Testing Offline Mode

1. Open Chrome DevTools → **Application** tab
2. Check **Offline** or use Network throttle
3. Fill and submit the form → should queue in IndexedDB
4. Uncheck **Offline** → Background Sync flushes queue to API

### Debugging

- **Service Worker**: DevTools → Application → Service Workers
- **IndexedDB**: DevTools → Application → Storage → IndexedDB → `app_campaign_reg`
- **Cache**: DevTools → Application → Cache Storage → `acr-shell-v2`
- **API Logs**: Check terminal running uvicorn for request logs

---

## Validation Rules

### Form Validation

- **Name**: Required; 2–120 chars; allow local scripts
- **Phone**: Required; must be 10 digits; real-time masking; normalized to E.164 on submit
- **Email**: Optional; format validation only if present
- **PC/AC/Ward-GP**: Required; must select from lists
- **Consent**: Required; checkbox must be checked to enable Submit

### Visual Feedback

- **Neutral borders** on page load (no pre-validation warnings)
- **Blue glow** on focus (inviting interaction)
- **Red border** after blur if invalid (touch-based validation)
- **Green border** after blur if valid (positive reinforcement)
- **Inline error messages** on submit if required fields empty

---

## UI/UX Highlights

### Design System

- **Colors**: 
  - Primary: #0b5fff (AAP blue)
  - Success: #10b981 (green)
  - Error: #f43f5e (red)
  - Neutral: #e2e8f0 (light gray)
- **Typography**: Inter (Google Fonts) with system fallbacks
- **Spacing**: 4px grid system
- **Animations**: Fade-in on load, slide-in for messages, scale on hover

### Accessibility

- **WCAG 2.1 AA**: Keyboard navigation, focus indicators, ARIA labels
- **Touch Targets**: Minimum 44px height for all interactive elements
- **Screen Readers**: Inline error announcements, descriptive labels
- **High Contrast**: Meets 4.5:1 contrast ratio for text

---

## Offline Architecture

### Service Worker Strategy

```
Cache Strategy:
- Shell (HTML/JS/CSS): Cache-first with network fallback
- API Requests: Network-first; queue on failure
- Background Sync: Flush queue when connectivity restored
```

### IndexedDB Stores

1. **registrations**: Queued submissions with sync status
   - Indexes: `by_synced`, `by_createdAt`
2. **prefs**: Last-selected PC/AC for faster repeat usage

---

## Performance

### Metrics (Target)

- **First Contentful Paint**: < 1s
- **Time to Interactive**: < 2s
- **Lighthouse Score**: 95+ (Performance, Accessibility, Best Practices, PWA)

### Optimizations

- SSG shell served from CDN (future)
- Code-split client islands (future)
- HTTP/2 with compression
- Long cache headers for static assets
- Edge-cached list APIs

---

## Security & Privacy

### Data Handling

- **No raw coordinates stored**: Geolocation used only for lookup, not persisted
- **Consent not stored**: Checkbox gates UI; no server-side consent audit trail
- **Phone normalization**: E.164 format prevents duplicate entries
- **CORS**: Restricted to known origins (localhost:8080, 127.0.0.1:8080 in dev)

### Transport Security

- **HTTPS/TLS**: Required for production (enforced by Service Worker)
- **Input Validation**: Server-side validation via Pydantic
- **Rate Limiting**: Planned for production deployment

---

## Roadmap

### Phase 1: MVP (Current) ✅
- [x] Frontend PWA with offline support
- [x] Backend API with stub data
- [x] Auto-detect + manual cascade flows
- [x] Consent gating (UI-only)
- [x] Touch-based validation
- [x] Modern gradient UI

### Phase 2: Production-Ready (Next)
- [ ] PostgreSQL persistence with SQLAlchemy + Alembic
- [ ] Real governance data (PC/AC/Ward-GP from official sources)
- [ ] Reverse geocoding integration (Google Maps or Mappls API)
- [ ] Stats and export endpoints (GET /api/stats, GET /api/export)
- [ ] QR code generator with UTM parameters
- [ ] Role-based admin dashboard

### Phase 3: Scale & Deploy
- [ ] Cloud Run deployment (backend)
- [ ] CDN deployment (frontend)
- [ ] Cloud SQL (PostgreSQL)
- [ ] Edge caching for list APIs
- [ ] Analytics integration
- [ ] A/B testing for conversion optimization

---

## Contributing

This is a private campaign project. For internal contributors:

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Commit with semantic messages: `feat:`, `fix:`, `docs:`, `chore:`
3. Test offline flows before pushing
4. Submit PR for review

---

## License

Proprietary. All rights reserved.

---

## Support

For questions or issues, contact the development team internally.

---

## Changelog

### v1.0 (October 29, 2025)
- Initial MVP release
- Offline-capable PWA with Service Worker + IndexedDB
- FastAPI backend with stub governance data
- Auto-detect via geolocation + manual cascade fallback
- Modern gradient UI with touch-based validation
- Consent gating (UI-only, no server storage)

---

**Built with ❤️ for rapid campaign onboarding**