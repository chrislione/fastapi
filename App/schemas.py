from pydantic import BaseModel, EmailStr,ConfigDict
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from typing import Literal
# from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Postm(PostBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    owner_id: int
    owner:UserOut

    model_config = ConfigDict(from_attributes=True)


class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = ConfigDict(from_attributes=True)


# class PostOut(BaseModel):
#     Post: Post
#     votes: int

#     class Config:
#         orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    # dir: conint(le=1) legacy-style typing and will be removed in v3
    # dir: Annotated[int, Field(le=1)]
    dir: Literal[0, 1]
