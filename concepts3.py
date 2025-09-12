# concepts3.py - using imports (modules)

import math_utils  # import the whole file

print("✅ Using math_utils module")

a, b = 15, 5
print(f"{a} + {b} = {math_utils.add(a, b)}")
print(f"{a} - {b} = {math_utils.subtract(a, b)}")
print(f"{a} * {b} = {math_utils.multiply(a, b)}")
print(f"{a} / {b} = {math_utils.divide(a, b)}")

# You can also import only what you need
from math_utils import add, multiply

print("\n🎯 Selective import:")
print("add:", add(2, 3))
print("multiply:", multiply(4, 6))
