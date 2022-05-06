from fastapi import APIRouter

from api.v1.endpoints.category import category_router

api_router = APIRouter()
api_router.include_router(category_router, prefix='/category', tags=['Post Categories'])