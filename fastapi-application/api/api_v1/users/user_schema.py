from datetime import datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class UserSchema(BaseModel):

    username: str
    password: str


class UserCreate(UserSchema):
    pass


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime

class User(UserSchema):
    model_config = ConfigDict(
        strict=True,
    )

    id: int
    created_at: datetime
