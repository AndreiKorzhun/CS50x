#include <cs50.h>
#include <stdio.h>

void spaces(int m);
void sharps(int m);

int main(void)
{
    // ask height
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);

    // On iteration i, print i hashes - two spaces - i hashes and then a newline
    for (int i = 1; i <= n; i++)
    {
        spaces(n - i);
        sharps(i);
        printf("  ");
        sharps(i);
        printf("\n");
    }
}

// Print "space"
void spaces(int m)
{
    for (int i = 0; i < m; i++)
    {
        printf(" ");
    }
}

// Print "sharps"
void sharps(int m)
{
    for (int i = 0; i < m; i++)
    {
        printf("#");
    }
}