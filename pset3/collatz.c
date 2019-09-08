#include <stdio.h>
#include <stdlib.h>

int collatz(int n);

int main(int argc, char *argv[])
{
    if (argc != 2) 
    {
        fprintf(stderr, "Usage: ./collatz n\n");
        return 1;
    }
    int in = atoi(argv[1]);
    printf("%i\n", collatz(in));
}

int collatz(int n) 
{
    if (n == 1)
        return 0;
        
    else if (n % 2 == 0)
        return 1 + collatz(n/2);

    else
        return 1 + collatz(n*3 + 1);
}