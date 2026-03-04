from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import dependencies
from app.services.address_service import AddressService
from app.schemas.address import AddressCreate, AddressUpdate, AddressInDB, AddressNearby

router = APIRouter()

@router.post("/", response_model=AddressInDB, status_code=status.HTTP_201_CREATED)
def create_address(
        address: AddressCreate,
        db: Session = Depends(dependencies.get_db)
):
    """Create a new address with geocoded coordinates."""
    db_address = AddressService.create_address(db, address)
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create address. Geocoding may have failed."
        )
    return db_address

@router.get("/{address_id}", response_model=AddressInDB)
def read_address(
        address_id: int,
        db: Session = Depends(dependencies.get_db)
):
    """Get address by ID."""
    db_address = AddressService.get_address(db, address_id)
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    return db_address

@router.put("/{address_id}", response_model=AddressInDB)
def update_address(
        address_id: int,
        address: AddressUpdate,
        db: Session = Depends(dependencies.get_db)
):
    """Update an existing address. If address components change, coordinates are re-geocoded."""
    db_address = AddressService.update_address(db, address_id, address)
    if not db_address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    return db_address

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
        address_id: int,
        db: Session = Depends(dependencies.get_db)
):
    """Delete an address."""
    deleted = AddressService.delete_address(db, address_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    return None

@router.get("/nearby/", response_model=List[AddressNearby])
def find_nearby_addresses(
        latitude: float,
        longitude: float,
        distance_km: float,
        db: Session = Depends(dependencies.get_db)
):
    """Find addresses within a given distance (km) from specified coordinates."""
    if distance_km <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Distance must be positive"
        )
    addresses = AddressService.get_addresses_within_distance(db, latitude, longitude, distance_km)
    return addresses