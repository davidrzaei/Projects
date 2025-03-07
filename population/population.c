#include <cs50.h>
#include <stdio.h>

int get_start(void);
int get_end(int start);

int main(void)
{
    // Initial "years"
    int years = 0;

    // "Start" Get postive number above '9'
    int start = get_start();

    // "End" Get positive number larger than "start"
    int end = get_end(start);

    // Calculate how many years to get from "Start" to "End"
    while (start < end)
    {
        start = start + (start / 3) - (start / 4);
        years++;
    }

    // Print number of years
    {
        printf("Years: %i\n", years);
    }
}

// Functions

// get_start
int get_start(void)
{
    int start;
    do
    {
        start = get_int("Start Size: ");
    }
    while (start < 9);
    return start;
}

// get_end
int get_end(int start)
{
    int end;
    do
    {
        end = get_int("End Size: ");
    }
    while (end < start);
    return end;
}
