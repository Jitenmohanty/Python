# This is the decorator function
def log_activity(original_function):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {original_function.__name__}")
        result = original_function(*args, **kwargs) # Call the original function
        print(f"Finished function: {original_function.__name__}")
        return result
    return wrapper

# Now, we apply the decorator to another function
@log_activity
def greet(name):
    print(f"Hello, {name}!")

# Calling the decorated function
greet("Alice")