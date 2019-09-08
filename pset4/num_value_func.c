#include <ctype.h>
#include "num_value.h"

int num_value(char c)
{
    if (isupper(c))
    {
        return c - 65;
    }
    else if(islower(c))
    {
        return c - 97;
    }
    else if (c == '\'')
    {
        return 26;
    }
    else
    {
        return -1;
    }
}