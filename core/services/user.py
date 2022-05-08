import datetime
from typing import Optional, Union, Coroutine

from fastapi import HTTPException
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import JOSE
from models.user import User
from schemas.user import UserLoginSchema, UserCreateUpdateSchema
from services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(User, db_session)

    async def create(self, data: UserCreateUpdateSchema) -> Optional[User]: 
        # need to optimize into one query with OR statement, maybe move duplicate validation on BaseService create & update level
        await self.duplicate_exists(self.model.username, data.username, 'User')
        await self.duplicate_exists(self.model.email, data.email, 'User')
        return await super().create(data)

    async def update(self, id: Union[int, str], data: UserCreateUpdateSchema) -> Optional[User]:
        await self.duplicate_exists(self.model.username, data.username, 'User')
        await self.duplicate_exists(self.model.email, data.email, 'User')
        return await super().update(id, data) 

    async def login(self, data: UserLoginSchema) -> str:
        user = await self.get_by_field(User.email == data.email)
        if user.verify_password(data.password):
            token = jwt.encode(
                {
                    'exp': datetime.datetime.utcnow() + JOSE['ACCESS_TOKEN_LIFETIME'], 
                    'iat': datetime.datetime.utcnow(),
                    'email': user.email, 
                }, 
                JOSE['SECRET_KEY'], 
                algorithm=JOSE['ALGORITHM']
            )
            return {'access_token': token}
        raise HTTPException(status_code=403, detail="Wrong password!")

    async def validate_token(self, token: str) -> str:
        res = jwt.decode(
            token, JOSE['SECRET_KEY'], algorithms=JOSE['ALGORITHM']
        )
        return res
