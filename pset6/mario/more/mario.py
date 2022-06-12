from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height < 9 and height > 0:
        break

for i in range(height):
    c = height-i-1
    print(" " * c, end="")
    print("#" * i, end="")
    print("#  #", end="")
    print("#" * i, end="")
    print()