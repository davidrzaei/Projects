#include <stdio.h>
#include <cs50.h>

string name(void);

int main()
{
    //Ask user for first name
    string first = get_string("What's your name? ");

    //Greet them
    printf("Hello, %s\n", first);

    //Ask for last name
    //string last = get_string("What's your last name? ");

    //Greet them again in full with a bit of flourish
    //printf("Hello, %s %s\nWonderful to meet you\n", first, last);
}
