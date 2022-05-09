from typing import List

from fastapi import APIRouter, Depends, status, Response
from fastapi_utils.cbv import cbv

from schemas.post import PostCategoryCreateUpdateSchema, PostCategorySchema
from services.post import PostCategoryService, get_category_service

category_router = APIRouter()


@cbv(category_router)
class CategoryRouter:
    service: PostCategoryService = Depends(get_category_service)
    
    @category_router.get('/', status_code=status.HTTP_200_OK, response_model=List[PostCategorySchema])
    async def list(self):
        return await self.service.list()

    @category_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PostCategorySchema)
    async def get(self, id: int):
        return await self.service.get(id)

    @category_router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostCategorySchema)
    async def create(self, payload: PostCategoryCreateUpdateSchema):
        return await self.service.create(payload)

    @category_router.put('/{id}', status_code=status.HTTP_200_OK, response_model=PostCategorySchema)
    async def update(self, id: int, payload: PostCategoryCreateUpdateSchema):
        return await self.service.update(id, payload)

    # response_class=Response, as FastAPI uses JSONResponse by default and converts None to "null" and leading to error
    # because every 204 response should return empty body by status code convention
    @category_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
    async def delete(self, id: int):
        return await self.service.delete(id)
