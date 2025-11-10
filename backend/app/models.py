from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class State(Base):
    __tablename__ = "states"
    
    state_id = Column(Integer, primary_key=True, index=True)
    state_name = Column(String(100), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    districts = relationship("District", back_populates="state")

class District(Base):
    __tablename__ = "districts"
    
    district_id = Column(Integer, primary_key=True, index=True)
    state_id = Column(Integer, ForeignKey("states.state_id"), nullable=False, index=True)
    district_name = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    state = relationship("State", back_populates="districts")
    mandals = relationship("Mandal", back_populates="district")

class Mandal(Base):
    __tablename__ = "mandals"
    
    mandal_id = Column(Integer, primary_key=True, index=True)
    district_id = Column(Integer, ForeignKey("districts.district_id"), nullable=False, index=True)
    mandal_name = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    district = relationship("District", back_populates="mandals")
    villages = relationship("Village", back_populates="mandal")

class Village(Base):
    __tablename__ = "villages"
    
    village_id = Column(Integer, primary_key=True, index=True)
    mandal_id = Column(Integer, ForeignKey("mandals.mandal_id"), nullable=False, index=True)
    village_name = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    mandal = relationship("Mandal", back_populates="villages")
    registrations = relationship("Registration", back_populates="village")

class Registration(Base):
    __tablename__ = "registrations"
    
    registration_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    phone_e164 = Column(String(15), nullable=False, unique=True, index=True)
    email = Column(String(120), nullable=True, index=True)
    state_id = Column(Integer, ForeignKey("states.state_id"), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.district_id"), nullable=False)
    mandal_id = Column(Integer, ForeignKey("mandals.mandal_id"), nullable=False)
    village_id = Column(Integer, ForeignKey("villages.village_id"), nullable=False)
    utm_source = Column(String(100), nullable=True)
    utm_medium = Column(String(100), nullable=True)
    utm_campaign = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    village = relationship("Village", back_populates="registrations")
