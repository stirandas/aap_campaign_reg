from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class RegistrationIn(BaseModel):
    id: str = Field(..., description="Client-generated UUID")
    name: str
    phone: str
    email: Optional[EmailStr] = None
    district: str
    mandal: str
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    utm_campaign: Optional[str] = None
    createdAt: int

class RegistrationOut(BaseModel):
    id: str
    status: str
