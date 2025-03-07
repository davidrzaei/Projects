#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

void error_usage(const char *programName);
int check_CLA(int argc, char *argv[]);
void shiftLetters(char *str, int shift);

int main(int argc, char *argv[])
{
    if (check_CLA(argc, argv) != 0)
    {
        return 1; // Gives usage message
    }

    int shift = atoi(argv[1]);

    char plaintext[100];

    // Get user input
    if (printf("plaintext: ") < 0 || scanf("%99[^\n]", plaintext) != 1)
    {
        printf("Error reading input.\n");
        return 1;
    }

    shiftLetters(plaintext, shift);

    // Output cipher
    printf("ciphertext: %s\n", plaintext);

    return 0;
}

// Functions

// Usage error message
void error_usage(const char *programName)
{
    printf("Usage: %s key\n", programName);
}

// CLA check
int check_CLA(int argc, char *argv[])
{
    // Check for CLA
    if (argc != 2)
    {
        error_usage(argv[0]);
        return 1;
    }

    // Check if the argument is a positiv integer
    for (int i = 0; argv[1][i] != '\0'; ++i)
    {
        if (!isdigit(argv[1][i]))
        {
            error_usage(argv[0]);
            return 1;
        }
    }

    return 0;
}

// Rotate letters
void shiftLetters(char *str, int shift)
{
    for (int i = 0; str[i] != '\0'; ++i)
    {
        // Checks if input is alpha
        if (isalpha(str[i]))
        {
            // Keeps case
            char base = islower(str[i]) ? 'a' : 'A';
            // Rotate
            str[i] = (str[i] - base + shift) % 26;
            if (str[i] < 0)
            {
                str[i] += 26; // Ensures the result is positive
            }
            str[i] += base;
        }
    }
}
