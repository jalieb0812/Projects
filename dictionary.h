// Declares a dictionary's functionality

#ifndef DICTIONARY_H
#define DICTIONARY_H

#include <stdbool.h>

// Maximum length for a word
// (e.g., pneumonoultramicroscopicsilicovolcanoconiosis)
#define LENGTH 45

// Prototypes
bool load(const char *dictionary);// bool load(const string dictionary)
unsigned int size(void);
bool check(const char *word); // bool check(const string word)//implimentation of check must be case insensitive
bool unload(void);

#endif // DICTIONARY_H
