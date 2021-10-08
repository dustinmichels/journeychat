from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from journeychat.api.api_v1.api import api_router
from journeychat.core.config import settings
from journeychat.socketio import ws_app

root_router = APIRouter()
app = FastAPI(title="JourneyChat API", openapi_url="/openapi.json")


@root_router.get("/")
def root() -> dict:
    """
    Root GET
    """
    with open("index.html") as f:
        html = f.read()
    return HTMLResponse(html)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# app.include_router(api_router)
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# mount websocket app
app.mount("/ws", ws_app)
