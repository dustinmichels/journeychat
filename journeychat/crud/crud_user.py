from typing import List, Optional

from sqlalchemy.orm import Session

from journeychat import crud, schemas
from journeychat.core.security import get_password_hash
from journeychat.crud.base import CRUDBase
from journeychat.models import User


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_joined_rooms(self, *, user: User) -> List[schemas.Room]:
        return user.joined_rooms

    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> User:
        def _create_user():
            create_data = obj_in.dict()
            create_data.pop("password")
            db_obj = User(**create_data)
            db_obj.hashed_password = get_password_hash(obj_in.password)
            db.add(db_obj)
            db.commit()
            return db_obj

        new_user = _create_user()

        # add to first room
        first_room = crud.room.get(db, 1)
        if first_room and new_user not in first_room.members:
            crud.room.add_member(db, room=first_room, user=new_user)

        return new_user

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
