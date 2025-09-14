from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# Helper for MongoDB ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# User models
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str

    @classmethod
    def from_mongo(cls, data):
        """Helper method to convert MongoDB document to UserOut"""
        data['id'] = str(data['_id'])
        return cls(**data)

# Todo models
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False

class TodoCreate(TodoBase):
    pass

class TodoOut(TodoBase):
    id: str  # ✅ Just use "id" without alias
    owner_id: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

# JWT token model - ADD THIS
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None