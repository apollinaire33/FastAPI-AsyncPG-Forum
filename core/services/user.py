import datetime
from typing import Dict, Optional

from fastapi import HTTPException, Depends
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import JOSE
from db.database import get_db
from models.user import User
from schemas.user import UserLoginSchema
from services.base import BaseService


class UserService(BaseService[User]):
    def __init__(self, db_session: AsyncSession):
        super().__init__(User, User.id, db_session)

    async def login(self, data: UserLoginSchema) -> Optional[Dict[str, str]]:
        user = await self.get(data.email, User.email)
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
