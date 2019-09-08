// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;

// Represents a trie
node *root;

unsigned int tsize = 0;

void clear(node *ptr);

// gets a number from 0-26 from a character
int num_value(char c)
{
    if (isupper(c))
    {
        return c - 65;
    }
    else if (islower(c))
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

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        return false;
    }
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        node *ptr = root;
        // Iterate through letters in word
        for (int i = 0, len = strlen(word); i < len; i++)
        {
            int val = num_value(word[i]);

            // if no node exists, create one
            if (ptr->children[val] == NULL)
            {
                ptr->children[val] = malloc(sizeof(node));

                ptr->children[val]->is_word = false;
                for (int k = 0; k < N; k++)
                {
                    ptr->children[val]->children[k] = NULL;
                }
            }

            // change pointer to next node
            ptr = ptr->children[val];

            // if gotten to last letter, set is_word to true
            if (i == len - 1)
            {
                ptr->is_word = true;
                tsize++;
            }
        }
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return tsize;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    node *ptr = root;
    for (int i = 0, len = strlen(word); i < len; i++)
    {
        int val = num_value(word[i]);
        if (ptr->children[val] == NULL)
        {
            return false;
        }
        else
        {
            ptr = ptr->children[val];
        }

        if (i == len - 1 &&
            ptr->is_word == true)
        {
            return true;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    clear(root);
    return true;
}

void clear(node *ptr)
{
    for (int i = 0; i < N; i++)
    {
        if (ptr->children[i] != NULL)
        {
            clear(ptr->children[i]);
        }
    }
    free(ptr);
}