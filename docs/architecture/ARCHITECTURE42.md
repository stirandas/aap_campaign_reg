# Architecture Documentation
**Campaign Registration PWA**

## Table of Contents

1. [C4 Model Diagrams](#c4-model-diagrams)
   - Level 1: System Context
   - Level 2: Container
   - Level 3: Component
   - Level 4: Code (Key Flows)
2. [arc42 Documentation](#arc42-documentation)

---

# C4 Model Diagrams

## Level 1: System Context Diagram

**Scope**: The entire Campaign Registration system and its external dependencies

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Campaign Event                              │
│                                                                     │
│  ┌──────────────┐                                                  │
│  │  Campaign    │  Scans QR Code                                   │
│  │  Volunteer   │  ──────────────────┐                             │
│  │              │                    │                             │
│  └──────────────┘                    ▼                             │
│                          ┌────────────────────────┐                │
│  ┌──────────────┐        │  Campaign Registration│                │
│  │   Citizen    │ Uses   │        PWA             │                │
│  │ (Registrant) │───────▶│                        │                │
│  └──────────────┘        │  [Mobile Web App]      │                │
│                          └────────────┬───────────┘                │
│                                       │                             │
└───────────────────────────────────────┼─────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
        ┌──────────────────┐  ┌────────────────┐  ┌──────────────────┐
        │  Geolocation API │  │  Registration  │  │  Governance Data │
        │   (Browser)      │  │   Backend API  │  │   Service        │
        │                  │  │  [FastAPI]     │  │  [Future: GIS]   │
        └──────────────────┘  └────────────────┘  └──────────────────┘
```

### Actors

**Campaign Volunteer**: Event staff who direct citizens to scan QR codes or access the registration URL

**Citizen (Registrant)**: Individual registering for campaign updates via mobile device

### External Systems

**Browser Geolocation API**: Native device API for obtaining GPS coordinates

**Registration Backend API**: FastAPI service handling list/lookup queries and registration persistence

**Governance Data Service**: Future GIS/mapping service for reverse geocoding (Google Maps, Mappls, or custom polygon service)

---

## Level 2: Container Diagram

**Scope**: Major runtime containers and their interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                               User's Mobile Device                          │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────┐       │
│  │                         Mobile Browser                          │       │
│  │                                                                 │       │
│  │  ┌──────────────────────────────────────────────────────┐      │       │
│  │  │            PWA Frontend Container                    │      │       │
│  │  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │      │       │
│  │  │  │ HTML/CSS   │  │ JavaScript │  │   Service    │  │      │       │
│  │  │  │  Shell     │  │  Islands   │  │   Worker     │  │      │       │
│  │  │  └────────────┘  └────────────┘  └──────────────┘  │      │       │
│  │  │                                                      │      │       │
│  │  │  ┌─────────────────────────────────────────────┐   │      │       │
│  │  │  │          IndexedDB                          │   │      │       │
│  │  │  │  - registrations (queue)                    │   │      │       │
│  │  │  │  - prefs (last selections)                  │   │      │       │
│  │  │  └─────────────────────────────────────────────┘   │      │       │
│  │  └──────────────────────────────────────────────────────┘      │       │
│  │                          │                                      │       │
│  └──────────────────────────┼──────────────────────────────────────┘       │
│                             │                                              │
└─────────────────────────────┼──────────────────────────────────────────────┘
                              │ HTTPS/JSON
                              ▼
              ┌───────────────────────────────────────┐
              │    Backend Container (FastAPI)        │
              │                                       │
              │  ┌─────────────────────────────────┐ │
              │  │   API Endpoints                 │ │
              │  │   - /list/pc, /list/ac,        │ │
              │  │     /list/ward_gp              │ │
              │  │   - /lookup?lat=...&lng=...    │ │
              │  │   - /api/register              │ │
              │  └─────────────────────────────────┘ │
              │                                       │
              │  ┌─────────────────────────────────┐ │
              │  │   In-Memory Store (MVP)         │ │
              │  │   - PCs, ACs, Ward/GPs (stubs) │ │
              │  │   - Registrations (temp)        │ │
              │  └─────────────────────────────────┘ │
              │                                       │
              └───────────────────────────────────────┘
                              │
                              │ (Phase 2)
                              ▼
              ┌───────────────────────────────────────┐
              │   PostgreSQL Database (Planned)       │
              │   - pc, ac, ward_gp tables            │
              │   - registrations (with dedupe)       │
              └───────────────────────────────────────┘
```

### Container Details

#### PWA Frontend Container
- **Technology**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Responsibilities**: UI rendering, user input, geolocation, offline queue, background sync
- **Storage**: IndexedDB (registrations queue + user preferences)
- **Communication**: RESTful JSON over HTTPS to Backend API

#### Backend Container
- **Technology**: FastAPI (Python 3.11+), Uvicorn ASGI server
- **Responsibilities**: List serving, reverse geocoding (stub), registration validation and dedupe
- **Storage**: In-memory dicts (MVP); PostgreSQL (Phase 2)
- **Communication**: REST API endpoints; CORS-enabled for localhost

#### Database (Phase 2)
- **Technology**: PostgreSQL 15+
- **Responsibilities**: Persistent storage with ACID guarantees, unique constraint on phone

---

## Level 3: Component Diagram

**Scope**: Components within the PWA Frontend Container

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PWA Frontend Container                             │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                         index.html (SSG Shell)                     │    │
│  │  - Static HTML structure                                           │    │
│  │  - Embedded CSS (gradient theme, animations)                       │    │
│  │  - Imports main.js as ES module                                    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                      │                                      │
│                                      │ imports                              │
│                                      ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                           main.js (Orchestrator)                    │    │
│  │                                                                     │    │
│  │  ┌─────────────────┐   ┌──────────────────┐   ┌─────────────────┐ │    │
│  │  │  Form Manager   │   │  Geolocation     │   │  Validation     │ │    │
│  │  │  - Submit flow  │   │  Island          │   │  Manager        │ │    │
│  │  │  - Consent gate │   │  - Permission    │   │  - Touch-based  │ │    │
│  │  │  - Phone norm.  │   │  - Lookup call   │   │  - Inline errors│ │    │
│  │  └─────────────────┘   └──────────────────┘   └─────────────────┘ │    │
│  │                                                                     │    │
│  │  ┌─────────────────────────────────────────────────────────────┐  │    │
│  │  │               Dropdowns Island                              │  │    │
│  │  │  - PC list loader                                           │  │    │
│  │  │  - AC cascade (filter by PC)                                │  │    │
│  │  │  - Ward/GP cascade (filter by AC, typeahead, pagination)    │  │    │
│  │  │  - Auto-correction logic (toast on mismatch)                │  │    │
│  │  └─────────────────────────────────────────────────────────────┘  │    │
│  │                                                                     │    │
│  │  ┌─────────────────────────────────────────────────────────────┐  │    │
│  │  │               API Client                                    │  │    │
│  │  │  - fetchJSON() helper                                        │  │    │
│  │  │  - tryOnlinePost()                                           │  │    │
│  │  └─────────────────────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                      │                                      │
│                                      │ imports                              │
│                                      ▼                                      │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                           db.js (IndexedDB Helper)                  │    │
│  │  - openDB()                                                         │    │
│  │  - queueRegistration()                                              │    │
│  │  - listUnsynced(), markSynced()                                     │    │
│  │  - savePref(), getPref()                                            │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                           sw.js (Service Worker)                    │    │
│  │  - install: cache SSG shell                                         │    │
│  │  - activate: cleanup old caches                                     │    │
│  │  - fetch: cache-first for static, network-first for API            │    │
│  │  - sync: flush registration queue on 'sync-registrations' event     │    │
│  │  - message: manual flush trigger                                    │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

#### Form Manager (main.js)
- Orchestrates form submission flow
- Gates submit button on consent checkbox
- Normalizes phone to E.164 before queuing
- Shows success/error messages

#### Geolocation Island (main.js)
- Requests browser location permission
- Calls /lookup API with coordinates
- Pre-fills PC/AC/Ward-GP on success
- Falls back to manual cascade on denial/failure

#### Dropdowns Island (main.js)
- Loads PC list on page load (or on fallback)
- Cascades AC list filtered by selected PC
- Cascades Ward/GP list filtered by selected AC with typeahead and pagination
- Auto-corrects AC/PC if Ward/GP implies different parents

#### Validation Manager (main.js)
- Adds "touched" class on blur
- Shows red/green borders based on validity
- Blocks submit if required fields empty or invalid

#### API Client (main.js)
- Central fetch wrapper with error handling
- tryOnlinePost() attempts immediate submission
- Falls back to queue if network fails

#### IndexedDB Helper (db.js)
- Manages two object stores: registrations, prefs
- CRUD operations for queue management
- Tracks sync status on each registration

#### Service Worker (sw.js)
- Intercepts fetch requests
- Caches static shell (install)
- Cleans old caches (activate)
- Flushes queue on Background Sync event or manual message

---

## Level 4: Code Diagram (Key Flow: Offline Submit → Sync)

**Scope**: Sequence diagram for offline submission and background sync

```
User          Browser        main.js        db.js        IndexedDB    sw.js      Backend API
 │               │              │             │              │           │            │
 │  Fill form    │              │             │              │           │            │
 │──────────────▶│              │             │              │           │            │
 │               │              │             │              │           │            │
 │  Check consent│              │             │              │           │            │
 │  & Submit     │              │             │              │           │            │
 │──────────────▶│──────────────▶             │              │           │            │
 │               │    validate & build payload│              │           │            │
 │               │              │──────────────▶              │           │            │
 │               │              │  queueRegistration(payload) │           │            │
 │               │              │             │──────────────▶│           │            │
 │               │              │             │   put(item)   │           │            │
 │               │              │             │◀──────────────│           │            │
 │               │              │◀──────────────              │           │            │
 │               │              │                             │           │            │
 │               │              │──────────────▶              │           │            │
 │               │              │ tryOnlinePost()             │           │            │
 │               │              │ (fetch fails, offline)      │           │            │
 │               │              │◀──────────────              │           │            │
 │               │              │   returns false             │           │            │
 │               │              │                             │           │            │
 │               │              │  register Background Sync   │           │            │
 │               │              │─────────────────────────────────────────▶            │
 │               │              │                             │           │            │
 │◀──────────────│◀──────────────                            │           │            │
 │  "Saved locally. Will sync when online."                  │           │            │
 │               │              │                             │           │            │
 │  [Time passes, network restored]                          │           │            │
 │               │              │                             │           │            │
 │               │              │            sync event fires │           │            │
 │               │              │             │               │◀──────────│            │
 │               │              │             │               │ 'sync-registrations' │
 │               │              │             │               │           │            │
 │               │              │             │               │───────────▶            │
 │               │              │             │               │  flushQueue()          │
 │               │              │             │               │   (in sw.js)           │
 │               │              │             │               │           │            │
 │               │              │             │               │  import db.js          │
 │               │              │             │               │  listUnsynced()        │
 │               │              │             │               │◀──────────│            │
 │               │              │             │◀──────────────│           │            │
 │               │              │             │   [item]      │           │            │
 │               │              │             │               │           │            │
 │               │              │             │               │           │──────────▶ │
 │               │              │             │               │           │ POST /api/ │
 │               │              │             │               │           │  register  │
 │               │              │             │               │           │◀────────── │
 │               │              │             │               │           │  201 OK    │
 │               │              │             │               │           │            │
 │               │              │             │◀──────────────│───────────│            │
 │               │              │             │  markSynced([id])         │            │
 │               │              │             │──────────────▶│           │            │
 │               │              │             │  update item  │           │            │
 │               │              │             │  synced: true │           │            │
```

---

# arc42 Documentation

## 1. Introduction and Goals

### Requirements Overview

**Primary Goal**: Enable rapid, offline-capable citizen registration at campaign events with minimal friction.

**Key Requirements**:
1. **One-screen registration flow** with auto-population of identity and governance fields
2. **Offline-first**: Queue submissions locally; sync when connectivity restored
3. **Sub-2-second first paint** on median mobile devices
4. **Accessible**: WCAG 2.1 AA compliant
5. **Privacy-first**: No raw coordinate storage; consent gating

### Quality Goals

| Priority | Quality Attribute | Scenario |
|----------|-------------------|----------|
| 1 | **Availability** | User can register even with zero connectivity; data syncs automatically when online |
| 2 | **Performance** | First Contentful Paint < 1s; Time to Interactive < 2s |
| 3 | **Usability** | One-screen flow; <5 taps from QR scan to submit; auto-fill reduces manual entry by 60%+ |
| 4 | **Accessibility** | Keyboard navigable; screen-reader friendly; 4.5:1 contrast ratio |
| 5 | **Maintainability** | Vanilla JS (no framework lock-in); clear separation of concerns; documented APIs |

### Stakeholders

| Role | Concerns |
|------|----------|
| Campaign Manager | Registration conversion rate; data quality; offline reliability |
| Volunteer | Ease of use; speed; works on low-end devices and poor networks |
| Citizen (Registrant) | Privacy; quick registration; mobile-friendly |
| Developer | Code maintainability; clear architecture; testability |
| IT Ops | Deployment simplicity; monitoring; scalability for large events |

---

## 2. Constraints

### Technical Constraints

| Constraint | Description |
|------------|-------------|
| **No framework dependencies** | Must use vanilla JavaScript to minimize bundle size and ensure fast first paint |
| **Browser compatibility** | Must support Chrome, Edge, Safari (iOS 14+), Firefox (last 2 versions) |
| **Offline-first** | Service Worker and IndexedDB required; no server-side session state |
| **Mobile-first** | Design and performance optimized for smartphones (320px+ width) |

### Organizational Constraints

| Constraint | Description |
|------------|-------------|
| **Timeline** | MVP delivered within 1 week |
| **Team** | Single full-stack developer |
| **Budget** | Minimal hosting cost (static CDN + serverless backend) |

### Regulatory Constraints

| Constraint | Description |
|------------|-------------|
| **Data Privacy** | No storage of raw GPS coordinates; consent checkbox required |
| **Accessibility** | WCAG 2.1 AA compliance for public-facing political campaign tool |

---

## 3. Context and Scope

### Business Context

**Campaign Registration System** enables campaign volunteers to rapidly onboard citizens at events (rallies, door-to-door canvassing, community centers) via QR code or direct URL. The system captures identity and governance data for downstream outreach (SMS, email, phone banking).

**Key Business Flows**:
1. Volunteer shares QR code → Citizen scans → PWA opens → Citizen submits
2. Citizen submission queued offline → Syncs when network available
3. Campaign team exports registrations for outreach segmented by PC/AC/Ward-GP

### Technical Context

```
┌──────────────┐      QR Code/URL     ┌────────────────────┐
│   Citizen    │─────────────────────▶│   PWA (Browser)    │
│   (Mobile)   │                      │                    │
└──────────────┘                      └──────────┬─────────┘
                                                 │
                                    HTTPS/JSON   │
                                                 │
                                                 ▼
                                      ┌────────────────────┐
                                      │  FastAPI Backend   │
                                      │  (Registration API)│
                                      └──────────┬─────────┘
                                                 │
                                        Postgres │ (Phase 2)
                                                 ▼
                                      ┌────────────────────┐
                                      │  Database          │
                                      │  (Registrations)   │
                                      └────────────────────┘
```

---

## 4. Solution Strategy

### Technology Decisions

| Decision | Rationale |
|----------|-----------|
| **Vanilla JavaScript** | Zero framework overhead; faster first paint; no build step for MVP; easier to maintain |
| **Service Worker + IndexedDB** | Industry-standard offline pattern; broad browser support; automatic background sync |
| **FastAPI (Python)** | High-performance async; built-in validation (Pydantic); fast prototyping; easy deployment |
| **SSG + Islands** | Static HTML shell loads instantly; JavaScript hydrates interactive parts incrementally |

### Architectural Patterns

1. **Progressive Web App (PWA)**: Installable; offline-capable; mobile-first
2. **Islands Architecture**: Static shell with isolated interactive components (dropdowns, geolocation)
3. **Offline-First**: Service Worker intercepts network requests; IndexedDB queues submissions
4. **API Gateway**: Backend exposes RESTful JSON endpoints; CORS-enabled; edge-cacheable lists

### Quality Strategies

| Quality Goal | Strategy |
|--------------|----------|
| **Performance** | SSG shell from CDN; code-split islands; HTTP/2; edge-cached list APIs |
| **Availability** | Service Worker caches shell; IndexedDB queues offline submissions; Background Sync auto-retry |
| **Usability** | Touch-based validation (no red borders on load); auto-fallback on geo denial; consent gates submit |
| **Accessibility** | Semantic HTML; ARIA labels; keyboard navigation; 4.5:1 contrast; focus indicators |

---

## 5. Building Block View

### Level 1: System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                Campaign Registration System                 │
│                                                             │
│  ┌──────────────────┐          ┌──────────────────┐        │
│  │   PWA Frontend   │◀────────▶│  Backend API     │        │
│  │   (Browser)      │  JSON/   │  (FastAPI)       │        │
│  │                  │  HTTPS   │                  │        │
│  └──────────────────┘          └──────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Level 2: PWA Frontend Whitebox

| Component | Responsibility |
|-----------|----------------|
| **index.html** | SSG shell; static layout; embedded CSS |
| **main.js** | Orchestrator; form logic; geolocation; API calls; validation |
| **db.js** | IndexedDB abstraction; queue management; preferences |
| **sw.js** | Service Worker; cache management; Background Sync; offline handling |

### Level 3: Backend API Whitebox

| Component | Responsibility |
|-----------|----------------|
| **main.py** | FastAPI app; route definitions; CORS middleware |
| **schemas.py** | Pydantic models for request/response validation |
| **Stub Data** | In-memory PC/AC/Ward-GP lists; temporary registration store (Phase 1) |

---

## 6. Runtime View

### Scenario: Auto-Detect Flow (Online)

1. User scans QR code → PWA loads from cache (Service Worker)
2. User taps "Quick Register with Auto-Fill"
3. Browser requests geolocation permission → **granted**
4. main.js calls `GET /lookup?lat=...&lng=...`
5. Backend returns `{ ward_gp_id, ac_id, pc_id, ... }`
6. main.js pre-fills all three dropdowns
7. User reviews, checks consent, submits
8. main.js normalizes phone → POST `/api/register`
9. Backend validates, dedupes by phone, returns 201
10. Success message displayed; form resets

### Scenario: Offline Submission & Sync

1. User fills form while offline
2. User checks consent, submits
3. main.js detects network failure in `tryOnlinePost()`
4. db.js queues payload in IndexedDB (`synced: false`)
5. Success message: "Saved locally. Will sync when online."
6. **Network restored** → Service Worker fires `sync` event
7. sw.js imports db.js → `listUnsynced()` → POST each item
8. Backend returns 201 → sw.js calls `markSynced([id])`
9. IndexedDB updated: `synced: true`

---

## 7. Deployment View

### Current (MVP): Local Development

```
Developer Machine
├── Terminal 1: Python http.server (port 8080) → serves frontend/
├── Terminal 2: Uvicorn (port 8000) → runs backend/app/main.py
└── Browser: http://localhost:8080/frontend/index.html
```

### Phase 2: Production Deployment

```
┌────────────────┐
│    Citizen     │
│   (Mobile)     │
└───────┬────────┘
        │ HTTPS
        ▼
┌────────────────────────────────────────┐
│         CDN (Cloudflare/CloudFront)    │
│  - Serves static frontend (SSG shell)  │
│  - Cache-Control: immutable            │
└────────────────┬───────────────────────┘
                 │
        API calls│ (HTTPS/JSON)
                 ▼
┌────────────────────────────────────────┐
│     Cloud Run / Railway / Fly.io       │
│  - FastAPI backend container           │
│  - Auto-scaling                        │
│  - CORS: production origins only       │
└────────────────┬───────────────────────┘
                 │
        SQL conn │
                 ▼
┌────────────────────────────────────────┐
│     Cloud SQL (PostgreSQL)             │
│  - Managed DB with backups             │
│  - Connection pooling                  │
└────────────────────────────────────────┘
```

---

## 8. Cross-Cutting Concepts

### Offline-First Pattern

**Principle**: Application remains fully functional without network connectivity.

**Implementation**:
- Service Worker caches static shell (HTML/CSS/JS)
- IndexedDB stores unsynced submissions
- Background Sync API retries failed POSTs automatically
- Manual flush fallback for browsers without Background Sync

### Progressive Enhancement

**Principle**: Core functionality works without JavaScript; JavaScript enhances UX.

**Implementation**:
- Form is valid HTML5 with native validation attributes
- JavaScript adds: auto-detect, cascade, touch-based validation, offline queue
- Fallback: Users can still submit via network-only (no offline support)

### Accessibility

**Principle**: Usable by everyone, including people with disabilities.

**Implementation**:
- Semantic HTML5 (`<form>`, `<label>`, `<input>`)
- ARIA labels for dropdowns (`role="combobox"`, `aria-expanded`)
- Keyboard navigation (tab order, Enter to submit)
- Focus indicators (blue ring)
- High contrast text (4.5:1)
- Touch targets ≥44px

### Security

**Principle**: Defense in depth; assume browser and network are hostile.

**Implementation**:
- HTTPS enforced (Service Worker requirement)
- CORS restricted to known origins
- Input validation on both client (UX) and server (security)
- Phone normalization prevents duplicate entries
- No raw GPS coordinates stored
- Rate limiting (Phase 2)

---

## 9. Architecture Decisions (ADRs)

### ADR-001: Use Vanilla JavaScript Instead of React/Vue

**Status**: Accepted

**Context**: Need fast first paint and minimal bundle size for mobile-first PWA.

**Decision**: Use vanilla JavaScript with ES modules; no framework.

**Consequences**:
- ✅ Zero framework overhead (~40KB saved)
- ✅ Instant first paint (no hydration delay)
- ✅ Easier to maintain (no framework updates)
- ❌ More manual DOM manipulation
- ❌ No declarative UI (acceptable for single-screen form)

---

### ADR-002: Consent as UI-Only Gating (No Server Storage)

**Status**: Accepted

**Context**: Original spec required consent text version and timestamp storage for audit trails.

**Decision**: Consent checkbox gates frontend submission only; not sent to backend.

**Consequences**:
- ✅ Simpler data model and API
- ✅ Faster MVP iteration
- ❌ No audit trail for consent opt-in
- ⚠️ May need to add back for legal compliance (Phase 2)

---

### ADR-003: In-Memory Storage for MVP; PostgreSQL for Phase 2

**Status**: Accepted

**Context**: Need working backend quickly; production requires persistence.

**Decision**: Use in-memory dicts for MVP; migrate to PostgreSQL in Phase 2.

**Consequences**:
- ✅ Fast prototyping (no DB setup)
- ✅ Easy local testing
- ❌ Data lost on server restart
- ⏭️ Phase 2: Add SQLAlchemy + Alembic + Postgres

---

## 10. Quality Requirements

### Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| First Contentful Paint | < 1s | Lighthouse |
| Time to Interactive | < 2s | Lighthouse |
| Total Blocking Time | < 200ms | Lighthouse |
| Lighthouse Performance | ≥95 | Automated CI |

### Availability

| Metric | Target | Measurement |
|--------|--------|-------------|
| Offline functionality | 100% (queue + sync) | Manual test |
| Background Sync success | ≥98% | Analytics |
| Service Worker install rate | ≥95% | Analytics |

### Accessibility

| Metric | Target | Measurement |
|--------|--------|-------------|
| Lighthouse Accessibility | 100 | Automated CI |
| Keyboard navigation | All actions accessible | Manual test |
| Screen reader support | All fields announced | Manual test (NVDA/VoiceOver) |

---

## 11. Risks and Technical Debt

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Background Sync unsupported** | Low (95% browser support) | Medium | Manual flush fallback implemented |
| **Geolocation denied** | High (privacy-conscious users) | Low | Auto-fallback to manual cascade |
| **Stub reverse geocoding** | High (MVP only) | High | Phase 2: integrate real GIS API |
| **In-memory data loss** | High (server restart) | High | Phase 2: migrate to Postgres |

### Technical Debt

| Item | Priority | Plan |
|------|----------|------|
| **No real governance data** | High | Phase 2: seed from official sources |
| **No PostgreSQL** | High | Phase 2: add SQLAlchemy + Alembic |
| **No stats/export APIs** | Medium | Phase 2: implement /api/stats, /api/export |
| **No rate limiting** | Low | Phase 3: add Redis-based rate limiter |
| **No monitoring** | Medium | Phase 3: integrate Sentry + analytics |

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **PC** | Parliamentary Constituency; largest governance unit |
| **AC** | Assembly Constituency; mid-level governance unit |
| **Ward/GP** | Ward (urban) or Gram Panchayat (rural); smallest governance unit |
| **SSG** | Static Site Generation; pre-rendered HTML |
| **PWA** | Progressive Web App; installable, offline-capable web application |
| **Service Worker** | Browser background script for offline caching and Background Sync |
| **IndexedDB** | Browser-based NoSQL database for client-side storage |
| **Background Sync** | API for deferring actions until network connectivity is restored |
| **Islands Architecture** | Pattern where static HTML is hydrated with isolated interactive components |
| **E.164** | International phone number format (e.g., +919876543210) |

---

**Document Version**: 1.0  
**Last Updated**: October 29, 2025  
**Authors**: Development Team  
**Status**: Active