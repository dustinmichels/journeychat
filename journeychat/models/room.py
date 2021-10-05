from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base
from journeychat.models import room_members  # noqa: F401


class Room(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    is_private = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("user.id"), default=1)
    owner = relationship("User", back_populates="owned_rooms")
    members = relationship(
        "User", secondary="room_members", back_populates="joined_rooms"
    )
