from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base


class Room(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    is_private = Column(Boolean, default=False)
    users = relationship("User", secondary="user_rooms", back_populates="rooms")
