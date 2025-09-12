from pydantic import BaseModel, Field
from typing import Optional

# User
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str

# Todo
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TodoCreate(TodoBase):
    pass

class TodoOut(TodoBase):
    id: str
    owner_id: str

# JWT token
class Token(BaseModel):
    access_token: str
    token_type: str
