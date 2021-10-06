from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, validator

from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = None
    username: str = None
    avatar: Optional[HttpUrl] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    is_superuser: bool = False
    password: str
    avatar: Optional[HttpUrl] = None
    created_at: datetime = datetime.now()

    @validator("avatar", pre=True, always=True)
    def set_default_avatar(cls, v, *, values):  # pylint: disable=no-self-argument
        """
        Create default avatar url if none is supplied.
            Use the site picsum to get a random image,
            with username as a random seed.
        """
        seed = values["username"]
        return v or f"https://picsum.photos/seed/{seed}/200/"


# Properties to receive via API on update
class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str
    is_superuser: bool


# Additional properties to return via API
class User(UserInDBBase):
    ...
