from typing import List

from fastapi import Depends, status, Response, APIRouter
from fastapi_utils.cbv import cbv

from api.permissions import AdminPermission, UserAdminPermission, UserOwnerPermission
from schemas.user import UserLoginSchema, UserSchema, UserCreateSchema, UserUpdateSchema, Token
from services.user import UserService, get_user_service

user_router = APIRouter()


@cbv(user_router)
class UserRouter:
    service: UserService = Depends(get_user_service)
    permissions = {
        'list': UserAdminPermission(),
        'retrieve': UserAdminPermission(),
        'put': UserOwnerPermission(),
        'delete': AdminPermission(),
    }

    @user_router.get(path='/', status_code=status.HTTP_200_OK, response_model=List[UserSchema], dependencies=[Depends(permissions['list'])])
    async def list(self):
        return await self.service.list()

    @user_router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserSchema, dependencies=[Depends(permissions['retrieve'])])
    async def retrieve(self, id: int):
        return await self.service.get(id)

    @user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchema)
    async def create(self, payload: UserCreateSchema):
        return await self.service.create(payload)

    @user_router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserSchema, dependencies=[Depends(permissions['put'])])
    async def update(self, id: int, payload: UserUpdateSchema):
        return await self.service.update(id, payload)

    @user_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response, dependencies=[Depends(permissions['delete'])])
    async def delete(self, id: int):
        return await self.service.delete(id)

    @user_router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
    async def login(self, payload: UserLoginSchema):
        return await self.service.login(payload)
