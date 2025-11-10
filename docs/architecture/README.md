# AAP Campaign Registration System

A Progressive Web App for citizen registration in AAP's social service activities across Andhra Pradesh.

![Version](https://img.shields.io/badge/version-2.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ (for Firebase CLI)
- PostgreSQL database (or Supabase account)
- Google Cloud account (for Cloud Run)
- Firebase account (for hosting)

### Installation

**1. Clone Repository**
```bash
git clone https://github.com/your-org/aap-campaign-reg.git
cd aap-campaign-reg
```

**2. Backend Setup**
```bash
cd backend
poetry install
cp .env.example .env
# Edit .env and add DATABASE_URL

# Run migrations
poetry run alembic upgrade head

# Start dev server
poetry run uvicorn main:app --reload
```

**3. Frontend Setup**
```bash
cd frontend
# Edit main.js and set API_BASE for local dev
# Open index.html in browser or use Live Server
```

---

## 📁 Project Structure

```
aap-campaign-reg/
├── frontend/
│   ├── index.html           # Main registration form
│   ├── main.js              # Form logic, validation, API calls
│   ├── db.js                # IndexedDB for offline queue
│   ├── sw.js                # Service Worker
│   ├── images/              # Logo and assets
│   └── manifest.webmanifest # PWA manifest
├── backend/
│   ├── main.py              # FastAPI routes
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic validation schemas
│   ├── crud.py              # Database operations
│   ├── database.py          # Database connection
│   ├── alembic/             # Database migrations
│   ├── Dockerfile           # Container config
│   └── pyproject.toml       # Poetry dependencies
├── ARCHITECTURE.md          # Architecture documentation
└── README.md                # This file
```

---

## 🛠️ Technology Stack

### Frontend
- **Vanilla JavaScript** (ES2020) - No framework overhead
- **HTML5 + CSS3** - Semantic markup, Flexbox layout
- **Service Worker** - Offline caching
- **IndexedDB** - Offline registration queue

### Backend
- **FastAPI** (Python) - High-performance async API
- **Pydantic** - Request/response validation
- **SQLAlchemy** - Async ORM
- **PostgreSQL** - Relational database

### Infrastructure
- **Firebase Hosting** - CDN for frontend
- **Google Cloud Run** - Serverless backend containers
- **Supabase** - Managed PostgreSQL database

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/list/state` | Get all states |
| GET | `/list/district?state_id=X` | Get districts by state |
| GET | `/list/mandal?district_id=X` | Get mandals by district |
| POST | `/register` | Submit registration |

**Sample Registration:**
```json
POST /register
{
  "name": "Rajesh Kumar",
  "phone": "9876543210",
  "email": "rajesh@example.com",
  "state_id": 1,
  "district_id": 15,
  "mandal_id": 234,
  "village_name": "Chilakaluripet"
}
```

---

## 🚢 Deployment

### Frontend (Firebase)
```bash
cd frontend
firebase login
firebase deploy --only hosting
```

### Backend (Google Cloud Run)
```bash
cd backend
gcloud run deploy aap-campaign-reg-backend \
  --source . \
  --region asia-south1 \
  --set-env-vars DATABASE_URL=$DATABASE_URL \
  --allow-unauthenticated
```

### Database Migrations
```bash
cd backend
poetry run alembic revision --autogenerate -m "Description"
poetry run alembic upgrade head
```

---

## 🎯 Features

✅ **Mobile-First Design** - Optimized for smartphones  
✅ **Offline Support** - Queue registrations without internet  
✅ **Real-Time Validation** - Instant feedback on form fields  
✅ **Location Hierarchy** - State → District → Mandal → Village  
✅ **Duplicate Prevention** - Phone number uniqueness  
✅ **Progressive Web App** - Install on home screen  
✅ **Responsive Layout** - Works on 360px+ screens  

---

## 📊 Database Schema

```
states (1:N)
    ↓
districts (1:N)
    ↓
mandals (1:N)
    ↓
villages (1:N)
    ↓
registrations
```

**Key Tables:**
- `states` - 29 Indian states
- `districts` - Districts per state
- `mandals` - Mandals per district
- `villages` - Auto-created on registration
- `registrations` - User submissions (phone UNIQUE)

---

## 🔧 Configuration

### Frontend (main.js)
```javascript
// Change for multi-state support
const DEFAULT_STATE = 'Andhra Pradesh';  // Set to null for multi-state

// API endpoint
const API_BASE = 'https://your-backend.run.app';
```

### Backend (main.py)
```python
# CORS origins
allow_origins=[
    "https://aapreg.web.app",
    "http://localhost:8080"
]
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
poetry run pytest
```

### Frontend Tests
```bash
cd frontend
npm run test:e2e  # Playwright E2E tests
```

---

## 📈 Monitoring

### Logs
```bash
# Cloud Run logs
gcloud run logs read aap-campaign-reg-backend --region asia-south1

# Firebase logs
firebase hosting:logs
```

### Metrics
- **Cloud Run:** CPU, Memory, Request count, Latency
- **Firebase:** Page views, Load time, Cache hit rate
- **Supabase:** Connection pool, Query performance

---

## 🐛 Known Issues

1. **No OTP Verification** - Phone numbers not verified (planned)
2. **Village Duplicates** - Typos create duplicate villages (needs cleanup tool)
3. **No Admin Panel** - Manual SQL queries needed for reports
4. **No Rate Limiting** - Potential for spam submissions

See [ARCHITECTURE.md](ARCHITECTURE.md) for full technical debt list.

---

## 🗺️ Roadmap

### v2.1 (Next Release)
- [ ] Phone OTP verification
- [ ] Admin dashboard
- [ ] Export to CSV/Excel
- [ ] Rate limiting

### v3.0 (Future)
- [ ] Multi-state support
- [ ] Analytics dashboard
- [ ] Duplicate detection tool
- [ ] Profile photo upload

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📞 Support

- **Email:** support@aapandhra.org
- **Issues:** [GitHub Issues](https://github.com/your-org/aap-campaign-reg/issues)
- **Docs:** [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Built with ❤️ for AAP Andhra Pradesh**
