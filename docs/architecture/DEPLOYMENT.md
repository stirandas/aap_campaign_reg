# Deployment Guide - AAP Campaign Registration System

This guide covers deployment procedures for frontend (Firebase) and backend (Google Cloud Run).

---

## Prerequisites

### Required Tools
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Install Firebase CLI
npm install -g firebase-tools
firebase login

# Install Poetry (for backend)
curl -sSL https://install.python-poetry.org | python3 -
```

### Required Accounts
- Google Cloud Platform account
- Firebase project
- Supabase account (or PostgreSQL database)

---

## Part 1: Database Setup (Supabase)

### 1.1 Create Supabase Project
1. Go to https://supabase.com
2. Create new project: `aap-campaign-reg`
3. Copy connection string from Settings → Database

### 1.2 Run Migrations
```bash
cd backend
export DATABASE_URL="postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres"
poetry install
poetry run alembic upgrade head
```

### 1.3 Seed Data
```bash
# Insert states, districts, mandals
poetry run python seed_data.py
```

---

## Part 2: Backend Deployment (Cloud Run)

### 2.1 Setup GCP Project
```bash
# Create project
gcloud projects create aap-campaign-reg --name="AAP Campaign Reg"

# Set project
gcloud config set project aap-campaign-reg

# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 2.2 Build and Deploy
```bash
cd backend

# Deploy to Cloud Run
gcloud run deploy aap-campaign-reg-backend \
  --source . \
  --region asia-south1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --set-env-vars DATABASE_URL=$DATABASE_URL

# Get service URL
gcloud run services describe aap-campaign-reg-backend \
  --region asia-south1 \
  --format='value(status.url)'
```

### 2.3 Update CORS Origins
Edit `backend/main.py` and add production URL:
```python
allow_origins=[
    "https://aapreg.web.app",
    "https://aap-campaign-reg.firebaseapp.com"
]
```

Redeploy:
```bash
gcloud run deploy aap-campaign-reg-backend \
  --source . \
  --region asia-south1
```

---

## Part 3: Frontend Deployment (Firebase)

### 3.1 Setup Firebase Project
```bash
cd frontend
firebase login
firebase init hosting

# Select options:
# - Use existing project: aap-campaign-reg
# - Public directory: . (current directory)
# - Configure as single-page app: No
# - Set up automatic builds: No
```

### 3.2 Update API URL
Edit `main.js` line 5-10:
```javascript
const API_BASE = 'https://aap-campaign-reg-backend-[PROJECT_ID].asia-south1.run.app';
```

### 3.3 Deploy
```bash
firebase deploy --only hosting

# Get hosting URL
firebase hosting:sites:get
```

---

## Part 4: Post-Deployment Checks

### 4.1 Test Backend
```bash
# Health check
curl https://your-backend-url.run.app/healthz

# List states
curl https://your-backend-url.run.app/list/state

# Test registration (should fail with 422)
curl -X POST https://your-backend-url.run.app/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","phone":"1234567890","state_id":1,"district_id":1,"mandal_id":1,"village_name":"Test"}'
```

### 4.2 Test Frontend
1. Open `https://aapreg.web.app`
2. Fill form with test data
3. Check browser console for errors
4. Submit registration
5. Verify success message

### 4.3 Test Offline Mode
1. Open app on mobile
2. Turn on Airplane mode
3. Fill and submit form
4. Verify "Queued for sync" message
5. Turn off Airplane mode
6. Verify auto-sync

---

## Part 5: Environment Variables

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Frontend (main.js)
```javascript
const API_BASE = process.env.API_BASE || 'https://your-backend.run.app';
const DEFAULT_STATE = 'Andhra Pradesh';
```

---

## Part 6: Rollback Procedures

### Backend Rollback
```bash
# List revisions
gcloud run revisions list --service aap-campaign-reg-backend --region asia-south1

# Rollback to specific revision
gcloud run services update-traffic aap-campaign-reg-backend \
  --region asia-south1 \
  --to-revisions [REVISION_NAME]=100
```

### Frontend Rollback
```bash
# List previous releases
firebase hosting:releases:list

# Rollback to specific release
firebase hosting:clone [SOURCE_SITE_ID]:[RELEASE_ID] [TARGET_SITE_ID]
```

---

## Part 7: Monitoring Setup

### Cloud Run Monitoring
```bash
# View logs
gcloud run logs read aap-campaign-reg-backend --region asia-south1 --limit 50

# View metrics
gcloud monitoring dashboards create --config-from-file=monitoring/dashboard.json
```

### Uptime Monitoring (optional)
1. Go to Cloud Console → Monitoring → Uptime checks
2. Create check for backend URL `/healthz`
3. Set alert threshold: 99% availability

### Error Tracking (Sentry)
```bash
# Add to backend requirements
poetry add sentry-sdk[fastapi]

# Add to main.py
import sentry_sdk
sentry_sdk.init(dsn="YOUR_SENTRY_DSN")
```

---

## Part 8: Backup & Recovery

### Database Backups
```bash
# Supabase provides automatic daily backups
# Manual backup:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Restore:
psql $DATABASE_URL < backup_20251110.sql
```

### Code Backups
```bash
# Tag release
git tag -a v2.0 -m "Production release v2.0"
git push origin v2.0

# Create GitHub release
gh release create v2.0 --title "Version 2.0" --notes "Production deployment"
```

---

## Part 9: Cost Optimization

### Cloud Run
- **Free Tier:** 2M requests/month, 360K GB-seconds
- **Optimization:** 
  - Set min-instances: 0 (scale to zero)
  - Use 512Mi memory (sufficient for FastAPI)
  - Set max-instances: 10 (prevent runaway costs)

### Firebase Hosting
- **Free Tier:** 10GB storage, 360MB/day transfer
- **Optimization:** Enable compression, cache static assets

### Supabase
- **Free Tier:** 500MB database, 2GB transfer
- **Optimization:** 
  - Use connection pooling
  - Add database indexes
  - Archive old registrations

---

## Part 10: Troubleshooting

### Issue: 502 Bad Gateway
**Cause:** Backend not responding  
**Solution:**
```bash
# Check logs
gcloud run logs read aap-campaign-reg-backend --region asia-south1 --limit 50

# Check service status
gcloud run services describe aap-campaign-reg-backend --region asia-south1
```

### Issue: CORS Error
**Cause:** Frontend origin not whitelisted  
**Solution:** Update `allow_origins` in `main.py`, redeploy

### Issue: Database Connection Timeout
**Cause:** Too many connections  
**Solution:** Enable Supabase connection pooler, use `?pgbouncer=true`

---

## Contact

For deployment issues, contact:
- **DevOps:** devops@aapandhra.org
- **Slack:** #aap-campaign-tech

---

**Last Updated:** November 10, 2025
