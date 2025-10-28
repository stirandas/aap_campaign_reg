from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from .schemas import RegistrationIn, RegistrationOut

app = FastAPI(title="Campaign Register API", version="0.1")

# Allow local dev frontends; tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080","http://127.0.0.1:8080","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary in-memory store for MVP wiring
STORE: Dict[str, RegistrationIn] = {}

@app.get("/healthz")
def health():
    return {"ok": True}

@app.post("/api/register", response_model=RegistrationOut, status_code=201)
def register(reg: RegistrationIn):
    # Upsert by phone for now (scan store). Replace with DB later.
    existing_id = None
    for _id, r in STORE.items():
        if r.phone == reg.phone:
            existing_id = _id
            break
    if existing_id:
        STORE[existing_id] = reg
        return {"id": existing_id, "status": "updated"}
    STORE[reg.id] = reg
    return {"id": reg.id, "status": "created"}
