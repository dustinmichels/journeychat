from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from journeychat import crud
from journeychat.crud.base import CRUDBase
from journeychat.models.room import Room
from journeychat.models.user import User
from journeychat.schemas.room import RoomCreate, RoomUpdate


class CRUDRoom(CRUDBase[Room, RoomCreate, RoomUpdate]):
    def get_multi_if_public(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Room]:
        """Returns a list of all public (non-private) rooms"""
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
        """Create new room, assigning creator as owner and adding them as a member."""

        def _create_room_with_owner() -> Room:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data, owner_id=owner_id)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj

        db_obj = _create_room_with_owner()
        owner = crud.user.get(db=db, id=owner_id)
        return self.add_member(db=db, room=db_obj, user=owner)

    def add_member(self, db: Session, *, room: Room, user: User) -> Room:
        """Add member to room."""
        members = [x for x in room.members]
        members.append(user)
        return self.update(db=db, db_obj=room, obj_in={"members": members})

    def remove_member(self, db: Session, *, room: Room, user: User) -> Room:
        """Remove member from room."""
        members = [x for x in room.members if x.id != user.id]
        return self.update(db=db, db_obj=room, obj_in={"members": members})

    def get_members(self, *, room: Room) -> List[User]:
        """Return list of members of a room"""
        return room.members


room = CRUDRoom(Room)
