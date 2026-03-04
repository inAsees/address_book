import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate

logger = logging.getLogger(__name__)


class AddressService:
    @staticmethod
    def create_address(db: Session, address_data: AddressCreate) -> Address:
        db_address = Address(
            latitude=address_data.latitude,
            longitude=address_data.longitude
        )
        try:
            db.add(db_address)
            db.commit()
            db.refresh(db_address)
            logger.info(f"Address created with id {db_address.id}")
            return db_address
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating address: {e}")
            raise

    @staticmethod
    def get_address(db: Session, address_id: int) -> Optional[Address]:
        return db.query(Address).filter(Address.id == address_id).first()

    @staticmethod
    def update_address(db: Session, address_id: int, address_data: AddressUpdate) -> Optional[Address]:
        db_address = AddressService.get_address(db, address_id)
        if not db_address:
            return None

        update_data = address_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_address, field, value)

        try:
            db.commit()
            db.refresh(db_address)
            logger.info(f"Address {address_id} updated")
            return db_address
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating address {address_id}: {e}")
            raise

    @staticmethod
    def delete_address(db: Session, address_id: int) -> bool:
        db_address = AddressService.get_address(db, address_id)
        if not db_address:
            return False

        try:
            db.delete(db_address)
            db.commit()
            logger.info(f"Address {address_id} deleted")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting address {address_id}: {e}")
            raise

    @staticmethod
    def get_addresses_within_distance(db: Session, latitude: float, longitude: float, distance_km: float) -> List[
        Address]:
        addresses = db.query(Address).all()
        result = []
        for addr in addresses:
            dist = geodesic((latitude, longitude), (addr.latitude, addr.longitude)).km
            if dist <= distance_km:
                addr.distance_km = dist  # type: ignore
                result.append(addr)
        logger.info(f"Found {len(result)} addresses within {distance_km}km of ({latitude}, {longitude})")
        return result