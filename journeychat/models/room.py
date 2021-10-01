from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base

from journeychat.models import joined_rooms


class Room(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    is_private = Column(Boolean, default=False)
    joined_users = relationship(
        "User", secondary="joined_rooms", back_populates="joined_rooms"
    )
