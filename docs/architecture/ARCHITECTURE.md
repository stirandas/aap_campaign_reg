# AAP Campaign Registration System - Architecture Documentation

**Version:** 2.0  
**Last Updated:** November 10, 2025  
**Project:** AAP Social Service Campaign Registration (Andhra Pradesh)

---

## Table of Contents

1. [Introduction & Goals](#1-introduction--goals)
2. [Constraints](#2-constraints)
3. [Context & Scope](#3-context--scope)
4. [Solution Strategy](#4-solution-strategy)
5. [Building Block View](#5-building-block-view)
6. [Runtime View](#6-runtime-view)
7. [Deployment View](#7-deployment-view)
8. [Crosscutting Concepts](#8-crosscutting-concepts)
9. [Architectural Decisions](#9-architectural-decisions)
10. [Quality Requirements](#10-quality-requirements)
11. [Risks & Technical Debt](#11-risks--technical-debt)

---

## 1. Introduction & Goals

### Project Overview
A Progressive Web App (PWA) for capturing citizen registrations for AAP's social service activities in Andhra Pradesh. The system enables field workers and citizens to register with their location details (District, Mandal, Village) even in offline conditions.

### Business Goals
- Enable grassroots volunteer registration across Andhra Pradesh
- Support offline-first data collection for field workers with unreliable connectivity
- Capture demographic and location data with hierarchical validation
- Prevent duplicate registrations (by phone number)

### Quality Goals
1. **Availability:** 99.5% uptime
2. **Performance:** Form submission < 2 seconds (online)
3. **Usability:** Mobile-first, accessible on low-end Android devices
4. **Offline Support:** Queue registrations for up to 7 days
5. **Data Integrity:** No duplicate phone registrations

### Stakeholders
- **End Users:** Citizens of Andhra Pradesh (18+ voters)
- **Field Workers:** AAP volunteers collecting registrations
- **Campaign Managers:** Viewing analytics and reports
- **Developers:** Maintenance and feature development (1-2 developers)

---

## 2. Constraints

### Technical Constraints
- **Frontend:** Vanilla JavaScript (no framework) for lightweight PWA
- **Backend:** Python FastAPI (async) for API performance
- **Database:** PostgreSQL on Supabase (managed service)
- **Hosting:** Firebase Hosting (frontend), Google Cloud Run (backend)
- **Budget:** Low-cost cloud services (<$50/month)

### Organizational Constraints
- **Geographic Scope:** Currently Andhra Pradesh only (future multi-state)
- **Team Size:** 1-2 developers
- **Timeline:** Rapid deployment (MVP in 2 weeks)

### Conventions
- RESTful API design
- Mobile-first responsive design
- PWA standards (Service Worker, offline support)
- Single-state mode with easy multi-state expansion

---

## 3. Context & Scope

### System Context (C4 Level 1)

```
┌─────────────────────────────────────────────────────────────────┐
│                        System Context                            │
│                                                                  │
│   ┌──────────┐                                                  │
│   │ Citizens │───┐                                              │
│   │ (Mobile) │   │                                              │
│   └──────────┘   │                                              │
│                  │                                              │
│   ┌──────────┐   │         ┌──────────────────────────┐        │
│   │  Field   │───┼────────▶│  AAP Campaign Reg        │        │
│   │ Workers  │   │         │  System (PWA + API)      │        │
│   └──────────┘   │         └──────────────────────────┘        │
│                  │                    │                         │
│   ┌──────────┐   │                    │                         │
│   │ Campaign │───┘                    │                         │
│   │ Managers │                        ▼                         │
│   └──────────┘                ┌──────────────┐                 │
│                                │  Supabase    │                 │
│                                │ PostgreSQL   │                 │
│                                └──────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

### External Interfaces
- **Users:** Mobile browsers (Chrome, Firefox, Safari, Edge)
- **Firebase Hosting:** CDN serving PWA static files
- **Google Cloud Run:** Serverless FastAPI backend (asia-south1)
- **Supabase:** Managed PostgreSQL database with connection pooling

---

## 4. Solution Strategy

### Key Architectural Decisions

#### 4.1 PWA Architecture
- **Offline-First:** Service Worker caches static assets
- **Local Queue:** IndexedDB stores registrations when offline
- **Background Sync:** Auto-syncs when connectivity restored
- **Responsive Design:** Mobile-first, works on 360px+ screens

#### 4.2 Location Hierarchy
- **Normalized Model:** State → District → Mandal → Village
- **Dynamic Villages:** Auto-created on first registration
- **Removed Political Boundaries:** Simplified to administrative hierarchy

#### 4.3 Validation Strategy
- **Client-Side:** Real-time validation with visual feedback
- **Server-Side:** Pydantic schemas + phone deduplication
- **Phone:** 10-digit validation, normalized to E.164 format

#### 4.4 State Management
- **Single-State Mode:** Andhra Pradesh hardcoded, field hidden
- **Future-Proof:** DEFAULT_STATE constant for easy multi-state enablement

---

## 5. Building Block View

### Container Diagram (C4 Level 2)

```
┌────────────────────────────────────────────────────────────────┐
│                  AAP Campaign System                            │
│                                                                 │
│  ┌────────────────────────────────────────────────────┐        │
│  │          Frontend (PWA)                            │        │
│  │  • index.html (Form UI with logo/title)           │        │
│  │  • main.js (Form logic, validation, API calls)    │        │
│  │  • db.js (IndexedDB offline queue)                │        │
│  │  • sw.js (Service Worker caching)                 │        │
│  │                                                    │        │
│  │  Hosted: Firebase Hosting                         │        │
│  │  URL: https://aapreg.web.app                      │        │
│  └────────────────┬───────────────────────────────────┘        │
│                   │ HTTPS/JSON                                 │
│                   ▼                                            │
│  ┌────────────────────────────────────────────────────┐        │
│  │          Backend (FastAPI)                         │        │
│  │  • main.py (API routes, CORS)                     │        │
│  │  • schemas.py (Pydantic validation)               │        │
│  │  • models.py (SQLAlchemy ORM)                     │        │
│  │  • crud.py (Database operations)                  │        │
│  │  • database.py (Connection pool)                  │        │
│  │                                                    │        │
│  │  Hosted: Google Cloud Run (asia-south1)           │        │
│  └────────────────┬───────────────────────────────────┘        │
│                   │ SQL over TLS                               │
│                   ▼                                            │
│  ┌────────────────────────────────────────────────────┐        │
│  │          Database (PostgreSQL 15)                  │        │
│  │  Tables: states, districts, mandals,              │        │
│  │          villages, registrations                   │        │
│  │                                                    │        │
│  │  Hosted: Supabase (managed)                        │        │
│  └────────────────────────────────────────────────────┘        │
└────────────────────────────────────────────────────────────────┘
```

---

## 6. Runtime View

### Scenario: User Registration (Online)

```
User Browser → PWA (main.js) → Backend API → Database
     │              │               │             │
     │ Fill form    │               │             │
     ├─────────────▶│               │             │
     │              │ Validate      │             │
     │              │               │             │
     │ Submit       │ POST /register│             │
     ├─────────────▶├──────────────▶│             │
     │              │               │ Check dupe  │
     │              │               ├────────────▶│
     │              │               │ Insert reg  │
     │              │               ├────────────▶│
     │◀─────────────┤◀──────────────┤ 201 Created │
     │ Success      │               │             │
```

### Scenario: Offline Registration

```
User Browser → PWA → IndexedDB → Service Worker → Backend
     │           │        │             │             │
     │ Submit    │        │             │             │
     ├──────────▶│        │             │             │
     │           │ Queue  │             │             │
     │           ├───────▶│             │             │
     │◀──────────┤        │             │             │
     │ Queued    │        │             │             │
     │           │        │  [Online]   │             │
     │           │        │ Sync event  │             │
     │           │        ├────────────▶│ POST queue  │
     │           │        │             ├────────────▶│
     │           │◀───────┤ Clear queue │             │
```

---

## 7. Deployment View

### Infrastructure

```
Internet
   │
   ├──▶ Firebase Hosting (Global CDN)
   │    └── Static Files (index.html, main.js, etc.)
   │
   └──▶ Google Cloud Run (asia-south1)
        └── FastAPI Container
             └── DATABASE_URL → Supabase PostgreSQL
```

### Deployment Commands

**Frontend:**
```bash
firebase deploy --only hosting
```

**Backend:**
```bash
gcloud run deploy aap-campaign-reg-backend \
  --source . \
  --region asia-south1 \
  --set-env-vars DATABASE_URL=$DATABASE_URL
```

---

## 8. Crosscutting Concepts

### Data Model

```
states (1:N) → districts (1:N) → mandals (1:N) → villages
                                                    ↑
                                                    │ (N:1)
                                              registrations
```

### Validation Rules

| Field | Rule | Server Validation |
|-------|------|-------------------|
| Name | 2-120 characters | Pydantic Field |
| Phone | 10 digits, unique | DB constraint |
| Email | Valid format (optional) | EmailStr |
| Village | 2-100 characters | Pydantic Field |

### UI/UX Design

- **Logo:** 88px, top-left corner
- **Title:** 3 lines, left-aligned
  - "Join our social service activities" (20px)
  - "in the state of" (13px, gray)
  - "ANDHRA PRADESH" (24px, bold, purple)
- **Phone & Email:** Side-by-side on desktop, stacked on mobile
- **State Field:** Hidden (auto-selected)
- **Validation:** Red borders on blur for invalid fields

---

## 9. Architectural Decisions

### ADR-001: Remove PC/AC/GP Boundaries
- **Status:** Accepted
- **Decision:** Use State/District/Mandal/Village hierarchy
- **Rationale:** Simpler for citizens to understand
- **Consequences:** Lost political analysis capability

### ADR-002: Vanilla JavaScript Frontend
- **Status:** Accepted
- **Decision:** No React/Vue, use vanilla JS
- **Rationale:** Faster load on 2G/3G networks
- **Consequences:** More boilerplate code

### ADR-003: Auto-Create Villages
- **Status:** Accepted
- **Decision:** get_or_create_village() on registration
- **Rationale:** Can't pre-populate 30,000+ villages
- **Consequences:** Potential typos need cleanup

### ADR-004: Single-State Mode
- **Status:** Accepted
- **Decision:** Hide state field, hardcode Andhra Pradesh
- **Rationale:** Cleaner UX for single-state campaign
- **Consequences:** Code change needed for multi-state

---

## 10. Quality Requirements

### Performance
- Form load (3G): < 3 seconds
- Registration submit: < 2 seconds
- Offline write: < 500ms

### Availability
- Frontend: 99.9% (Firebase)
- Backend: 99.5% (Cloud Run)
- Database: 99.9% (Supabase)

### Security
- TLS 1.3 encryption (HTTPS)
- CORS whitelist
- Phone uniqueness constraint

---

## 11. Risks & Technical Debt

### Current Risks
1. **Supabase downtime** - Daily backups needed
2. **No OTP verification** - Risk of fake entries
3. **Village duplicates** - Need cleanup tool
4. **No rate limiting** - Potential spam

### Technical Debt
1. No automated tests (pytest, Playwright)
2. No CI/CD pipeline (GitHub Actions)
3. No monitoring/alerting (Sentry)
4. Hardcoded configuration (move to env vars)
5. No admin panel for data export

---

## API Specification

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Health check |
| GET | /healthz | Health check |
| GET | /list/state | Get all states |
| GET | /list/district?state_id=X | Get districts |
| GET | /list/mandal?district_id=X | Get mandals |
| POST | /register | Create registration |

### Sample Request

```json
POST /register
{
  "name": "Rajesh Kumar",
  "phone": "9876543210",
  "email": "rajesh@example.com",
  "state_id": 1,
  "district_id": 15,
  "mandal_id": 234,
  "village_name": "Chilakaluripet",
  "utm_source": "whatsapp"
}
```

### Response (201)

```json
{
  "registration_id": 1523,
  "village_id": 789,
  "status": "success"
}
```

---

## Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Frontend | Vanilla JS, HTML5, CSS3 | ES2020 |
| Backend | FastAPI, Pydantic, SQLAlchemy | 0.104+, 2.x |
| Database | PostgreSQL | 15 |
| Hosting | Firebase, Cloud Run, Supabase | - |
| DevOps | Docker, Poetry, Alembic | - |

---

**Document Version:** 2.0  
**Last Updated:** November 10, 2025
