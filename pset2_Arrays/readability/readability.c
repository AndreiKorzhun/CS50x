// a program that computes the approximate grade level needed to comprehend some text
#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int numberOfLetters(string text);
int numberOfWords(string text);
int numberOfSentences(string text);

int main(void)
{
    // text input
    string str = get_string("Text: ");

    float averageOfLetters =
        100 * (float)numberOfLetters(str) / numberOfWords(str);
    float averageOfSentences =
        100 * (float)numberOfSentences(str) / numberOfWords(str);
    int index = round(0.0588 * averageOfLetters -
                      0.296 * averageOfSentences - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

// determines the number of letters in the text
int numberOfLetters(string text)
{
    int letters = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return letters;
}


// determines the number of words in the text
int numberOfWords(string text)
{
    int words = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    return words + 1;
}


// determines the number of sentence in the text
int numberOfSentences(string text)
{
    // punctuation marks at the end of sentence
    int array[] = {33, 46, 63}; // {"!", ".", "?"}
    int n = sizeof(array) / sizeof(array[0]);

    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        for (int j = 0; j < n; j++)
        {
            if ((int)text[i] == array[j])
            {
                sentences++;
            }
        }
    }
    return sentences;
}