from fastapi import FastAPI, APIRouter, HTTPException

from journeychat.schemas import User
from journeychat.user_data import USERS

app = FastAPI(title="JourneyChat API", openapi_url="/openapi.json")

api_router = APIRouter()


@api_router.get("/")
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


@api_router.get("/user/{user_id}", status_code=200, response_model=User)
def fetch_user(*, user_id: int) -> dict:
    """
    Fetch a single recipe by ID
    """
    result = [user for user in USERS if user["id"] == user_id]
    if not result:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return result[0]


app.include_router(api_router)


# if __name__ == "__main__":
#     # Use this for debugging purposes only
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
