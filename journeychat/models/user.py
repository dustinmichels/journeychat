from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from journeychat.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    display_name = Column(String, nullable=True)
    email = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
