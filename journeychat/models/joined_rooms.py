from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base


class Joined_Rooms(Base):
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    room_id = Column(Integer, ForeignKey("room.id"), primary_key=True)
