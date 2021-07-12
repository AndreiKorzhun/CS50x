#include <cs50.h> // prompt a user
#include <stdio.h>

int main(void)
{
    // Prompt for start size
    int start_size;
    do
    {
        start_size = get_int("Start size: ");
    }
    while (start_size < 9);

    // Prompt for end size
    int end_size;
    do
    {
        end_size = get_int("End size: ");
    }
    while (end_size < start_size);

    // Calculate number of years until we reach threshold
    int delta;
    int years = 0;
    for (; start_size < end_size; years += 1)
    {
        // Each year, n / 3 new llamas are born, and n / 4 llamas pass away
        delta = start_size / 3 - start_size / 4;
        start_size += delta;
    }

    // Print number of years
    printf("Years: %i\n", years);
}