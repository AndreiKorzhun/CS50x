import cs50
import csv
from sys import argv, exit


# open database for SQLite
db = cs50.SQL("sqlite:///students.db")


def main():
    # checking the number of input arguments in the terminal
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} characters.csv")
        exit(1)

    # open file CSV
    with open(argv[1], "r") as file:
        # create DictReader
        reader = csv.DictReader(file)

        # iterate over CSV file
        for row in reader:
            # creates a list in which it separates name into first, middle and last name
            name = row['name'].split()
            # if the list name doesn't contain a middle name, enter None
            if len(name) == 2:
                name.insert(1, None)

            # insert the values from the CSV file into students.db
            db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?,?,?,?,?)",
                       name[0], name[1], name[2], row['house'], row['birth'])


main()
