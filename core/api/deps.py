from typing import Dict, Union, Optional

from fastapi import HTTPException, status, Security, Depends
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import JOSE
from db.database import get_db
from models.user import User

oauth_scheme = HTTPBearer()


async def verify_jwt_scopes(
    security_scopes: SecurityScopes,
    token: HTTPAuthorizationCredentials = Security(oauth_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value}
    )

    try:
        payload: Dict[str, Union[int, str]] = jwt.decode(token.credentials, JOSE['SECRET_KEY'], algorithms=JOSE['ALGORITHM'])
    except JWTError:
        raise credentials_exception

    scope = payload.get('scope', None)
    if not scope:
        raise credentials_exception

    if scope not in security_scopes.scopes:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not enough permissions!',
            headers={'WWW-Authenticate': authenticate_value}
        )


async def get_current_user(
    token: HTTPAuthorizationCredentials = Security(oauth_scheme), 
    session: AsyncSession = Depends(get_db)
) -> Optional[User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: Dict[str, Union[int, str]] = jwt.decode(token.credentials, JOSE['SECRET_KEY'], algorithms=JOSE['ALGORITHM'])
    except JWTError:
        raise credentials_exception

    email = payload.get('email', None)
    if not email:
        raise credentials_exception

    res: ChunkedIteratorResult = await session.execute(select(User).where(User.email == email))
    user: User = res.scalar()
    return user
