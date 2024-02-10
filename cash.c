#include <cs50.h>
#include <stdio.h>

int calc_quarters(int cents);
int calc_dimes(int cents);
int calc_nickles(int cents);
int calc_pennies(int cents);

int main(void)
{
    int cents;
    do
    {
        cents = get_int("Change owed: ");
    }
    while (cents < 0);

    int quarters = calc_quarters(cents);
    cents = cents - (quarters * 25);
    int dimes = calc_dimes(cents);
    cents = cents - (dimes * 10);
    int nick = calc_nickles(cents);
    cents = cents - (nick * 5);
    int pennies = calc_pennies(cents);
    cents = cents - (pennies * 1);
    int total = quarters + dimes + nick + pennies;
    printf("%d ", total);
}

int calc_quarters(int cents)
{
    int quarters = 0;
    while (cents >= 25)
    {
        quarters++;
        cents -= 25;
    }
    return quarters;
}

int calc_dimes(int cents)
{
    int dimes = 0;
    while (cents >= 10)
    {
        dimes++;
        cents -= 10;
    }
    return dimes;
}

int calc_nickles(int cents)
{
    int nick = 0;
    while (cents >= 5)
    {
        nick++;
        cents -= 5;
    }
    return nick;
}

int calc_pennies(int cents)
{
    int pennies = 0;
    while (cents >= 1)
    {
        pennies++;
        cents -= 1;
    }
    return pennies;
}
