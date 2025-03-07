#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 512

bool validateArguments(int argc);

FILE *openMemoryCard(char *file);

FILE *openJpgFile(int *jpg_count, char *jpg_name);

void closeJpgFile(FILE *outptr);

void recoverJpgs(FILE *raw_file, int *jpg_count, bool *found_jpg);

int main(int argc, char *argv[])
{
    // Validate command-line arguments
    if (!validateArguments(argc))
    {
        fprintf(stderr, "Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card file
    char *file = argv[1];
    FILE *raw_file = openMemoryCard(file);

    // Initialize variables for JPEG recovery
    bool found_jpg = false;
    int jpg_count = 0;

    // Recover JPEG images
    recoverJpgs(raw_file, &jpg_count, &found_jpg);

    // Close the memory card file
    fclose(raw_file);

    return 0;
}

// Functions
// Validate command-line arguments
bool validateArguments(int argc)
{
    return (argc == 2);
}

// open the memory card file
FILE *openMemoryCard(char *file)
{
    FILE *raw_file = fopen(file, "rb");
    if (raw_file == NULL)
    {
        fprintf(stderr, "Could not open %s\n", file);
        exit(EXIT_FAILURE);
    }
    return raw_file;
}

// Create a new JPEG file
FILE *openJpgFile(int *jpg_count, char *jpg_name)
{
    FILE *outptr = NULL;
    sprintf(jpg_name, "%03d.jpg", *jpg_count);
    outptr = fopen(jpg_name, "wb");
    if (outptr == NULL)
    {
        fprintf(stderr, "Could not create %s\n", jpg_name);
        exit(EXIT_FAILURE);
    }
    // Return pointer
    (*jpg_count)++;
    return outptr;
}

// Close the current JPEG file
void closeJpgFile(FILE *outptr)
{
    fclose(outptr);
}

// Recover JPEG images from the memory card
void recoverJpgs(FILE *raw_file, int *jpg_count, bool *found_jpg)
{
    uint8_t buffer[BUFFER_SIZE];
    char jpg_name[8];
    FILE *outptr = NULL;

    // Read the memory card in blocks
    while (fread(buffer, 1, BUFFER_SIZE, raw_file) == BUFFER_SIZE)
    {
        // Check for the JPEG file signature
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If a JPEG is already found, close the previous one
            if (*found_jpg)
            {
                closeJpgFile(outptr);
            }
            else
            {
                // If this is the first JPEG, set the flag
                *found_jpg = true;
            }

            // Open a new JPEG file
            outptr = openJpgFile(jpg_count, jpg_name);
        }

        // If a JPEG is found, write the buffer content to the file
        if (*found_jpg)
        {
            fwrite(buffer, 1, BUFFER_SIZE, outptr);
        }
    }

    // Close the last JPEG file
    closeJpgFile(outptr);
}
