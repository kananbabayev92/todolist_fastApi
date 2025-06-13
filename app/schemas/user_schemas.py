# File: app/schemas/user_schemas.py
from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    # this schema  is used  as a base for other user schemas
    email: str
    username : Optional[str] = None

class UserCreate(UserBase):
    # this schema is used to create a new user
    password: str
    is_active: bool = True

    class Config:
        from_attributes = True

class User(UserBase):
    # this schema is used to return user details
    # it inherits from UserBase and adds an id field
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    # this schema is used to update user details
    email: Optional[str]= None
    username: Optional[str]= None
    password: Optional[str]= None
    is_active: Optional[bool]= None


#print(UserCreate.model_fields.keys()) # to get the fields of the usercreate schema

#print(User.model_fields.keys()) # to get the fields of the user schema 

# the schema UserLogin is used to login a user
class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str