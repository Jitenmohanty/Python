from pydantic import BaseModel
from typing import Optional

# User models
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str

# Todo models
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TodoCreate(TodoBase):
    pass

class TodoOut(TodoBase):
    id: str
    owner_id: str

# JWT token model
class Token(BaseModel):
    access_token: str
    token_type: str
