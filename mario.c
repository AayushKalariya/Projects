#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int num;
    do
    {
        num = get_int("Height: ");
    }
    while (num < 1 || num > 8);

    for (int i = 0; i < num; i++)
    {
        for (int k = 0; k < num - i - 1; k++)
        {
            printf(" ");
        }
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
