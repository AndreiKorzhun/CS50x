from cs50 import get_float
from math import floor


def main():
    # converting dollars to cents
    cents = round(money() * 100)

    # number of coins
    number = 0

    for i in [25, 10, 5, 1]:
        # get the number of coins of each denomination
        number += floor(cents / i)
        # get the number of cents after deducting coins of each denomination
        cents = cents % i

    # print minimum number of coins
    print(number)


# getting a positive number from the user
def money():
    while True:
        dollars = get_float("Change owed: ")
        if dollars > 0:
            break
    return dollars


main()