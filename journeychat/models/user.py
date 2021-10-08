from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base
from journeychat.models import room_members  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    username = Column(String, nullable=True)
    is_superuser = Column(Boolean, default=False)
    display_name = Column(String, nullable=True)
    avatar = Column(String(256), nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime)
    owned_rooms = relationship("Room", back_populates="owner")
    joined_rooms = relationship(
        "Room", secondary="room_members", back_populates="members"
    )
