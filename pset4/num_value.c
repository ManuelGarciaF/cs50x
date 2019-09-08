#include <stdio.h>
#include <string.h>
#include "num_value.h"

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }
    
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        int n = num_value(argv[1][i]);
        printf("%c = %i\n",argv[1][i], n);
    }

}