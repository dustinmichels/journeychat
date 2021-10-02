from fastapi import APIRouter

from journeychat.api.api_v1.endpoints import auth, room


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(room.router, prefix="/rooms", tags=["rooms"])
