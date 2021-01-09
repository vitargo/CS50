#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long number;

    do
    {
        number = get_long("Number: ");
    }
    while (number < 999999999999 && number > 10000000000000000);
    
    int sum = 0;
    int num_1 = 0;
    int num_2 = 0;
    int num_2_1 = 0;
    long mod_num = number;
    int i = 0;    

    while (mod_num > 0)
    {
        num_1 = mod_num % 10;
        sum = sum + num_1;
        mod_num = mod_num / 10;
        i++;
        if (mod_num == 0)
        {
            break;
        } 
        num_2_1 = mod_num % 10;
        num_2 = num_2_1 * 2;
        if (num_2 > 9)
        { 
            num_2 = (num_2 % 10) + (num_2 / 10);
        }
        sum = sum + num_2;
        mod_num = mod_num / 10;
        i++;
        if (mod_num == 0)
        {
            break;
        } 
    }
    if (i < 13 || i > 16)
    {
        printf("INVALID\n");
        return 0;
    }
    if (sum % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }
    if (i % 2 == 0)
    {
        switch (num_2_1)
        {
            case 4:
                printf("VISA\n");
                break;

            case 5:
                if (num_1 > 0 && num_1 < 6)
                {
                    printf("MASTERCARD\n");
                    break;
                }
            default:
                printf("INVALID\n");
                break;
        }
    }
    else
    {
        switch (num_1)
        {
            case 4:
                printf("VISA\n");
                break;

            case 3:
                if (num_2_1 == 4 || num_2_1 == 7)
                {
                    printf("AMEX\n");
                    break;
                }
            default:
                printf("INVALID\n");
                break;
        }
    }
}
