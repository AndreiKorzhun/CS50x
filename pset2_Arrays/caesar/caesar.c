#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int validate(string key);


int main(int argc, string argv[])
{
    // counting Command-Line Arguments
    if (argc == 2 && validate(argv[1]) != 1)
    {
        string str = get_string("plaintext: ");     //prompts the user for a secret message
        // changes the message to the actual key value
        printf("ciphertext: ");
        for (int i = 0, n = strlen(str); i < n; i++)
        {
            if (isupper(str[i]))
            {
                printf("%c", 65 + (str[i] - 65 + atoi(argv[1])) % 26);
            }
            else if (islower(str[i]))
            {
                printf("%c", 97 + (str[i] - 97 + atoi(argv[1])) % 26);
            }
            else
            {
                printf("%c", str[i]);
            }
        }
        printf("\n");
        return 0;

    }
    else
    {
        // invalid input
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }
}

// validating the Key
int validate(string key)
{
    int num = 0;
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        if (isdigit(key[i]) == false)
        {
            return 1;
        }
    }
    return 0;
}