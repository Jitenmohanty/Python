import json
import os

FILE = os.path.join(os.path.dirname(__file__), "students.json")

def load_students():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_students(students):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4)
