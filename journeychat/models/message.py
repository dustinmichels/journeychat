from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")
    room_id = Column(Integer, ForeignKey("room.id"))
    timestamp = Column(DateTime)
    text = Column(String)
