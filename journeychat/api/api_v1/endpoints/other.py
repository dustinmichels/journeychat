# import asyncio
# from typing import Any, Optional

# # import httpx
# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session

# from journeychat import crud
# from journeychat.api import deps
# from journeychat.schemas.recipe import Recipe, RecipeCreate, RecipeSearchResults

# router = APIRouter()


# @router.get("/{test}", status_code=200)
# def fetch_recipe(
#     *,
#     recipe_id: int,
#     db: Session = Depends(deps.get_db),
# ) -> Any:
#     """
#     Fetch a single recipe by ID
#     """
#     result = crud.recipe.get(db=db, id=recipe_id)
#     if not result:
#         # the exception is raised, not returned - you will get a validation
#         # error otherwise.
#         raise HTTPException(
#             status_code=404, detail=f"Recipe with ID {recipe_id} not found"
#         )

#     return result
