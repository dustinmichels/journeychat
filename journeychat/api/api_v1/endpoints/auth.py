from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from journeychat import crud, schemas
from journeychat.api import deps
from journeychat.core.auth import authenticate, create_access_token
from journeychat.models import User
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.post("/signup", response_model=schemas.User, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    # check if email already exists
    if crud.user.get_by_email(db=db, email=user_in.email):
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists in the system",
        )
    # check if username already exists
    if crud.user.get_by_username(db=db, username=user_in.username):
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists in the system",
        )
    return crud.user.create(db=db, obj_in=user_in)


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """
    return current_user
