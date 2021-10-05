from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

from journeychat.crud.base import CRUDBase
from journeychat.models.message import Message
from journeychat.schemas.message import MessageCreate, MessageUpdate


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def create(self, db: Session, *, obj_in: MessageCreate) -> Message:
        """Override create function to omit json encoder step"""
        create_data = obj_in.dict()
        db_obj = Message(**create_data)
        db.add(db_obj)
        db.commit()
        return db_obj

    def get_multi_by_room(
        self, db: Session, *, room_id: int, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """
        Get messages for a given room.
        Messages are sorted in descending order, so that `limit` applies to n most recent messages
        But returned in ascending order.
        """
        res = (
            db.query(self.model)
            .filter(Message.room_id == room_id)
            .order_by(Message.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        res.reverse()
        return res


message = CRUDMessage(Message)
