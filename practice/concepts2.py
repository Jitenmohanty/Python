# ✅ Python Concepts - Part 2
import os

# 1. Function with parameters and return
def add_numbers(a, b):
    return a + b

print("➕ Add Function:", add_numbers(10, 20))

# 2. List comprehension (filter + transform in one line)
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

squares = [n * n for n in numbers]  # square each number
evens = [n for n in numbers if n % 2 == 0]  # filter even numbers

print("\n🔢 Squares:", squares)
print("🔹 Even Numbers:", evens)

# 3. Error handling (try / except)
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print("\n⚠️ Error caught:", e)

# Save file inside E:\Python\
file_path = os.path.join("E:\\Python", "testfile.txt")

# Write to file with UTF-8
with open(file_path, "w", encoding="utf-8") as f:
    f.write("Hello, this is Python writing to a file!\n")
    f.write("Line 2: Python is awesome 🚀\n")

# Read from file with UTF-8
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

print("\n📂 File Content:")
print(content)

