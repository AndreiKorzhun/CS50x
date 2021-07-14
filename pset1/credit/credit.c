#include <cs50.h>
#include <stdio.h>

int sum1(long number);
int sum2(long number);

int main(void)
{
    // prompt for input
    long number;
    do
    {
        number = get_long("Number: ");
    }
    while (number < 0);

    // calculation of the sum of digits
    int result = sum1(number) + sum2(number / 10);

    // check for card length and starting digits
    if (result % 10 == 0)
    {
        if (number / 10000000000000 == 34 || number / 10000000000000 == 37)
        {
            printf("AMEX\n");
        }
        else if (number / 100000000000000 >= 51 && number / 100000000000000 <= 55)
        {
            printf("MASTERCARD\n");
        }
        else if (number / 1000000000000000 == 4 || number / 1000000000000 == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

// calculating the sum of numbers
int sum1(long number)
{
    int result = 0;
    while (number > 0)
    {
        int n = number % 10;
        result += n;
        number /= 100;
    }
    return result;
}

// calculating the sum of numbers which are multiplied by 2
int sum2(long number)
{
    int result = 0;
    while (number > 0)
    {
        int n = 2 * (number % 10);
        if (n >= 10)
        {
            result += n % 10 + n / 10 % 10;
        }
        else
        {
            result += n;
        }
        number /= 100;
    }
    return result;
}