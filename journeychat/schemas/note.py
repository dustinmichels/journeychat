from typing import Optional

from datetime import datetime
from pydantic import BaseModel


class NoteBase(BaseModel):
    id: int
    chat_room_id: int
    user_id: int
    message: str
    timestamp: datetime
