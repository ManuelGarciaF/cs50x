#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int get_num_value(char c);

int main(int argc, string argv[])
{
    if (argc == 2) //check that there is exactly 1 argument
    {
        for (int i = 0, len = strlen(argv[1]); i < len; i++) //iterate through each character in the argument
        {
            if (isalpha(argv[1][i]) == false) //if any are not digits, return an error
            {
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
        }
    }
    else //if there is more than 1 argument return an error
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }

    string s_key = argv[1]; //make the key an int
    int keylen = strlen(s_key);
    
    string ptext = get_string("plaintext: "); //ask the user for the plaintext

    printf("ciphertext: ");
    int j = 0;
    for (int i = 0, len = strlen(ptext); i < len; i++) //iterate through each character in ptext
    {
        if (j >= keylen) { j = 0; }
        
        int i_key;
        i_key = get_num_value(s_key[j]);
        //printf("i_key:%i j:%i ptext:%c    ", i_key, j, ptext[i]);

        char ctext;
        if (isupper(ptext[i]))
        {
            ctext = ((get_num_value(ptext[i]) + i_key) % 26) + 65;
            printf("%c", ctext);
            j++;
        }
        else if (islower(ptext[i]))
        {
            ctext = ((get_num_value(ptext[i]) + i_key) % 26) + 97;
            printf("%c", ctext);
            j++;
        }
        else //if it's not a letter, print as it is
        {
            printf("%c", ptext[i]);
        }
    }
    printf("\n");
}

int get_num_value(char c) //calculate the numerical value of each letter (1-26)
{
    int v;
    if (isupper(c))
    {
        v = (c - 65);
    }
    else
    {
        v = (c - 97);
    }
    return v;
}
