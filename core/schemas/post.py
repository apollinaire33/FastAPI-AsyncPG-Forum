from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr


class PostCategorySchema(BaseModel):
    id: int
    title: str
    description: str

    # to use .from_orm() for translating from Model to Schema,
    # e.g. PostCategorySchema.from_orm(model_instance) -> id=1 title='foo' description='bar'
    class Config:
        orm_mode = True


class PostCategoryCreateUpdateSchema(BaseModel):
    title: constr(max_length=25)
    description: Optional[str]

    class Config:
        orm_mode = True
        

class PostSchema(BaseModel):
    id: int
    title: str
    text: str
    time_created: datetime
    time_updated: Optional[datetime]
    category: str
    validated: bool

    class Config:
        orm_mode = True


class PostCreateUpdateSchema(BaseModel):
    title: str
    text: str
    category: str

    class Config:
        orm_mode = True


class PostUpdateValidatedSchema(BaseModel):
    validated: bool

    class Config:
        orm_mode = True
