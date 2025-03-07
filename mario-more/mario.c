#include <cs50.h>
#include <stdio.h>

int get_height(void);
void print_hills(int height);

int main(void)
{

        int h = get_height();

    print_hills(h);

    return 0;
 }

// Get input from user
int get_height(void)
{
    int h;
    do
    {
        h = get_int("How high should we build, sir?: ");
    }
    while (h < 1 || h > 8);

    return h;
}

// Make the two hills
void print_hills(int h)
{
    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < h; j++)
        {
            if (i + j < h - 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }

        printf("  ");

        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }

        printf("\n");
    }
}
