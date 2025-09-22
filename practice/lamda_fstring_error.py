name = "Charlie"
age = 8
pet_type = "dog"

# Using an f-string to embed variables
greeting = f"{name} is a {pet_type} who is {age} years old."
print(greeting) # Output: Charlie is a dog who is 8 years old.


# You can even put expressions or function calls inside
calculation = f"In two years, {name} will be {age + 2} years old."
print(calculation) # Output: In two years, Charlie will be 10 years old.

shouted_name = f"His name in uppercase is {name.upper()}."
print(shouted_name) # Output: His name in uppercase is CHARLIE.


try:
    numerator = 10
    denominator = int(input("Enter a number to divide by: "))
    result = numerator / denominator
except ZeroDivisionError:
    # This block runs ONLY if the user enters 0
    print("Error: You can't divide by zero!")
except ValueError:
    # This block runs ONLY if the user enters non-numeric text like 'cat'
    print("Error: Please enter a valid number.")
else:
    # This runs ONLY if no errors occurred
    print(f"The result is {result}.")
finally:
    # This runs ALWAYS
    print("Calculation attempt finished.")


    # A regular function
def add_func(a, b):
    return a + b

# The equivalent lambda function
add_lambda = lambda a, b: a + b

print(add_func(5, 3))    # Output: 8
print(add_lambda(5, 3))  # Output: 8


points = [(1, 5), (4, 2), (8, 9), (3, 7)]

# Sort the list by the second item in each tuple (the y-coordinate)
points.sort(key=lambda item: item[1])

print(points) # Output: [(4, 2), (1, 5), (3, 7), (8, 9)]