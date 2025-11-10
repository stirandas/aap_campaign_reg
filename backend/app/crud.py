from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from . import models

# States
async def get_all_states(db: AsyncSession):
    result = await db.execute(select(models.State).order_by(models.State.state_name))
    return result.scalars().all()

# Districts
async def get_districts_by_state(db: AsyncSession, state_id: int):
    result = await db.execute(
        select(models.District)
        .where(models.District.state_id == state_id)
        .order_by(models.District.district_name)
    )
    return result.scalars().all()

# Mandals
async def get_mandals_by_district(db: AsyncSession, district_id: int):
    result = await db.execute(
        select(models.Mandal)
        .where(models.Mandal.district_id == district_id)
        .order_by(models.Mandal.mandal_name)
    )
    return result.scalars().all()

# Villages
async def get_or_create_village(db: AsyncSession, mandal_id: int, village_name: str):
    # Check if village exists
    result = await db.execute(
        select(models.Village)
        .where(
            models.Village.mandal_id == mandal_id,
            models.Village.village_name == village_name
        )
    )
    village = result.scalar_one_or_none()
    
    if village:
        return village
    
    # Create new village
    village = models.Village(mandal_id=mandal_id, village_name=village_name)
    db.add(village)
    await db.commit()
    await db.refresh(village)
    return village

# Registrations
async def create_registration(db: AsyncSession, registration_data: dict):
    # Check if phone already registered
    result = await db.execute(
        select(models.Registration)
        .where(models.Registration.phone_e164 == registration_data["phone_e164"])
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        return None  # Phone already registered
    
    # Create registration
    registration = models.Registration(**registration_data)
    db.add(registration)
    await db.commit()
    await db.refresh(registration)
    return registration
