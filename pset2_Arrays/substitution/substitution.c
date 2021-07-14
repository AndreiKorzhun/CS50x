/*************************************************
* substitution.c
*
* In a substitution cipher,
* we “encrypt” a message by replacing every letter with another letter.
*
* CS50
* problem set 2
*************************************************/

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[])
{
    // Command line should contain two arguments
    if (argc != 2)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }

    char *key = argv[1];
    // Key length
    int length = strlen(key);

    // The key must contain 26 characters
    if (length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // The key must contain characters that are alphabetic characters and contain each letter exactly once
    for (int i = 0; i < length; i += 1)
    {
        // How many times does each character meet in the key
        int count = 0;
        // Iterates over each letter and compares it to the rest
        for (int j = 0; j < length; j += 1)
        {
            if (key[i] == key[j])
            {
                count += 1;
            }
        }

        // Check if the user enters each letter exactly once
        if (count > 1)
        {
            printf("Key must contain each letter exactly once.\n");
            return 1;
        }

        // Check if the user enters only alphabetic characters
        if (isalpha(key[i]) == 0)
        {
            printf("Key must contain only alphabetic characters.\n");
            return 1;
        }
    }

    // Text input for substitution
    char *plaintext = get_string("plaintext: ");

    // Сopy the inputed text
    char *ciphertext = plaintext;

    // Replacing plaintext with ciphertext
    for (int i = 0; i < strlen(ciphertext); i += 1)
    {
        // Replaces only letters of the alphabet
        if (isalpha(ciphertext[i]) != 0)
        {
            // If the letter is uppercase
            if (isupper(ciphertext[i]) != 0)
            {
                ciphertext[i] = toupper(key[(int)ciphertext[i] - 65]);
            }
            // If the letter is lowercase
            else
            {
                ciphertext[i] = tolower(key[(int)ciphertext[i] - 97]);
            }
        }
    }

    // Ciphertext output
    printf("ciphertext: %s\n", ciphertext);
}