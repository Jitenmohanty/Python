from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory "database"
students = [
    {"id": 1, "name": "Alice", "grade": 85},
    {"id": 2, "name": "Bob", "grade": 92},
    {"id": 3, "name": "Charlie", "grade": 78},
    {"id": 4, "name": "Diana", "grade": 95},
    {"id": 5, "name": "Evan", "grade": 88},
    {"id": 6, "name": "Fiona", "grade": 67},
    {"id": 7, "name": "George", "grade": 91},
    {"id": 8, "name": "Hannah", "grade": 74},
    {"id": 9, "name": "Ian", "grade": 83},
    {"id": 10, "name": "Jenny", "grade": 79},
    {"id": 11, "name": "Kevin", "grade": 96},
    {"id": 12, "name": "Luna", "grade": 82},
    {"id": 13, "name": "Mike", "grade": 89},
    {"id": 14, "name": "Nina", "grade": 93},
    {"id": 15, "name": "Oscar", "grade": 70},
    {"id": 16, "name": "Paul", "grade": 84},
]

# Home route
@app.route("/")
def home():
    return "🎉 Welcome to Complex Flask API!"

# GET all students
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)

# GET single student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

# POST new student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    if "name" not in data or "grade" not in data:
        return jsonify({"error": "Missing name or grade"}), 400
    
    new_id = max([s["id"] for s in students]) + 1
    new_student = {"id": new_id, "name": data["name"], "grade": data["grade"]}
    students.append(new_student)
    return jsonify(new_student), 201

# PUT update student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student["name"] = data.get("name", student["name"])
    student["grade"] = data.get("grade", student["grade"])
    return jsonify(student)

# DELETE student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    global students
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": f"Student {student_id} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
