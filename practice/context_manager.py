f = open("my_file.txt", "w")
try:
    f.write("Hello, world!")
finally:
    f.close() # You must remember to close it manually

    # with open("my_file.txt", "w") as f:
    # f.write("Hello, world!")
# The file is automatically closed here, even if an error happened inside the block.