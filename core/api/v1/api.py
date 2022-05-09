from fastapi import APIRouter

from api.v1.endpoints.category import category_router
from api.v1.endpoints.post import post_router
from api.v1.endpoints.user import user_router

api_router = APIRouter()
api_router.include_router(category_router, prefix='/category', tags=['Post Categories'])
api_router.include_router(post_router, prefix='/post', tags=['Posts'])
api_router.include_router(user_router, prefix='/user', tags=['Users'])
