from jose import JWTError, jwt
from socketio.exceptions import ConnectionRefusedError
from sqlalchemy.orm.session import Session

from journeychat import crud, schemas
from journeychat.api import deps
from journeychat.core.config import settings
from journeychat.models.user import User


async def get_authenticated_user(token) -> User:
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
