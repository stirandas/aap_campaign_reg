from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List


class RegisterIn(BaseModel):
    id: str
    name: str = Field(min_length=2, max_length=120)
    phone: str  # send 10 digits client-side; normalize to E.164 server-side
    email: Optional[EmailStr] = None
    pc_id: str
    ac_id: str
    ward_gp_id: str
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    createdAt: int


class RegisterOut(BaseModel):
    id: str
    status: str


class PCOut(BaseModel):
    id: str
    code: str
    name: str


class ACOut(BaseModel):
    id: str
    code: str
    name: str
    pc_id: str


class WardGPOut(BaseModel):
    id: str
    code: str
    name: str
    ac_id: str


class WardGPPage(BaseModel):
    items: List[WardGPOut]
    page: int
    page_size: int
    total: int


class LookupOut(BaseModel):
    ward_gp_id: str
    ward_gp_name: str
    ac_id: str
    ac_name: str
    pc_id: str
    pc_name: str
    source: str
