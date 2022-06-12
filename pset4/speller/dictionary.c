// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];
int wordcount = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}
/*
bool printHashtable (node *table[])
{
    for (int i = 0; i < N; i++)
    {
        for (node *ptr = hashtable[i]; ptr !=NULL; ptr = ptr->next)
        {
            printf("%s\t", ptr->word);

        }
        printf ("\n");
    }

    return true;

}
*/

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
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


    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
        //створюю новий вузол
        node *newWord = malloc (sizeof (node));
        //перевіряю чи виділена пам'ять
        if (newWord == NULL)
        {
            fclose (file);
            return false;
        }
        //роблю копію слова у хештаблицю
        strcpy (newWord->word, word);
        //хешую слово
        int n = hash(word);
        //додаю слово до корзини
        newWord->next = hashtable[n];
        hashtable[n] = newWord;

        wordcount ++;

    }

    // Close dictionary
    fclose(file);
    //printHashtable(hashtable);

    // Indicate success
    return true;

}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (true) return wordcount;
    else return 0;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    int y = strlen (word);
    char copy [y+1];
    copy [y] = '\0';
    for (int c = 0; c < y; c++)
    {
        copy[c] = tolower (word [c]);
    }

    int n = hash(copy);

    node *cursor = hashtable [n];
    while (cursor != NULL)
    {
        if (strcmp (cursor->word, copy) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO


    for (int i = 0; i < 26; i++)
    {
        node *cur = hashtable[i];
        while (cur != 0)
        {
            node *tmp = cur;
            cur = cur->next;
            free (tmp);
        }
    }
    return true;
}
