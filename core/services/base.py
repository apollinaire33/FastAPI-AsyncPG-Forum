from typing import Any, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, Column
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.expression import ColumnOperators

from db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseService(Generic[ModelType]):
    def __init__(self, model: ModelType, db_session: AsyncSession):
        self.model = model
        self.db_session = db_session

    async def duplicate_exists(self, model_field: Column, payload_value: Union[int, str], model_name: str) -> None:
        model_field_name: str = getattr(model_field, 'name')
        duplicate: ChunkedIteratorResult = await self.db_session.execute(select(model_field).filter(model_field == payload_value))
        if duplicate.scalar():
            raise HTTPException(status_code=400, detail=f"{model_name} with {model_field_name} {payload_value} already exists!")

    async def get(self, id: Union[int, str]) -> Optional[ModelType]:
        stmt: Select = select(self.model).where(self.model.id == id)
        res: ChunkedIteratorResult = await self.db_session.execute(stmt)
        db_obj: Optional[ModelType] = res.scalar()
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return db_obj

    async def get_by_field(self, sub_stmt: Union[ColumnOperators, bool] = True) -> Optional[ModelType]:
        stmt: Select = select(self.model).where(sub_stmt)
        res: ChunkedIteratorResult = await self.db_session.execute(stmt)
        db_obj: Optional[ModelType] = res.scalar()
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return db_obj

    async def list(self, sub_stmt: Union[ColumnOperators, bool] = True) -> List[ModelType]:
        stmt: Select = select(self.model).where(sub_stmt)
        res: ChunkedIteratorResult = await self.db_session.execute(stmt)
        return res.scalars().all()

    async def create(self, data: SchemaType) -> ModelType:
        db_obj = self.model(**data.dict())
        self.db_session.add(db_obj)
        # For Pydantic: .flush() adds values to db_obj, that generates on DB side e.g. Primary Keys or server_default values
        await self.db_session.flush()
        return db_obj

    async def update(self, id: Union[int, str], data: SchemaType) -> ModelType:
        db_obj = await self.get(id)
        for column, value in data.dict(exclude_unset=True).items():
            setattr(db_obj, column, value)
        return db_obj

    async def delete(self, id: Union[int, str]) -> None:
        db_obj = await self.get(id)
        await self.db_session.delete(db_obj)
