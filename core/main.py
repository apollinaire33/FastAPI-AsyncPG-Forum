from fastapi import FastAPI

from api.v1.api import api_router
from core.config import API_V1_PREFIX

app = FastAPI(
    title='Forum Async API',
    description='Fully asynchronous RESTful API for Forum Application',
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
)

app.include_router(api_router, prefix=API_V1_PREFIX)
