import re
from cs50 import get_int


def main():
    # number is positiv integer
    number = get_positive()

    # the result of calculating the luna's algorithm
    result = sum1(number) + sum2(number / 10)

    # transform an integer into a string
    string = str(number)

    # check for card length and starting digits
    if result % 10 == 0:
        if re.match(r"^[34, 37]{2}\d{13}", string):
            # card number length is 15, the first two values are 34 or 37
            print("AMEX")
        elif re.match(r"^[5][1 - 5]{1}\d{14}", string):
            # card number length is 16, the first values is 5 the second from 1 to 5
            print("MASTERCARD")
        elif re.match(r"^[4]{1}(\d{12}|\d{15})", string):
            # card number length 13 or 16, the first values is 4
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")


# getting a positive number from the user
def get_positive():
    while True:
        number = get_int("Number: ")
        if number > 0:
            break
    return number


# calculating the sum of numbers
def sum1(number):
    result = 0
    while (number >= 1):
        # sum the numbers of the card number in one
        result += int(number) % 10
        number /= 100
    return result


# calculating the sum of numbers which are multiplied by 2
def sum2(number):
    result = 0
    while (number >= 1):
        # multiply the last digit of the number by two
        n = 2 * (int(number) % 10)
        # add the value of the resulting number n to the total result,
        # if n is more than ten, break it down into components and summarize
        if n >= 10:
            result += int(n) % 10 + int(n / 10) % 10
        else:
            result += n
        number /= 100
    return result


main()