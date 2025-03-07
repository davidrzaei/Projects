#include "helpers.h"
#include "math.h"
#define RED_C 0
#define GREEN_C 1
#define BLUE_C 2

int makeBlur(int c, int h, int height, int width, RGBTRIPLE image[height][width], int cP);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gray_scale = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);

            image[i][j].rgbtRed = gray_scale;
            image[i][j].rgbtGreen = gray_scale;
            image[i][j].rgbtBlue = gray_scale;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaR = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaG = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaB = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = fmin(255, sepiaR);
            image[i][j].rgbtGreen = fmin(255, sepiaG);
            image[i][j].rgbtBlue = fmin(255, sepiaB);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp;
    // Loop through all pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // Swap pixels horizontally
            temp = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = makeBlur(i, j, height, width, copy, RED_C);
            image[i][j].rgbtGreen = makeBlur(i, j, height, width, copy, GREEN_C);
            image[i][j].rgbtBlue = makeBlur(i, j, height, width, copy, BLUE_C);
        }
    }
}

// Blur function
int makeBlur(int c, int h, int height, int width, RGBTRIPLE image[height][width], int cP)
{
    float count = 0;
    int sum = 0;

    for (int i = c - 1; i <= (c + 1); i++)
    {
        for (int j = h - 1; j <= (h + 1); j++)
        {
            if (i < 0 || i >= height || j < 0 || j >= width)
            {
                continue;
            }
            if (cP == RED_C)
            {
                sum += image[i][j].rgbtRed;
            }
            else if (cP == GREEN_C)
            {
                sum += image[i][j].rgbtGreen;
            }
            else
            {
                sum += image[i][j].rgbtBlue;
            }
            count++;
        }
    }
    return round(sum / count);
}
