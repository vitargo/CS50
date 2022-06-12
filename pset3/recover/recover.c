#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    char *infile = argv [1];
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }
    int i = 0;

    unsigned char buf [512];
    FILE *outptr = NULL;
    char filename [8];


   while (! feof (inptr))
    {
        //fread(buf, 512, 1, inptr);
        int size = fread(buf, 512, 1, inptr);
        if (size != 1)
        {
           break;
        }
        if (buf[0] == 0xff && buf[1] == 0xd8 && buf[2] == 0xff && (buf[3] & 0xf0) == 0xe0)
        {
            i++;
            if (outptr)
            {
                fclose (outptr);
            }
            sprintf(filename, "%03i.jpg", i - 1);
            outptr = fopen(filename, "w");
            fwrite(buf, 512, 1, outptr);
        }
        else if (outptr)
        {
            fwrite(buf, 512, 1, outptr);
        }

    }

    fclose (inptr);

     if (outptr) fclose (outptr);

    return 0;

}

