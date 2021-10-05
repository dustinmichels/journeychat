from typing import List
from journeychat.crud.base import CRUDBase
from journeychat.models.room import Room
from journeychat.models.user import User
from journeychat.schemas.room import RoomCreate, RoomUpdate

from journeychat import crud

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
        # create room
        db_obj = self._create_room_with_owner(db=db, obj_in=obj_in, owner_id=owner_id)
        # add owner as member
        owner = crud.user.get(db=db, id=owner_id)
        return self.add_member(db=db, room=db_obj, user=owner)

    def _create_room_with_owner(
        self, db: Session, *, obj_in: RoomCreate, owner_id: int
    ) -> Room:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_member(self, db: Session, *, room: Room, user: User) -> Room:
        members = [x for x in room.members]
        members.append(user)
        return self.update(db=db, db_obj=room, obj_in={"members": members})

    def get_members(self, *, room: Room):
        return room.members


room = CRUDRoom(Room)
