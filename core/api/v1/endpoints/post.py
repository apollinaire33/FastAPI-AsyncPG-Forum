from typing import List
from unicodedata import category

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from models.post import Post

from db.database import get_db
from schemas.post import PostSchema, PostCreateUpdateSchema, PostUpdateValidatedSchema
from services.post import PostService

post_router = APIRouter()


@post_router.get('/', status_code=status.HTTP_200_OK, response_model=List[PostSchema])
async def list(session: AsyncSession = Depends(get_db)):
    return await PostService(session).list()

@post_router.get('/validated', status_code=status.HTTP_200_OK, response_model=List[PostSchema])
async def list_validated(session: AsyncSession = Depends(get_db)):
    return await PostService(session).list_validated()

@post_router.get('/unvalidated', status_code=status.HTTP_200_OK, response_model=List[PostSchema])
async def list_unvalidated(session: AsyncSession = Depends(get_db)):
    return await PostService(session).list_unvalidated()

@post_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PostSchema)
async def get(id: int, session: AsyncSession = Depends(get_db)):
    return await PostService(session).get(id)

@post_router.put('/{id}/update_validated', status_code=status.HTTP_200_OK, response_model=PostSchema)
async def update_validated(id: int, payload: PostUpdateValidatedSchema, session: AsyncSession = Depends(get_db)):
    return await PostService(session).update(id, payload)

@post_router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostSchema)
async def create(payload: PostCreateUpdateSchema, session: AsyncSession = Depends(get_db)):
    return await PostService(session).create(payload)

@post_router.put('/{id}', status_code=status.HTTP_200_OK, response_model=PostSchema)
async def update(id: int, payload: PostCreateUpdateSchema, session: AsyncSession = Depends(get_db)):
    return await PostService(session).update(id, payload)

@post_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete(id: int, session: AsyncSession = Depends(get_db)):
    return await PostService(session).delete(id)
