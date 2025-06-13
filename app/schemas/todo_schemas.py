#schemas.py

from pydantic import BaseModel
from typing import Optional


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    # user_id: int


class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    # user_id: int

    class Config:
        from_attributes = True


class Todoupdate(TodoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool]

    class Config:
        from_attributes = True
