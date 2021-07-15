#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // accept exactly one command-line argument, the name of a forensic image
    if (argc != 2)
    {
        printf("Usage: %s image\n", argv[0]);
        return 1;
    }


    // open "card.raw"
    FILE *f = fopen(argv[1], "r");
    if (f == NULL)
    {
        return 1;
    }

    // allocate memory for information read from the card
    BYTE *buffer = malloc(512 * sizeof(BYTE));
    // is there enough space in the computer memory
    if (buffer == NULL)
    {
        return 1;
    }

    // allocate memory for the name of the found images
    char *name = malloc(8);
    // is there enough space in the computer memory
    if (name == NULL)
    {
        return 1;
    }
    int num = 0;
    bool open = false;
    while (fread(buffer, sizeof(BYTE), 512, f) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // first image
            sprintf(name, "%03i.jpg", num);
            FILE *img = fopen(name, "w");
            fwrite(buffer, sizeof(BYTE), 512, img);
            fclose(img);
            open = true;
            num += 1;

        }
        else
        {
            if (open == true)
            {
                // adds the read bytes to the image
                FILE *img = fopen(name, "a");
                fwrite(buffer, sizeof(BYTE), 512, img);
                fclose(img);
            }

        }
    }
    fclose(f);
    free(buffer);
    free(name);
    return 0;
}