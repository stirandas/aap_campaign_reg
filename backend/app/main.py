from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from . import schemas, crud
from .database import get_db
import re

app = FastAPI(title="Campaign Register API", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://192.168.1.37:8080",  # ipv4 compatible i.e., access desktop app from mobile on same network
        "https://aapreg.web.app",
        "https://aap-campaign-reg.firebaseapp.com"  # Alt Firebase URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Campaign Registration API v1.0"}

@app.get("/healthz")
def health():
    return {"ok": True}

# ========== LIST ENDPOINTS ==========

@app.get("/list/state", response_model=list[schemas.StateOut])
async def list_states(db: AsyncSession = Depends(get_db)):
    """Get all states"""
    states = await crud.get_all_states(db)
    return [
        schemas.StateOut(state_id=s.state_id, state_name=s.state_name)
        for s in states
    ]

@app.get("/list/district", response_model=list[schemas.DistrictOut])
async def list_districts(
    state_id: int = Query(..., description="State ID"),
    db: AsyncSession = Depends(get_db)
):
    """Get districts for a state"""
    districts = await crud.get_districts_by_state(db, state_id)
    
    if not districts:
        raise HTTPException(status_code=404, detail="No districts found for this state")
    
    return [
        schemas.DistrictOut(
            district_id=d.district_id,
            state_id=d.state_id,
            district_name=d.district_name
        )
        for d in districts
    ]

@app.get("/list/mandal", response_model=list[schemas.MandalOut])
async def list_mandals(
    district_id: int = Query(..., description="District ID"),
    db: AsyncSession = Depends(get_db)
):
    """Get mandals for a district"""
    mandals = await crud.get_mandals_by_district(db, district_id)
    
    if not mandals:
        raise HTTPException(status_code=404, detail="No mandals found for this district")
    
    return [
        schemas.MandalOut(
            mandal_id=m.mandal_id,
            district_id=m.district_id,
            mandal_name=m.mandal_name
        )
        for m in mandals
    ]

# ========== REGISTRATION ENDPOINT ==========

@app.post("/register", response_model=schemas.RegisterOut)
async def register(
    payload: schemas.RegisterIn,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user with auto-create village"""
    
    # Normalize phone to E.164 format
    phone_normalized = normalize_phone(payload.phone)
    
    # Get or create village
    village = await crud.get_or_create_village(
        db,
        mandal_id=payload.mandal_id,
        village_name=payload.village_name.strip().title()
    )
    
    # Create registration
    registration_data = {
        "name": payload.name,
        "phone_e164": phone_normalized,
        "email": payload.email,
        "state_id": payload.state_id,
        "district_id": payload.district_id,
        "mandal_id": payload.mandal_id,
        "village_id": village.village_id,
        "utm_source": payload.utm_source,
        "utm_medium": payload.utm_medium,
        "utm_campaign": payload.utm_campaign,
    }
    
    registration = await crud.create_registration(db, registration_data)
    
    if not registration:
        raise HTTPException(status_code=409, detail="Phone number already registered")
    
    return schemas.RegisterOut(
        registration_id=registration.registration_id,
        village_id=village.village_id,
        status="success"
    )

# ========== HELPER FUNCTIONS ==========

def normalize_phone(phone: str) -> str:
    """Normalize phone to E.164 format (+91XXXXXXXXXX)"""
    cleaned = re.sub(r'\D', '', phone)
    
    if len(cleaned) == 10:
        return f"+91{cleaned}"
    elif len(cleaned) == 12 and cleaned.startswith("91"):
        return f"+{cleaned}"
    else:
        raise HTTPException(status_code=400, detail="Invalid phone number format")
