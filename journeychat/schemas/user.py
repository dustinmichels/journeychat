from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl


class UserBase(BaseModel):
    username: Optional[str]
    display_name: Optional[str]
    email: Optional[EmailStr] = None
    avatar = HttpUrl
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    ...


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    hashed_password: str


# Additional properties to return via API
class User(UserInDBBase):
    ...
