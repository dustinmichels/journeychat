from typing import Optional

from datetime import datetime
from pydantic import BaseModel


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
