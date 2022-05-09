import datetime
from typing import Dict, Optional, Union

from fastapi import HTTPException, Depends
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import JOSE
from db.database import get_db
from models.user import User
from schemas.user import UserLoginSchema, UserCreateSchema, UserUpdateSchema
from services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(User, db_session)

    async def create(self, payload: UserCreateSchema) -> Optional[User]: 
        # need to optimize into one query with OR statement, maybe move duplicate validation on BaseService create & update level
        # await self.duplicate_exists(self.model.username, payload.username, 'User')
        await self.duplicate_exists(self.model.email, payload.email, 'User')
        return await super().create(payload)

    # won't work when 2 and more unique fields to update
    async def update(self, id: Union[int, str], data: UserUpdateSchema) -> Optional[User]:
        # await self.duplicate_exists(self.model.username, data.username, 'User')
        await self.duplicate_exists(self.model.email, data.email, 'User')
        return await super().update(id, data) 

    async def login(self, data: UserLoginSchema) -> Optional[Dict[str, str]]:
        user = await self.get_by_field(User.email == data.email)
        if not user.active:
            raise HTTPException(status_code=403, detail="User not active!")

        if user.verify_password(data.password):
            token = jwt.encode(
                {
                    'exp': datetime.datetime.utcnow() + JOSE['ACCESS_TOKEN_LIFETIME'], 
                    'iat': datetime.datetime.utcnow(),
                    'scope': user.role.value,
                    'email': user.email,
                },
                JOSE['SECRET_KEY'], 
                algorithm=JOSE['ALGORITHM']
            )
            return {'access_token': token}
        raise HTTPException(status_code=403, detail="Wrong password!")


def get_user_service(
        session: AsyncSession = Depends(get_db),
) -> UserService:
    return UserService(session)
