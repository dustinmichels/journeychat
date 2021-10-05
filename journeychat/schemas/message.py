from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from journeychat.schemas.user import User


class MessageBase(BaseModel):
    user_id: int
    room_id: int
    timestamp: datetime
    text: str


class MessageCreate(MessageBase):
    ...


class MessageUpdate(MessageBase):
    ...


class MessageInDBBase(MessageBase):
    id: int

    class Config:
        orm_mode = True


class Message(MessageInDBBase):
    ...


class MessageNested(MessageInDBBase):
    user: User
