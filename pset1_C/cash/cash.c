#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // set the value in dollars and check it
    float dollars;
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);

    // converting dollars to cents
    int cents = round(dollars * 100);

    // array of available coins
    int coins[] = {25, 10, 5, 1};
    // number of elements in the array
    size_t size = sizeof(coins) / sizeof(coins[0]);

    // the minimum number of coins
    int count = 0;

    for (int i = 0; i < size; i++)
    {
        count += cents / coins[i];
        cents = cents % coins[i];
    }

    printf("%i\n", count);
}