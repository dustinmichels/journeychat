from typing import Generator, Optional

from fastapi import Cookie, Depends, HTTPException, Query, WebSocket, status
from jose import JWTError, jwt
from journeychat import crud, schemas
from journeychat.core.auth import oauth2_scheme
from journeychat.core.config import settings
from journeychat.db.session import SessionLocal
from journeychat.models.user import User
from pydantic import BaseModel
from sqlalchemy.orm.session import Session


# class TokenData(BaseModel):
#     username: Optional[str] = None


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        token_data = schemas.TokenPayload(**payload)
    except JWTError:
        raise credentials_exception
    user = crud.user.get(db, id=token_data.sub)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_room_authenticated(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    *,
    room_id: int,
):
    """
    Return room with given ID
        if: room is public or user is a member
        else: raise http error
    """
    room = crud.room.get(db=db, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")
    if room.is_private and current_user not in room.members:
        raise HTTPException(
            status_code=404,
            detail=f"Room with ID {room_id} not found, or you don't have permission to view",
        )
    return room


# --- Websocket Stuff ----


async def ws_get_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return token


async def ws_get_current_user(
    websocket: WebSocket,
    db: Session = Depends(get_db),
    token: str = Depends(ws_get_token),
) -> User:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        token_data = schemas.TokenPayload(**payload)
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    user = crud.user.get(db, id=token_data.sub)
    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return user
