from typing import Any

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from journeychat import crud, deps
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
def fetch_user(*, user_id: int, db: Session = Depends(deps.get_db)) -> Any:
    """
    Fetch a single recipe by ID
    """
    # result = [user for user in USERS if user["id"] == user_id]
    result = crud.user.get(db=db, id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return result


app.include_router(api_router)


# if __name__ == "__main__":
#     # Use this for debugging purposes only
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
