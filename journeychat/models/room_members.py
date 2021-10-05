from sqlalchemy import Column, ForeignKey, Integer

from journeychat.db.base_class import Base


class Room_Members(Base):
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    room_id = Column(Integer, ForeignKey("room.id"), primary_key=True)
