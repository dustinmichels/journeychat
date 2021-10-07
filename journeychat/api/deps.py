from typing import Generator, Optional

from fastapi import Depends, HTTPException, Query, WebSocket, status
from jose import JWTError, jwt
from sqlalchemy.orm.session import Session

from journeychat import crud, models, schemas
from journeychat.core.auth import oauth2_scheme
from journeychat.core.config import settings
from journeychat.db.session import SessionLocal
from journeychat.models.room import Room
from journeychat.models.user import User


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


def get_room_if_member(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    room_id: int,
) -> Room:
    """
    Return room with given ID, if user is member or room is public.
    Otherwise, raise http error.
    """
    room = crud.room.get(db=db, id=room_id)
    if not room:
        raise HTTPException(status_code=404, detail=f"Room with ID {room_id} not found")
    if room.is_private and current_user not in room.members:
        raise HTTPException(
            status_code=400,
            detail=f"You do not have permission to access {room_id}",
        )
    return room


def get_room_if_owner(
    current_user: models.User = Depends(get_current_user),
    room: models.Room = Depends(get_room_if_member),
) -> Room:
    """
    Return room if owner, otherwise return http error
    """
    if not crud.user.is_superuser(current_user) and (room.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
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


async def ws_test(
    db: Session = Depends(get_db),
    token: Optional[str] = Query(None),
) -> User:
    print("INSIDE WS TEST!!")
    print(token)
    return ""
    # try:
    #     payload = jwt.decode(
    #         token,
    #         settings.JWT_SECRET,
    #         algorithms=[settings.ALGORITHM],
    #         options={"verify_aud": False},
    #     )
    #     token_data = schemas.TokenPayload(**payload)
    # except JWTError:
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    # user = crud.user.get(db, id=token_data.sub)
    # if user is None:
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    # return user
