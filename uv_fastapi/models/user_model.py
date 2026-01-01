from pydantic import BaseModel, EmailStr
from typing import Optional

class UserModel(BaseModel):
    name: str
    email: EmailStr
    password: str  # raw before hash

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
