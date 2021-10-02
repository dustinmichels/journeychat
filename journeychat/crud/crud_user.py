from typing import Any, Dict, Optional, Union

from journeychat import models, schemas
from journeychat.core.security import get_password_hash
from journeychat.crud.base import CRUDBase
from journeychat.models import User
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> User:
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)

        # add avatar
        if not db_obj.avatar:
            seed = db_obj.username
            db_obj.avatar = f"https://picsum.photos/seed/{seed}/200/"

        db.add(db_obj)
        db.commit()

        return db_obj

    # def update(
    #     self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    # ) -> User:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)

    #     return super().update(db, db_obj=db_obj, obj_in=update_data)

    # def is_superuser(self, user: User) -> bool:
    #     return user.is_superuser


user = CRUDUser(User)
