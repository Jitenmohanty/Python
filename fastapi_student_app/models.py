from pydantic import BaseModel

class Student(BaseModel):
    id: int | None = None
    name: str
    grade: int

class StudentCreate(BaseModel):
    name: str
    grade: int
