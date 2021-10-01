from datetime import datetime

from pydantic import BaseModel, HttpUrl

# from typing import Sequence


class User(BaseModel):
    id: int
    username: str
    display_name: str


class ChatRoom(BaseModel):
    id: int


class ChatMessage(BaseModel):
    id: int
    chat_room_id: int
    user_id: int
    message: str
    timestamp: datetime
