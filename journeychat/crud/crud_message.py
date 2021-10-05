from typing import List
from journeychat.crud.base import CRUDBase
from journeychat.models.message import Message
from journeychat.schemas.message import MessageCreate, MessageUpdate
from datetime import datetime
from sqlalchemy.orm import Session


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def create(self, db: Session, *, obj_in: MessageCreate) -> Message:
        create_data = obj_in.dict()
        # if isinstance(create_data["timestamp"], str):
        #     print("Converting timestamp to datetime object")
        #     create_data["timestamp"] = datetime(create_data["timestamp"])
        db_obj = Message(**create_data)
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



    def get_multi_by_room(
        self, db: Session, *, room_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        return (
            db.query(self.model)
            .filter(Message.room_id == room_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


message = CRUDMessage(Message)
