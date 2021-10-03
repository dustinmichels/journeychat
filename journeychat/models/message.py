from sqlalchemy import Integer, String, Column, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    room_id = Column(Integer, ForeignKey("room.id"), primary_key=True)
    timestamp = Column(DateTime)
    text = Column(String)
