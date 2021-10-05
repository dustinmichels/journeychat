from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from journeychat import crud, models, schemas
from journeychat.core.security import get_password_hash
from journeychat.crud.base import CRUDBase
from journeychat.models import User


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> User:
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)

        # <--- INIT DEFAULTS
        # TODO: move this initial logic to Pydantic model??

        # add avatar
        if not db_obj.avatar:
            seed = db_obj.username
            db_obj.avatar = f"https://picsum.photos/seed/{seed}/200/"

        # add to first room
        first_room = crud.room.get(db, 1)
        if first_room and first_room not in db_obj.joined_rooms:
            db_obj.joined_rooms.append(first_room)
        # INIT DEFAULTS --->

        db.add(db_obj)
        db.commit()

        return db_obj

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
