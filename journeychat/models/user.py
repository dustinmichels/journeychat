from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base

# leave in - for import order
from journeychat.models import joined_rooms


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    email = Column(String, index=True, nullable=False)
    avatar = Column(String(256), nullable=True)
    is_superuser = Column(Boolean, default=False)
    hashed_password = Column(String, nullable=False)
    joined_rooms = relationship(
        "Room", secondary="joined_rooms", back_populates="joined_users"
    )

    class Config:
        orm_mode = True
