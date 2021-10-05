from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base

from journeychat.models import room_members  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    email = Column(String, index=True, nullable=False)
    avatar = Column(String(256), nullable=True)
    is_superuser = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    owned_rooms = relationship("Room", back_populates="owner")
    joined_rooms = relationship(
        "Room", secondary="room_members", back_populates="members"
    )
