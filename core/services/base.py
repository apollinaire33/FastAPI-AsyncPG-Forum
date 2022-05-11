from typing import Generic, List, Optional, TypeVar, Union

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, Column, or_
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.elements import BinaryExpression

from db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class BaseService(Generic[ModelType]):
    def __init__(self, model: ModelType, model_pk: Column, db_session: AsyncSession):
        self._model = model
        self._model_name = model.__name__
        self._model_pk = model_pk
        self._constraints = [constraint.columns.keys()[0] for constraint in model.__table__.constraints]
        self._db_session = db_session

    async def duplicate_exists(self, model_field: Column, payload_value: Union[int, str]) -> None:
        """BaseService method for duplicate validation.

        Mainly for cases, where we need to validate single field with detailed error.
        """
        model_field_name: str = getattr(model_field, 'name')
        duplicate: ChunkedIteratorResult = await self._db_session.execute(select(model_field).filter(model_field == payload_value))
        if duplicate.scalar():
            raise HTTPException(status_code=400, detail=f"{self._model_name} with {model_field_name} {payload_value} already exists!")


    async def duplicate_exists_list(self, data: SchemaType) -> None:
        """BaseService method for duplicate validation.

        Mainly for cases, where we need to validate list of fields within single query.
        Does not have detailed error.
        """
        constraint_column_list: List[Column] = []
        advanced_condition: List[BinaryExpression] = []

        for field in data.dict().keys():
            if field in self._constraints: 
                column = getattr(self._model, field)
                value = getattr(data, field)

                constraint_column_list.append(column)
                advanced_condition.append(column == value)

        duplicate: ChunkedIteratorResult = await self._db_session.execute(select(*constraint_column_list).filter(or_(*advanced_condition)))
        if duplicate.scalars().all():
            raise HTTPException(status_code=400, detail=f"{self._model_name} with provided values already exists!")

    async def get(self, value: Union[int, str], column: Optional[Column] = None) -> Optional[ModelType]:
        if column is None:
            column = self._model_pk

        if column.key not in self._constraints:
            raise Exception('Specified field is not unique constraint!')

        stmt: Select = select(self._model).where(column == value)
        res: ChunkedIteratorResult = await self._db_session.execute(stmt)
        db_obj: Optional[ModelType] = res.scalar()
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return db_obj

    async def list(self, sub_stmt: Union[BinaryExpression, bool] = True) -> List[ModelType]:
        stmt: Select = select(self._model).where(sub_stmt)
        res: ChunkedIteratorResult = await self._db_session.execute(stmt)
        return res.scalars().all()

    async def create(self, data: SchemaType) -> ModelType:
        for field, value in data.dict().items():
            if field in self._constraints:
                column = getattr(self._model, field)
                await self.duplicate_exists(column, value)
        
        db_obj = self._model(**data.dict())
        self._db_session.add(db_obj)
        # For Pydantic: .flush() adds values to db_obj, that generates on DB side e.g. Primary Keys or server_default values
        await self._db_session.flush()
        return db_obj

    async def update(self, id: Union[int, str], data: SchemaType) -> ModelType:
        db_obj = await self.get(id)
        for field, value in data.dict(exclude_unset=True).items():
            if getattr(db_obj, field) == value:
                continue

            if field in self._constraints:
                column = getattr(self._model, field)
                await self.duplicate_exists(column, value)

            setattr(db_obj, field, value)
        return db_obj

    async def delete(self, id: Union[int, str]) -> None:
        db_obj = await self.get(id)
        await self._db_session.delete(db_obj)
