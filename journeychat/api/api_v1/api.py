from fastapi import APIRouter

from journeychat.api.api_v1.endpoints import auth, room, chat, message, action, member


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(room.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(member.router, prefix="/members", tags=["members"])
api_router.include_router(message.router, prefix="/messages", tags=["messages"])
api_router.include_router(action.router, prefix="/actions", tags=["actions"])
api_router.include_router(chat.router)
