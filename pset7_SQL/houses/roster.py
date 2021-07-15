import cs50
import csv
from sys import argv, exit


# open database for SQLite
db = cs50.SQL("sqlite:///students.db")


def main():
    # checking the number of input arguments in the terminal
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} 'name of a house'")
        exit(1)

    # sample of students of the specified house
    students = (db.execute('''
        SELECT first, middle, last, birth
        FROM students WHERE house = ?
        ORDER BY last, first
        ''', argv[1]))

    # iterates over each student
    for row in students:
        # doesn't display the middle name if it isn't specified
        if row['middle'] == None:
            print('{} {}, born {}'.format(row['first'], row['last'], row['birth']))
        else:
            print('{} {} {}, born {}'.format(row['first'], row['middle'], row['last'], row['birth']))


main()
