from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from .schemas import (
    RegisterIn, RegisterOut,
    PCOut, ACOut, WardGPOut, WardGPPage, LookupOut
)
import re
import time


app = FastAPI(title="Campaign Register API", version="0.2")


# Dev CORS: restrict to your frontend origins only
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "https://aapreg.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------- In-memory data (stub) ----------
PCS: List[PCOut] = [
    PCOut(id="pc-1", code="PC01", name="Sample PC One"),
    PCOut(id="pc-2", code="PC02", name="Sample PC Two"),
]
ACS: List[ACOut] = [
    ACOut(id="ac-1", code="AC01", name="Sample AC A", pc_id="pc-1"),
    ACOut(id="ac-2", code="AC02", name="Sample AC B", pc_id="pc-1"),
    ACOut(id="ac-3", code="AC03", name="Sample AC C", pc_id="pc-2"),
]
WARD_GPS: List[WardGPOut] = [
    WardGPOut(id="w-1", code="W001", name="Ward Alpha", ac_id="ac-1"),
    WardGPOut(id="w-2", code="W002", name="Ward Beta", ac_id="ac-1"),
    WardGPOut(id="w-3", code="W003", name="Ward Gamma", ac_id="ac-2"),
    WardGPOut(id="w-4", code="W004", name="Ward Delta", ac_id="ac-3"),
]


# Temporary registrations store with dedupe by phone
STORE: Dict[str, RegisterIn] = {}


# --------- Helpers ----------
def normalize_phone_to_e164(phone: str) -> str:
    digits = re.sub(r"\D", "", phone or "")
    if len(digits) == 10:
        return f"+91{digits}"
    if digits.startswith("91") and len(digits) == 12:
        return f"+{digits}"
    if digits.startswith("0") and len(digits) == 11:
        return f"+91{digits[1:]}"
    if digits.startswith("+") and len(digits) >= 11:
        return digits
    raise HTTPException(status_code=422, detail="Invalid Indian phone; provide 10 digits")


def find_pc(pc_id: str) -> PCOut | None:
    return next((x for x in PCS if x.id == pc_id), None)


def find_ac(ac_id: str) -> ACOut | None:
    return next((x for x in ACS if x.id == ac_id), None)


def find_ward(ward_id: str) -> WardGPOut | None:
    return next((x for x in WARD_GPS if x.id == ward_id), None)


# --------- Health & root ----------
@app.get("/healthz")
def health():
    return {"ok": True, "ts": int(time.time())}


@app.get("/")
def root():
    return {"message": "OK. Use /docs for API and serve frontend on http://localhost:8080/frontend/index.html"}


# --------- Public list endpoints ----------
@app.get("/list/pc", response_model=List[PCOut])
def list_pc():
    return PCS


@app.get("/list/ac", response_model=List[ACOut])
def list_ac(pc_id: str = Query(..., description="Parent PC id")):
    return [x for x in ACS if x.pc_id == pc_id]


@app.get("/list/ward_gp", response_model=WardGPPage)
def list_ward_gp(ac_id: str, page: int = 1, page_size: int = 20, q: str | None = None):
    items = [x for x in WARD_GPS if x.ac_id == ac_id]
    if q:
        ql = q.lower()
        items = [x for x in items if ql in x.name.lower() or ql in x.code.lower()]
    total = len(items)
    start = (page - 1) * page_size
    return WardGPPage(items=items[start:start+page_size], page=page, page_size=page_size, total=total)


# --------- Reverse lookup (stub) ----------
@app.get("/lookup", response_model=LookupOut)
def lookup(lat: float, lng: float):
    # Stub: pick a deterministic ward for now; integrate real resolver later
    ward = WARD_GPS[0]
    ac = find_ac(ward.ac_id)
    pc = find_pc(ac.pc_id) if ac else None
    return LookupOut(
        ward_gp_id=ward.id, ward_gp_name=ward.name,
        ac_id=ac.id, ac_name=ac.name,
        pc_id=pc.id, pc_name=pc.name,
        source="stub"
    )


# --------- Registration ----------
@app.post("/api/register", response_model=RegisterOut, status_code=201)
def register(reg: RegisterIn):
    phone_e164 = normalize_phone_to_e164(reg.phone)
    if not find_pc(reg.pc_id) or not find_ac(reg.ac_id) or not find_ward(reg.ward_gp_id):
        raise HTTPException(status_code=422, detail="Invalid governance ids")
    # Dedupe by phone: update existing or create new
    existing_id = None
    for rid, r in STORE.items():
        if normalize_phone_to_e164(r.phone) == phone_e164:
            existing_id = rid
            break
    if existing_id:
        STORE[existing_id] = reg
        return {"id": existing_id, "status": "updated"}
    STORE[reg.id] = reg
    return {"id": reg.id, "status": "created"}
