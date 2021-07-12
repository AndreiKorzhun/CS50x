#include <cs50.h> // prompt a user
#include <stdio.h>
#include <ctype.h> // check whether a character
#include <string.h>


// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}


int compute_score(string word)
{
    /* Compute and return score for string */

    int score = 0;
    int index;

    // Iterate over each character
    for (int i = 0; i < strlen(word); i += 1)
    {
        char character = word[i];

        // Сheck whether a character is alphabetical
        if (isalpha(character))
        {
            // Check whether a character is lowercase
            if (islower(character))
            {
                // Define the index in the array 'POINTS'
                index = (int)character - 97;
            }
            // if the character is uppercase
            else
            {
                // Define the index in the array 'POINTS'
                index = (int)character - 65;
            }

            // Compute score for string
            score += POINTS[index];
        }
    }
    return score;
}