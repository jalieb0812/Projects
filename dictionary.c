// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <cs50.h>
#include <strings.h>
#include <string.h>

#include "dictionary.h"


//can assume dict will contain 1 word, sorted from top to bootom alphabetically each word ending with /n
//can assume in dcit no word will be longer than LENGTH (45); no words will appear more than once;;
//can assume in dict no word will appear morehtan once, that each word will contain only lowercase alphabet letters and possibly apostrophies but not at begning of word./
//can alter value of N and implimentation of hash
// no leaking memory; use valgrind
// Represents number of buckets in a hash table///
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table//a global array
node *hashtable[N];



//counter for size
int word_counter = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter//
//const char means that once the string is passed in i cant change it!!!!!
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

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
    char word[LENGTH + 1]; // ensures that no word can be longer than 45 chars

    // Insert words into hash table
    // while loop iterates over word in dictionary and reads words therein, one at a time, into a buffer (i.e., string) called word
    while (fscanf(file, "%s", word) != EOF)
    {

        //// TODO insert words into hash table

        ///jll code

        // for every word scanned, Malloc a node*
        node *new_node = malloc(sizeof(node));

        //check if malloc succedeed
        if (new_node == NULL)
        {

            unload(); // unload dict if malloc did not succeed
            return false;

        }


        //if maloc succeeds, then copy new word into next node
        strcpy(new_node ->word, word);


        word_counter++;
        //new_node->next = NULL;


        new_node->next = hashtable[hash(new_node->word)]; //new_node points to head


        hashtable[hash(new_node->word)] = new_node; //head points to new_node

        //hashtable[hash(new_node->word)]->next = new_node ->word;
        //head = hash(new_node ->word);
        // ok figured out that head == hashtable[hash(new_node->word)]
        //*hashtable[hash(new_node->word)] = new_node->word ;

        // how to insert into linked list
        // new node inserted into the begingin
        //so new node shoudl point to whatever was previosu first vlaue in list
        //so point new_node to whatever value head (first node pointer) was pointing to


        //now can reassigne what head pointer to new_node
        //hashtable[hash(new_node->word)] = new_node;
        //new_node->next = NULL;
        //printf("new word in dict %s \n", new_node->word);


        //for (node *ptr = hashtable[hash(word)]; ptr != NULL; ptr = ptr->next)
        //{
        //printf("words at bucket %i are: %s\n", hash(word), hashtable[hash(word)]->word);
        //hashtable[hash(word)] = hashtable[hash(word)]->next;


        //}
        //how to know which word to put into which list: use hash function

        //new_node-> word has the word from the dict
        //hasing new_node word will giv eus the index of bucket in the hash table
        //insert tio the linked list

        //jo self code starting here


        //jl code ends here
    }
    //for (int i = 0; i < word_counter; i++ )

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    //keep track of how many words are put in
    //keep a counter in load that is a global variable
    //from here can do size
    return word_counter;
}

// Returns true if word is in dictionary else false//must be case insensitive
//only return true on possesives if possesive is in the dictionary
bool check(const char *word)
{
    // TODO

    //jo code starts

    node *head = hashtable[hash(word)];
    node *cursor = head;


    while (cursor != NULL)
    {


        if (strcasecmp(word, cursor->word) == 0)

        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }

    }

    //jo code ends here
    return false;

}

//jl code here
//node word = const char *word;
// Unloads dictionary from memory, returning true if successful else false

bool unload(void)
{
    // TO  DO

    //jo code starts
    // create cursor pointing to head
    int count = 0;
    for (int i = 0, n = N; i < n; i++)
    {

        node *head = hashtable[i];
        node *cursor = head;
        count ++;
        while (cursor != NULL) //
        {


            node *temp = cursor;
            cursor = cursor ->next;
            free(temp);


        }


    }


    if (count == N)
    {
        return true;
    }
    else
    {
        return false;
    }



}
