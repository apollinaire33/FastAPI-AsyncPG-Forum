from typing import Optional, Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from models.post import Post, PostCategory
from schemas.post import PostCategoryCreateUpdateSchema
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


def get_category_service(
        session: AsyncSession = Depends(get_db),
) -> PostCategoryService:
    return PostCategoryService(session)
