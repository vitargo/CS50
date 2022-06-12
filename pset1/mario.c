#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    for (int i = 1; i <= h; i++)
    {
        for (int space = h; space > i; space--)
        {
            printf(" ");
        }

        for (int dash = 0; dash < i; dash++)
        {
            printf("#");
        }

        printf("  ");

        for (int dash2 = 0; dash2 < i; dash2++)
        {
            printf("#");
        }

        printf("\n");
    }
}
