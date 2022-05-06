from typing import Any, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select

from db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def get(self, id: Union[int, str]) -> Optional[ModelType]:
        stmt: Select = select(self.model).where(self.model.id == id)
        res: ChunkedIteratorResult = await self.db_session.execute(stmt)
        db_obj: Optional[ModelType] = res.scalar()
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return db_obj

    async def list(self) -> List[ModelType]:
        stmt: Select = select(self.model)
        res: ChunkedIteratorResult = await self.db_session.execute(stmt)
        return res.scalars().all()

    async def create(self, data: CreateSchemaType) -> ModelType:
        db_obj = self.model(**data.dict())
        self.db_session.add(db_obj)
        # For Pydantic: .flush() adds values to db_obj, that generates on DB side
        await self.db_session.flush()
        return db_obj

    async def update(self, id: Union[int, str], data: UpdateSchemaType) -> ModelType:
        db_obj = await self.get(id)
        for column, value in data.dict(exclude_unset=True).items():
            setattr(db_obj, column, value)
        return db_obj

    async def delete(self, id: Union[int, str]) -> None:
        db_obj = await self.get(id)
        await self.db_session.delete(db_obj)
