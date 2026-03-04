from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class AddressBase(BaseModel):
    street: str
    city: str
    state: Optional[str] = None
    country: str
    postal_code: Optional[str] = None


class AddressCreate(AddressBase):
    # All fields from AddressBase are required, except optionals.
    # No additional fields needed.
    pass


class AddressUpdate(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None


class AddressInDB(AddressBase):
    id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class AddressNearby(AddressInDB):
    distance_km: float