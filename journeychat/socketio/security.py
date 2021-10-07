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

from socketio.exceptions import ConnectionRefusedError


from fastapi import Depends
from journeychat.api import deps


async def get_authenticated_user(token):
    db: Session = next(deps.get_db())
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        token_data = schemas.TokenPayload(**payload)
    except JWTError:
        raise ConnectionRefusedError("authentication failed")
    user = crud.user.get(db, id=token_data.sub)
    if user is None:
        raise ConnectionRefusedError("authentication failed")
    return user
