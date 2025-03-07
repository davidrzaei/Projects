#include <cs50.h>
#include <stdio.h>

long get_number(void);
int half_digit(long ask);
int times_two(int end);
void check(int sum, long cardNumber);

int main(void)
{
    long ask = get_number();
    int sum = half_digit(ask);
    check(sum, ask);
}

// Functions

// Get user input
long get_number(void)
{
    long ask;
    do
    {
        ask = get_long("Enter credit card number here: ");
    }
    while (ask <= 0);
    return ask;
}

// Calculate whether number is a valid card number
// Add every other number from right-left
int half_digit(long ask)
{
    int sum = 0;
    bool second = false;
    while (ask > 0)
    {
        int end = ask % 10;
        sum += second ? times_two(end) : end;
        second = !second;
        ask = ask / 10;
    }
    return sum;
}

// Multiply by 2
int times_two(int end)
{
    int multi = end * 2;
    int sum = 0;
    while (multi > 0)
    {
        sum += multi % 10;
        multi = multi / 10;
    }
    return sum;
}

// Determine if input is valid
void check(int sum, long cardNumber)
{
    if (sum % 10 == 0)
    {
        // Count lenght of input
        int length = 0;
        long tempCardNumber = cardNumber;
        while (tempCardNumber > 0)
        {
            tempCardNumber /= 10;
            length++;
        }

        // ID card type from input length and first digit/s
        if (length == 15 && (cardNumber / 10000000000000 == 34 || cardNumber / 10000000000000 == 37))
        {
            printf("AMEX\n");
        }
        else if ((length == 13 && cardNumber / 1000000000000 == 4) || (length == 16 && cardNumber / 1000000000000000 == 4))
        {
            printf("VISA\n");
        }
        else if (length == 16 && (cardNumber / 100000000000000 >= 51 && cardNumber / 100000000000000 <= 55))
        {
            printf("MASTERCARD\n");
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
