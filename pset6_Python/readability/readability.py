from cs50 import get_string
import re


def main():
    # text input
    str = get_string("Text: ")

    averageOfLetters = 100 * numberOfLetters(str) / numberOfWords(str)
    averageOfSentences = 100 * numberOfSentences(str) / numberOfWords(str)

    # compute the Coleman-Liau index
    index = round(0.0588 * averageOfLetters - 0.296 * averageOfSentences - 15.8)
    # outputs the grade level for the text
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


# determines the number of letters in the text
def numberOfLetters(text):
    letters = len(re.findall("[a-zA-Z]", text))
    return letters


# determines the number of words in the text
def numberOfWords(text):
    words = text.count(" ") + 1
    return words


# determines the number of sentence in the text
def numberOfSentences(text):
    sentences = len(re.findall("[.!?]", text))
    return sentences


main()