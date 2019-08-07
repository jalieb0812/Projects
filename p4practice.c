//jo practice with types and linked l ists

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>

typedef struct sllist //do i need a diffrent name bc its self referntial?

{

    int n;
    struct sllist *next;


}
sllnode;

//create linked list

sllnode* create(VAL val);

sllnode* new = create(6);

//check if in linked list
bool find(sllnode* head, VALUE val);
bool exists = find(list, 6);

//insert value into linked list

sllnode* insert(sllnode* head, VALUE val);
list = insert(list, 12);

//destroy linked list
void destroy(sllnode* head);

int main (int argc, char *argv[])

{



}