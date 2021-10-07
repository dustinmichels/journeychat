# from typing import Generator, Optional

# from fastapi import Depends, HTTPException, Query, WebSocket, status
# from jose import JWTError, jwt
# from sqlalchemy.orm.session import Session

# from journeychat import crud, models, schemas
# from journeychat.core.auth import oauth2_scheme
# from journeychat.core.config import settings
# from journeychat.db.session import SessionLocal
# from journeychat.models.room import Room
# from journeychat.models.user import User


# async def ws_get_token(
#     websocket: WebSocket,
#     token: Optional[str] = Query(None),
# ):
#     if token is None:
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#     return token


# async def ws_get_current_user(
#     websocket: WebSocket,
#     db: Session = Depends(get_db),
#     token: str = Depends(ws_get_token),
# ) -> User:
#     try:
#         payload = jwt.decode(
#             token,
#             settings.JWT_SECRET,
#             algorithms=[settings.ALGORITHM],
#             options={"verify_aud": False},
#         )
#         token_data = schemas.TokenPayload(**payload)
#     except JWTError:
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#     user = crud.user.get(db, id=token_data.sub)
#     if user is None:
#         await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
#     return user
