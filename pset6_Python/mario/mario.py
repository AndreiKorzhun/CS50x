#
# mario.py
#
# A half-pyramid of a specified height
#
# CS50
# problem set 6
#
from cs50 import get_int


def main():
    n = positiv_int()
    m = 1
    for i in range(n):
        space(n - m)
        sharp(m)
        print("  ", end="")
        sharp(m)
        if i != n:
            print()
            m += 1


# checks if a number is a positive integer from 1 to 8


def positiv_int():
    while True:
        number = get_int("Height: ")
        if number > 0 and number <= 8:
            break
    return number


def space(n):
    print(" " * n, end="")


def sharp(n):
    print("#" * n, end="")


main()