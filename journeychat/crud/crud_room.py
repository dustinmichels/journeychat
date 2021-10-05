from typing import List
from journeychat.crud.base import CRUDBase
from journeychat.models.room import Room
from journeychat.models.user import User
from journeychat.schemas.room import RoomCreate, RoomUpdate

from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session


class CRUDRoom(CRUDBase[Room, RoomCreate, RoomUpdate]):
    def get_multi_if_public(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Room]:
        return (
            db.query(self.model)
            .filter(Room.is_private == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: RoomCreate, owner_id: int
    ) -> Room:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_member(self, db: Session, *, user_id: int) -> Room:
        ...


room = CRUDRoom(Room)
