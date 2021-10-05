from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base

# leave in - for import order
from journeychat.models import joined_rooms


class Room(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    is_private = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("user.id"), default=1)
    owner = relationship("User", back_populates="owned_rooms")
    # TODO: rename as members
    joined_users = relationship(
        "User", secondary="joined_rooms", back_populates="joined_rooms"
    )
