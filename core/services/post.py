from typing import Optional, Union, Coroutine

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from models.post import PostCategory
from schemas.post import PostCategoryCreateUpdateSchema
from services.base import BaseService


class PostCategoryService(
    BaseService[PostCategory, PostCategoryCreateUpdateSchema, PostCategoryCreateUpdateSchema]
):
    def __init__(self, db_session: AsyncSession):
        super().__init__(PostCategory, db_session)

    async def category_exists(self, data: PostCategoryCreateUpdateSchema) -> None:
        category: ChunkedIteratorResult = await self.db_session.execute(select(PostCategory.title).filter_by(title=data.title))
        if category.scalar():
            raise HTTPException(status_code=404, detail=f"Category {data.title} already exists!")

    async def create(self, data: PostCategoryCreateUpdateSchema) -> Optional[PostCategory]:
        await self.category_exists(data)
        return await super().create(data) 

    async def update(self, id: Union[int, str], data: PostCategoryCreateUpdateSchema) -> Optional[PostCategory]:
        await self.category_exists(data)
        return await super().update(id, data) 

