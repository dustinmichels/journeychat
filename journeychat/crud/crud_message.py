from journeychat.crud.base import CRUDBase
from journeychat.models.message import Message
from journeychat.schemas.message import MessageCreate, MessageUpdate
from datetime import datetime
from sqlalchemy.orm import Session


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def create(self, db: Session, *, obj_in: MessageCreate) -> Message:
        create_data = obj_in.dict()
        # ensure timestamp has datetime format
        # create_data["timestamp"] = datetime.fromisoformat(create_data["timestamp"])
        db_obj = Message(**create_data)

        db.add(db_obj)
        db.commit()

        return db_obj


message = CRUDMessage(Message)
