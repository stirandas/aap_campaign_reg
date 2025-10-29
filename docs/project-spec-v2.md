# Project Specification v2.0
**Mobile-First PWA for Campaign Onboarding (QR + Auto-Fill)**

## Key Revisions from v1.0

### Data Model Changes
- **REMOVED**: `isUrban` flag from governance capture
- **REMOVED**: `dataset_version` field from all schemas
- **REMOVED**: Consent text version and timestamp storage (consent is UI-only gating now)
- **SIMPLIFIED**: Governance fields remain PC/AC/Ward-GP but no metadata tracking

### UX/UI Changes
- **REMOVED**: "Enter manually" secondary link (auto-fallback on geolocation denial)
- **ENHANCED**: Touch-based validation (red/green borders only after blur, not on load)
- **ENHANCED**: Modern gradient UI with Inter font, animations, and accessibility improvements
- **IMPROVED**: Consent checkbox now gates Submit button but does not transmit consent metadata

### Backend Changes
- **REMOVED**: Consent validation from POST /api/register
- **REMOVED**: isUrban, version fields from GET /lookup response
- **SIMPLIFIED**: RegisterIn schema drops consent_text_version, consent_ts, dataset_version, isUrban

### Flow Changes
- **AUTO-FALLBACK**: Geolocation denial/failure automatically loads manual PC list and focuses PC input
- **CLIENT-ONLY CONSENT**: Checkbox blocks submission on frontend; no server-side consent audit trail

---

## Project Overview

**Title**: Mobile-First PWA for Campaign Onboarding (QR + Auto-Fill)

**Objective**: Rapidly onboard citizens at campaign events via QR code with a mobile-first, offline-capable PWA that auto-populates identity fields and precise governance fields for accurate downstream outreach.

### Scope and Goals
- One-screen, high-conversion registration flow optimized for first-time, one-time users
- Fast first paint, low interaction latency, resilient offline behavior, and privacy-first data handling
- Accurate capture of governance hierarchy via auto-detect or manual cascade

---

## Data Captured

### Identity
- **Name**: required
- **Phone**: required; India default (+91) 10-digit with masking, normalize to E.164 on submit
- **Email**: optional; strongly recommended helper text to encourage entry if available

### Governance (all required)
- **Parliamentary Constituency (PC)**
- **Assembly Constituency (AC)**
- **Ward/Gram Panchayat (Ward/GP)**

### Consent
- **Mandatory checkbox**: "I consent to receive updates about AAP community service campaigns"
- **UI-only gating**: Submission is blocked until consent is checked; **no consent metadata stored** (no text version, no timestamp)

---

## Core User Flow

1. Scan QR → PWA page opens instantly (no install)
2. Tap **"Quick Register with Auto-Fill"**
3. Browser offers Name/Phone/Email via autocomplete; user may accept or edit
4. **If location permission granted**:
   - Get coordinates → lookup Ward/GP → derive AC and PC → preselect all three dropdowns
   - Show "Detected from your location" toast with option to manually change
5. **If permission denied/fails**:
   - **Auto-fallback**: PC list loads automatically and PC input receives focus
   - Manual cascade: select PC → load AC list filtered by PC → load Ward/GP list filtered by AC
6. User reviews fields, checks mandatory consent, and submits
7. Submission queues locally if offline and syncs automatically when online

---

## Rendering and Application Architecture

### Rendering Mode: SSG + Client Islands
- **SSG shell**: pre-render static HTML for layout, labels, Name/Phone/Email inputs, consent checkbox, and skeleton placeholders for PC/AC/Ward-GP dropdowns; served via CDN for instant first paint
- **Client islands**:
  - **Dropdowns island**: typeahead, cascade, virtualization
  - **Geolocation island**: permission request + lookup
  - Hydrate dropdowns immediately; hydrate geolocation after first paint or on interaction

### Offline-First
- **Service Worker**: caches the SSG shell and static assets; Background Sync enqueues and flushes submissions
- **IndexedDB**: caches submissions, last-used selections, and recent list pages

---

## Governance Data Logic

### Auto-Detect Path
- Use coordinates strictly for polygon membership; resolve to the smallest unit (Ward/GP)
- Derive AC and PC via precomputed parentage tables
- **Near-boundary handling**: show accuracy note; allow quick manual correction

### Manual Cascade Path
1. **Dropdown 1**: PC list with typeahead
2. **Dropdown 2**: AC list filtered by selected PC
3. **Dropdown 3**: Ward/GP list filtered by selected AC

### Consistency
- If user picks a Ward/GP implying different parents, automatically correct AC/PC and toast a brief notification

---

## Validation Rules

### Required Fields
Name, Phone, PC, AC, Ward/GP, and Consent must be valid/checked to enable Submit.

### Field-Specific Rules
- **Name**: 2–120 chars; trim/normalize; allow letters, spaces, hyphens, apostrophes, local scripts
- **Phone**: 10 digits for India path with mask; on submit, normalize to E.164; surface validation errors inline
- **Email**: optional; validate format only if present; show non-blocking helper text recommending entry
- **Dropdowns**: required; show inline errors if empty on submit; typeahead debounced 200–300 ms
- **Validation Timing**: Show red/green borders only after user blur (touched state), not on page load

---

## Form UX Design

### CTAs
- **Primary**: "Submit" (large, gradient blue, disabled until consent + required fields valid)
- **Secondary**: "Quick Register with Auto-Fill" (smaller, light blue background)

### Inputs
- **Name**: `autocomplete="name"`
- **Phone**: `autocomplete="tel"` + numeric keypad
- **Email**: `autocomplete="email"`
- Required fields marked with "*"; "Email (optional)" label clarifies optionality

### Dropdowns
- Show code + name in results
- Virtualized list rendering for large sets
- Clear/reset affordances

### Consent
- Checkbox displayed above Submit
- Submit disabled until consent is checked and required fields valid

### Success Screen
- Clear confirmation message
- Optional: social share, next steps

---

## APIs and Backend

### Public APIs (edge-hosted for low latency)

#### GET /list/pc
Returns list of Parliamentary Constituencies.

**Response**: 
```json
[
  { "id": "pc-1", "code": "PC01", "name": "Sample PC One" },
  { "id": "pc-2", "code": "PC02", "name": "Sample PC Two" }
]
```

**Caching**: Long max-age + ETag

---

#### GET /list/ac?pc_id=...
Returns Assembly Constituencies filtered by PC.

**Response**: 
```json
[
  { "id": "ac-1", "code": "AC01", "name": "Sample AC A", "pc_id": "pc-1" }
]
```

**Caching**: Long max-age + ETag

---

#### GET /list/ward_gp?ac_id=...&page=...&q=...
Returns Ward/GPs (paged, searchable) filtered by AC.

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

**Caching**: Long max-age + ETag; client memoizes by parent id

---

#### GET /lookup?lat=...&lng=...
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

**Caching**: Short TTL

---

### Registration Backend

#### POST /api/register
Validates payload, dedupes by phone (upsert), stores registration.

**Request**:
```json
{
  "id": "uuid",
  "name": "string",
  "phone": "string (10 digits client-side)",
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

**Response**: 
```json
{
  "id": "uuid",
  "status": "created" | "updated"
}
```
(201 Created)

**Validation**:
- Normalize phone to E.164 (+91...)
- Validate PC/AC/Ward-GP exist
- Dedupe by normalized phone (upsert)

---

#### GET /api/stats
Aggregates and returns counts grouped by PC/AC/Ward-GP and source.

---

#### GET /api/export
Streams CSV for outreach filtered by PC/AC/Ward-GP, date, and UTM source. Includes optional Email field.

---

### Store
- **PostgreSQL** with backups (Phase 2)
- Role-based dashboard access
- Audit logs for edits

---

## Data Sources, Identifiers, and Versioning

### Constituency Boundaries
- PC and AC polygons with official/community codes
- Aligned to the latest delimitation where applicable

### Ward/Gram Panchayat
- Authoritative administrative datasets normalized to LGD codes
- Maintain parentage tables: Ward/GP → AC → PC

### Versioning
- **REMOVED**: No `dataset_version` tracking in payload or storage

---

## Privacy, Security, and Compliance

### Geolocation
- Explicit permission request with clear purpose specific to PC/AC/Ward-GP auto-fill
- Do not store raw coordinates unless necessary

### Consent Management
- **Client-side gating only**: mandatory checkbox blocks submission
- **No server-side storage**: consent text version and timestamp not captured or stored
- Honor opt-out for communications via separate mechanisms

### Transport and API Security
- HTTPS/TLS
- CORS (restrict to known origins)
- Rate limiting, input validation, logging, and monitoring

---

## Performance Requirements

### First Paint
Instant via SSG shell from CDN

### Interaction Latency
Sub-150 ms round-trips for list fetching and lookups on median connections through edge APIs

### Bundling
- Code-split islands
- Defer optional map code
- Compress assets
- HTTP/2 or HTTP/3

### Main Thread
Use Web Workers if any heavy client-side geometry is introduced; otherwise resolve via edge lookup

---

## Accessibility and Localization

### Accessibility
- ARIA-compliant comboboxes
- Keyboard navigation
- High-contrast and large touch targets
- Error summary and inline messages for screen readers

### Localization
- Support local scripts in Name and in search aliases for governance names
- Pluralization and transliteration where applicable

---

## Analytics and Reporting

### Metrics
- Registrations
- Auto-detect vs manual split
- Correction rate (auto-corrected AC/PC)
- Permission grant rate
- List/lookup latency p95

### Funnel
View → autofill attempt → permission result → governance resolution → consent checked → submit success

### Exports
- Scheduled CSVs filtered by PC/AC/Ward-GP, date, and UTM source
- Include optional Email field

---

## Testing Plan

### Unit
- Validation for Name/Phone/Email
- Cascade logic
- Parent-child corrections
- Consent gating (UI-only)

### Integration
- Geolocation grant/deny
- Lookup results
- List pagination and search debounce
- Offline queue and retry

### E2E
- Cold-start FCP/LCP on mid/low-end devices
- Offline-to-online sync
- Submission idempotency
- Accessibility checks

---

## Deployment

### Static SSG Build
- Deploy to CDN with immutable content hashing
- Cache-busting via versioned filenames

### Edge Deployments
- List/lookup APIs in primary user regions
- Low-latency responses via edge caching

### Environment Configuration
- Keys/secrets server-side only
- No sensitive keys in client code

---

## Build Plan (MVP ~1 week)

### Days 1–2
- SSG shell
- Service Worker
- IndexedDB queue
- Base form (Name, Phone, Email optional with recommendation, consent checkbox)
- Skeleton states

### Days 3–4
- Client islands for dropdowns and geolocation
- List/lookup APIs
- Cascade, validation, and consent gating (UI-only)

### Days 5–6
- Analytics counters
- Exports
- Dedupe in Postgres
- QR/UTM rollout
- Privacy copy

### Day 7
- Performance tuning
- Accessibility and offline QA
- Deploy to CDN and edge

---

## Version Control Summary

### For Git Commit Message

```
feat(spec): update project requirements to v2.0

BREAKING CHANGES:
- Remove isUrban, dataset_version, consent metadata from data model
- Consent is now UI-only gating (not persisted server-side)

UX/UI:
- Add auto-fallback to manual cascade on geolocation denial
- Implement touch-based validation (blur-triggered borders)
- Enhance UI with gradient theme, Inter font, animations

Backend:
- Simplify RegisterIn schema (remove consent fields)
- Remove consent validation from POST /api/register
- Simplify GET /lookup response

Docs:
- Add project-spec-v2.md with complete revision tracking
- Update API contracts and validation rules
- Clarify consent as client-side gating only
```

---

**Document Version**: 2.0  
**Last Updated**: October 29, 2025  
**Status**: Active Development (MVP Phase)