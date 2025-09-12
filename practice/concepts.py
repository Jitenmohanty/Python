# ✅ Python Concepts Demo

# 1. List (like array)
fruits = ["apple", "banana", "mango", "orange"]

print("🍎 Fruits List:")
for fruit in fruits:
    print("-", fruit)

# 2. Dictionary (like object in JS)
person = {
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "JavaScript", "SQL"]
}

print("\n👩 Person Object:")
print("Name:", person["name"])
print("Age:", person["age"])
print("Skills:", ", ".join(person["skills"]))

# 3. Class and Object
class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
    
    def drive(self):
        return f"{self.year} {self.brand} {self.model} is driving 🚗"

my_car = Car("Tesla", "Model 3", 2024)
print("\n🚘 Car Object:")
print(my_car.drive())

# 4. List of Objects
students = [
    {"name": "John", "grade": 85},
    {"name": "Emma", "grade": 92},
    {"name": "Liam", "grade": 78}
]

print("\n🎓 Students List:")
for s in students:
    print(f"{s['name']} scored {s['grade']}")

# 5. Condition
print("\n🔎 Students with grade >= 80:")
for s in students:
    if s["grade"] >= 80:
        print(s["name"])
