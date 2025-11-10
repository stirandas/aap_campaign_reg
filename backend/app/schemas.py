from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# INPUT SCHEMAS
class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    phone: str  # 10 digits client-side; normalize to E.164 server-side
    email: Optional[EmailStr] = None
    state_id: int
    district_id: int
    mandal_id: int
    village_name: str = Field(min_length=2, max_length=100)
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None

# OUTPUT SCHEMAS
class RegisterOut(BaseModel):
    registration_id: int
    village_id: int
    status: str

class StateOut(BaseModel):
    state_id: int
    state_name: str

class DistrictOut(BaseModel):
    district_id: int
    state_id: int
    district_name: str

class MandalOut(BaseModel):
    mandal_id: int
    district_id: int
    mandal_name: str

class VillageOut(BaseModel):
    village_id: int
    mandal_id: int
    village_name: str
