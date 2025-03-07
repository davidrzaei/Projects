#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

string txt(void);
int count_letters(const char *txt);
int count_words(const char *txt);
int count_sentences(const char *txt);
float calculate_L(int letters, int words);
float calculate_S(int sentences, int words);
float calculate_index(float L, float S);
int round_to_nearest_int(float value);
void print_grade_level(float index);

int main(void)
{
    // Ask for user input
    string get_txt = txt();

    // Count words
    int count_w = count_words(get_txt);

    // Count letters
    int count_l = count_letters(get_txt);
    // Per 100 words
    float L = calculate_L(count_l, count_w);

    // Count sentences
    int count_s = count_sentences(get_txt);
    // Per 100 words
    float S = calculate_S(count_s, count_w);

    // Calculate using Index
    float index = calculate_index(L, S);
    // Round to nearest int
    int rounded_index = round_to_nearest_int(index);

    // Debug printf
    // printf("Letters: %i\n", count_l);
    // printf("Words: %i\n", count_w);
    // printf("Sentences: %i\n", count_s);
    // printf("Letters per 100 words (L): %.2f\n", L);
    // printf("Sentences per 100 words (S): %.2f\n", S);
    // printf("Index: %.2f\n", index);
    // printf("Rounded Index: %i\n", rounded_index);

    // Output grade level
    print_grade_level(index);
}

// Functions

// Ask for user input
string txt(void)
{
    string txt;
    do
    {
        txt = get_string("Enter sample text here: ");
    }
    // Only accept input with at least 1 alpha letter
    while (!isalpha(txt[0]));

    return txt;
}

// Count letters
int count_letters(const char *txt)
{
    int count_letters = 0;

    while (*txt != '\0')
    {
        // Only count alpha letters
        if (isalpha((unsigned char) *txt))
        {
            count_letters++;
        }
        txt++;
    }

    return count_letters;
}

// Count words
int count_words(const char *txt)
{
    int count_words = 0;
    int is_word_indicator = 0;

    while (*txt != '\0')
    {
        if (*txt == ' ' || *txt == '.' || *txt == '!' || *txt == '?')
        {
            if (!is_word_indicator)
            {
                count_words++;
                is_word_indicator = 1;
            }
        }
        else
        {
            is_word_indicator = 0; // Avoid counting words by ex. ". ! "
        }

        txt++;
    }

    return count_words;
}
////

// Count sentences

int count_sentences(const char *txt)
{
    int count_sentences = 0;
    int has_alphabetical_letter = 0;

    while (*txt != '\0')
    {
        // Sentence ord when ".", "!", "?"
        if (*txt == '.' || *txt == '!' || *txt == '?')
        {
            // Requires a alpha letter before counting new sentence
            if (has_alphabetical_letter)
            {
                count_sentences++;
                has_alphabetical_letter = 0;
            }
        }
        else if (isalpha((unsigned char) *txt))
        {
            has_alphabetical_letter = 1;
        }

        txt++;
    }

    return count_sentences;
}

// Calculate using Index

// Letters per 100 words = L
float calculate_L(int letters, int words)
{
    return (float) letters / words * 100.0;
}

// Sentence per 100 words = S
float calculate_S(int sentences, int words)
{
    return (float) sentences / words * 100.0;
}

// Use (0.0588 * L) - (0.296 * S) - 15.8
float calculate_index(float L, float S)
{
    return 0.0588 * L - 0.296 * S - 15.8;
}
// Round to nearest int
int round_to_nearest_int(float value)
{
    return (int) (value + 0.5);
}

// Output grade level
void print_grade_level(float index)
{
    // If final sum is less than 1
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    // If final sum is 1-15
    else if (index >= 1 && index <= 15)
    {
        printf("Grade %i\n", round_to_nearest_int(index));
    }
    else
    // If final sum is = or < than 16
    {
        printf("Grade 16+\n");
    }
}
