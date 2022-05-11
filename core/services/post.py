from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from models.post import Post, PostCategory
from services.base import BaseService


class PostCategoryService(BaseService[PostCategory]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(PostCategory, db_session)


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
