def number_generator(limit):
    n = 0
    while n < limit:
        yield n # Pauses here and returns the value of n
        n += 1

# The function doesn't run yet, it just creates the generator object
my_gen = number_generator(3)
print(my_gen) # Output: <generator object number_generator at 0x...>

# Now we iterate, and the code inside the generator runs
print(next(my_gen)) # Output: 0
print(next(my_gen)) # Output: 1
print(next(my_gen)) # Output: 2
# Calling next() again would raise a StopIteration error because it's finished.

# Or more commonly, use it in a for loop
for number in number_generator(3):
    print(number) # Prints 0, 1, 2