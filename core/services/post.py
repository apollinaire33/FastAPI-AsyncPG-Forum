from typing import Optional, Union, Coroutine

from fastapi import HTTPException
from sqlalchemy import select, Column
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from models.post import Post, PostCategory
from schemas.post import PostCreateUpdateSchema, PostCategoryCreateUpdateSchema
from services.base import BaseService


class PostCategoryService(BaseService[PostCategory]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(PostCategory, db_session)

    async def create(self, data: PostCategoryCreateUpdateSchema) -> Optional[PostCategory]:
        await self.duplicate_exists(self.model.title, data.title, 'Category')
        return await super().create(data)

    async def update(self, id: Union[int, str], data: PostCategoryCreateUpdateSchema) -> Optional[PostCategory]:
        await self.duplicate_exists(self.model.title, data.title, 'Category')
        return await super().update(id, data) 


class PostService(BaseService[PostCategory]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(Post, db_session)

    async def list_validated(self):
        return await super().list(Post.validated == True)
    
    async def list_unvalidated(self):
        return await super().list(Post.validated == False)
