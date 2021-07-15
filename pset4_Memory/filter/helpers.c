#include "helpers.h"
#include <math.h>

int color(int color);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtBlue +
                                 image[i][j].rgbtGreen +
                                 (double)image[i][j].rgbtRed) / 3);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // algorithm for converting an image to sepia
            int sepiaRed = round(0.393 * image[i][j].rgbtRed +
                                 0.769 * image[i][j].rgbtGreen +
                                 0.189 * image[i][j].rgbtBlue);

            int sepiaGreen = round(0.349 * image[i][j].rgbtRed +
                                   0.686 * image[i][j].rgbtGreen +
                                   0.168 * image[i][j].rgbtBlue);

            int sepiaBlue = round(0.272 * image[i][j].rgbtRed +
                                  0.534 * image[i][j].rgbtGreen +
                                  0.131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = color(sepiaRed);
            image[i][j].rgbtGreen = color(sepiaGreen);
            image[i][j].rgbtBlue = color(sepiaBlue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < ceil(width / 2); j++)
        {
            RGBTRIPLE container = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = container;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // image copy
    RGBTRIPLE new_image[height][width];

    // i - matrix rows
    for (int i = 0; i < height; i++)
    {
        // j - matrix columns
        for (int j = 0; j < width; j++)
        {
            float sum_rgbtRed = 0;
            float sum_rgbtGreen = 0;
            float sum_rgbtBlue = 0;

            // number of neighbors of pixel [i, j]
            int num_neighbors = 0;

            // get the sum of all rgbt.. elements and
            // the number of neighbors for pixel [i, j]
            // di, dj - offset
            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    // coordinates of the neighboring pixel with pixel [i, j]
                    int ai = i + di;
                    int aj = j + dj;

                    if ((0 <= ai && ai < height) && (0 <= aj && aj < width))
                    {
                        sum_rgbtRed += image[ai][aj].rgbtRed;
                        sum_rgbtGreen += image[ai][aj].rgbtGreen;
                        sum_rgbtBlue += image[ai][aj].rgbtBlue;
                        num_neighbors++;
                    }
                }
            }

            // new value of pixel
            new_image[i][j].rgbtRed = round(sum_rgbtRed / num_neighbors);
            new_image[i][j].rgbtGreen = round(sum_rgbtGreen / num_neighbors);
            new_image[i][j].rgbtBlue = round(sum_rgbtBlue / num_neighbors);

        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = new_image[i][j];
        }
    }

    return;
}

int color(int color)
{
    int result;
    if (color > 255)
    {
        result = 255;
    }
    else
    {
        result = color;
    }
    return result;
}