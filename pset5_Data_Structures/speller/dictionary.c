/**
* dictionary.c
*
* Implements a dictionary's functionality
* A program that spell-checks a file using a hash table.
*
* CS50
* problem set 5
*/

#include <stdio.h>
#include <stdbool.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 32768;
// Hash table
node *table[N];

// a counter of the number of words read from the dictionary
unsigned int m = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // сreates a copy of a word and converts it to lowercase
    int n = strlen(word);
    char word_copy[n];
    for (int i = 0; i < n; i++)
    {
        word_copy[i] = tolower(word[i]);
    }
    word_copy[n] = '\0';

    // determine which index into the hash table you should use
    int index = hash(word_copy);

    // loop from start to end of linked list
    for (node *cursor = table[index]; cursor != NULL; cursor = cursor->next)
    {
        // compare a word in a linked list
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
    }

    // the word is not in the linked list
    return false;
}

// hashes word to a number
// http://en.wikipedia.org/wiki/Jenkins_hash_function
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        hash += word[i];
        hash += (hash << 10);
        hash ^= (hash >> 6);
    }
    hash += (hash << 3);
    hash ^= (hash >> 11);
    hash += (hash << 15);
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // open dictionary
    FILE *file = fopen(dictionary, "r");
    // if the dictionary does not open, return false
    if (!file)
    {
        return false;
    }

    // a variable in which the word read from the dictionary will be stored
    char word[LENGTH + 1];

    // reads each word from the dictionary and adds it to the hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        //create a new node to store particular word
        node *n = malloc(sizeof(node));
        // if there is no way to enough memory, return false
        if (n == NULL)
        {
            unload();
            return false;
        }

        // copy the word from the dictionary to the created node
        strcpy(n->word, word);
        n->next = NULL;

        // determine which index into the hash table you should use
        int index = hash(word);

        // adds a node to a specific cell of the hash table
        if (table[index] == NULL)       // the hash table cell contains no other nodes
        {
            table[index] = n;
        }
        else        // hash table cell contains other nodes
        {
            n->next = table[index];
            table[index] = n;
        }

        // a counter of the number of words read from the dictionary
        m++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return m;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // go to each index of the hash table
    for (int i = 0; i < N; i++)
    {
        node *tmp = table[i];
        // free the memory of each node in the linked list
        for (node *cursor = table[i]; cursor != NULL; tmp = cursor)
        {
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
