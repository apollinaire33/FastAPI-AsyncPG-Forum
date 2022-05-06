from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from schemas.post import PostCategoryCreateUpdateSchema, PostCategorySchema
from services.post import PostCategoryService

category_router = APIRouter()


@category_router.get('/', status_code=status.HTTP_200_OK, response_model=List[PostCategorySchema])
async def list(session: AsyncSession = Depends(get_db)):
    return await PostCategoryService(session).list()

@category_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PostCategorySchema)
async def get(id: int, session: AsyncSession = Depends(get_db)):
    return await PostCategoryService(session).get(id)

@category_router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostCategorySchema)
async def create(payload: PostCategoryCreateUpdateSchema, session: AsyncSession = Depends(get_db)):
    return await PostCategoryService(session).create(payload)

@category_router.put('/{id}', status_code=status.HTTP_200_OK, response_model=PostCategorySchema)
async def update(id: int, payload: PostCategoryCreateUpdateSchema, session: AsyncSession = Depends(get_db)):
    return await PostCategoryService(session).update(id, payload)

# response_class=Response, as FastAPI uses JSONResponse by default and converts None to "null" and leading to error
# because every 204 response should return empty body by status code convention
@category_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete(id: int, session: AsyncSession = Depends(get_db)):
    return await PostCategoryService(session).delete(id)
