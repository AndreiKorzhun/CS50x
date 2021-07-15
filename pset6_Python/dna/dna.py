import csv
from sys import argv, exit


def main():
    # checking the number of input arguments in the terminal
    if len(argv) != 3:
        print(f"Usage: python {argv[0]} data.csv sequence.txt")
        exit(1)

    # open the CSV file(dna database) and read its
    csvfile = open(argv[1], "r")
    csvreader = csv.reader(csvfile)
    # open the DNA sequence and read its
    txtfile = open(argv[2], 'r')
    txtreader = txtfile.read()

    # creates a list STRs specified in the database CSV file
    strs = list(next(csvreader))
    del strs[0]

    # create a list of the maximum number of matches for all STRs
    result = []
    for i in strs:
        result.append(numberOfSTRs(i, txtreader))

    # iterates over each line in the CSV file
    for row in csvreader:
        # convert the list of STR matches from the dataset to integer format
        element = [int(item) for item in row[1:]]
        # if the database list and the resulting dna sequence list are equal
        if element == result:
            # print the person's name and finish the program
            print(row[0])
            exit(0)
    # the STR counts do not match exactly with any of the individuals in the CSV file
    print('No match')
    exit(0)


# calculates the longest row of consecutive STR repeats in a DNA sequence
def numberOfSTRs(str, txt):
    # length STR
    length = len(str)
    counter = [0]
    # for each element of the read text from the file, checks the match with STR
    for i in range(len(txt) - length):
        # if an element of text matches with STR
        if txt[i: i + length] == str:
            # if the previous element coincided with STR
            if txt[i - length: i] == str:
                # create a list item equal to the last item this list
                counter.append(counter[-1])
                # add 1 to the last element of the created list
                counter[-1] += 1
            else:
                # add 1 at the end of the list
                counter.append(1)
    # return the maximum number of matches
    return max(counter)


main()