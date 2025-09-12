from fastapi import FastAPI, HTTPException
from models import Student, StudentCreate
from storage import load_students, save_students
from typing import List

app = FastAPI(title="Student Management API", version="1.0")

# Home route
@app.get("/")
def home():
    return {"message": "🎉 Welcome to FastAPI Student API!"}

# GET all students
@app.get("/students", response_model=List[Student])
def get_students():
    return load_students()

# GET single student
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    students = load_students()
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# POST new student
@app.post("/students", response_model=Student, status_code=201)
def add_student(student: StudentCreate):
    students = load_students()
    new_id = max([s["id"] for s in students], default=0) + 1
    new_student = {"id": new_id, "name": student.name, "grade": student.grade}
    students.append(new_student)
    save_students(students)
    return new_student

# PUT update student
@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentCreate):
    students = load_students()
    existing_student = next((s for s in students if s["id"] == student_id), None)
    if not existing_student:
        raise HTTPException(status_code=404, detail="Student not found")

    existing_student["name"] = student.name
    existing_student["grade"] = student.grade
    save_students(students)
    return existing_student

# DELETE student
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    students = load_students()
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    students = [s for s in students if s["id"] != student_id]
    save_students(students)
    return {"message": f"Student {student_id} deleted"}
