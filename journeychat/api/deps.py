from typing import Generator, Optional

from fastapi import Cookie, Depends, HTTPException, Query, WebSocket, status
from jose import JWTError, jwt
from journeychat.core.auth import oauth2_scheme
from journeychat.core.config import settings
from journeychat.db.session import SessionLocal
from journeychat.models.user import User
from pydantic import BaseModel
from sqlalchemy.orm.session import Session


class TokenData(BaseModel):
    username: Optional[str] = None


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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


async def get_current_user_ws(
    db: Session = Depends(get_db), token: str = Depends(get_cookie_or_token)
) -> User:
    # TODO: Better error handling
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
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
