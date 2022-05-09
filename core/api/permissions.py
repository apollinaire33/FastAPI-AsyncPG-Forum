from typing import List, Callable, TypeVar, Type, Union, TypedDict

from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_current_user
from services.base import ModelType
from services.enums import RolesEnum
from db.database import get_db
from models.user import User

SelfBasePermission = TypeVar('SelfBasePermission', bound='BasePermission')


class PermissionParams(TypedDict):
    id: Union[int, str, None]
    current_user: User
    session: AsyncSession


class BasePermission:
    def __init__(self, scope: List[str] = ['any'], additional_model: Type[ModelType] = None) -> None:
        self.scope = scope
        self.additional_model = additional_model
        self.error = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not enough permissions!',
            headers={'WWW-Authenticate': f'Bearer scope="{self.scope}"'}
        )

    def __call__(
        self, 
        id: Union[str, int, None] = None,
        current_user: User = Depends(get_current_user), 
        session: AsyncSession = Depends(get_db)
    ) -> Callable[[Type[SelfBasePermission], PermissionParams], None]:
        return self.validate_permission(id=id, current_user=current_user, session=session)

    def validate_permission(self, **kwargs: PermissionParams):
        pass


class UserPermission(BasePermission):
    def __init__(self, scope: List[str] = ['user'], additional_model: Type[ModelType] = None) -> None:
        super().__init__(scope, additional_model)

    def validate_permission(self, **kwargs: PermissionParams):
        current_user: User = kwargs['current_user']
        if current_user.role.value != RolesEnum.USER.value:
            raise self.error


class AdminPermission(BasePermission):
    def __init__(self, scope: List[str] = ['admin'], additional_model: Type[ModelType] = None) -> None:
        super().__init__(scope, additional_model)

    def validate_permission(self, **kwargs: PermissionParams):
        current_user: User = kwargs['current_user']
        if current_user.role.value != RolesEnum.ADMIN.value:
            raise self.error


class UserAdminPermission(BasePermission):
    def __init__(self, scope: List[str] = ['user', 'admin'], additional_model: Type[ModelType] = None) -> None:
        super().__init__(scope, additional_model)

    def validate_permission(self, **kwargs: PermissionParams):
        current_user: User = kwargs['current_user']
        if current_user.role.value not in (RolesEnum.USER.value, RolesEnum.ADMIN.value):
            raise self.error


class UserOwnerPermission(BasePermission):
    def __init__(self, scope: List[str] = ['user_owner'], additional_model: Type[ModelType] = None) -> None:
        super().__init__(scope, additional_model)

    def validate_permission(self, **kwargs: PermissionParams):
        current_user: User = kwargs['current_user']
        if str(current_user.id) != kwargs['id']:
            raise self.error
