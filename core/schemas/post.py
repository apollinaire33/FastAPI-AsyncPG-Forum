from typing import Optional

from pydantic import BaseModel, constr


class PostCategorySchema(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True


class PostCategoryCreateUpdateSchema(BaseModel):
    title: constr(max_length=25)
    description: Optional[str]

    class Config:
        orm_mode = True
        