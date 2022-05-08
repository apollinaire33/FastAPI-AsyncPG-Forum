from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from schemas.user import UserLoginSchema, UserSchema, UserCreateUpdateSchema, Token
from services.user import UserService

user_router = APIRouter()


@user_router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def list(session: AsyncSession = Depends(get_db)):
    return await UserService(session).list()

@user_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get(id: int, session: AsyncSession = Depends(get_db)):
    return await UserService(session).get(id)

@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
async def create(payload: UserCreateUpdateSchema, session: AsyncSession = Depends(get_db)):
    return await UserService(session).create(payload)

@user_router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserSchema)
async def update(id: int, payload: UserCreateUpdateSchema, session: AsyncSession = Depends(get_db)):
    return await UserService(session).update(id, payload)

@user_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete(id: int, session: AsyncSession = Depends(get_db)):
    return await UserService(session).delete(id)

@user_router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def create(payload: UserLoginSchema, session: AsyncSession = Depends(get_db)):
    return await UserService(session).login(payload)

@user_router.post('/validate_token', status_code=status.HTTP_200_OK)
async def create(payload: Token, session: AsyncSession = Depends(get_db)):
    return await UserService(session).validate_token(payload.access_token)