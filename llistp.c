// linkedlist practice

// hashtbale is now array of 10 nodes
node* hashtable[10];

hash("Joey"); // pretend reutrns 6;

// now dynimaclly allocate sapce for joe and add him to the chain

// fro walkthrough for load
//creates node struct
typedef struct node
{

    char word[LENGHT + 1];
    struct node *next;


}
node;

node *node1 = malloc(sizeof(node)); // allocates space in memory to store node
// and malloc returns the first node pointer to a node
//created by code above [node1] --> [Val][node pointer]

node *node2 = malloc(sizeof(node));
//creates new node pointer and allocats space for node2 -- [node2] --> [Val][node pointer]

// use access notation to access the word variable
strcpy(node1 ->word, "hello");
//[node1] --> ["hello"][node pointer]
strcpy(node2 ->word, "world");
//[node2] --> ["wolrd"][node pointer]

//access variable by pointing to the value of the next node
node1 ->next = node2 // now there is arrow pointing from node 1 to value in node 2


// how to populate hashtable
//while loop searches through dict (file here), look for a string, then put string into variabel called word


while (fscanf(file, "%s", word) != EOF)
{

    // for every word scanned, Malloc a node*
    node *new_node == malloc(sizeof(node));
    //check if malloc succedeed
    if (new_node == NULL)
    {

        unload(); // unload dict
        return false;

    }
    //if maloc succeeds, then copy new word into next node
    strcpy(new_node ->word, word);

    // how to insert into linked list
    // new node inserted into the begingin
    //so new node shoudl point to whatever was previosu first vlaue in list
    //so point new_node to whatever value head (first node pointer) was pointing to

    new_node ->next = head

    //now can reassigne what head pointer to new_node
    head = new_node;

    //how to know which word to put into which list: use hash function

    //new_node-> word has the word from the dict
    //hasing new_node word will giv eus the index of bucket in the hash table
    //insert tio the linked list


}


// check walkthrough
//case insensitive
//if the word exists, it can be foudn in the has table
//whch bucket woudl the word be in?
hashtable[hash(word)];
//search in the linked list using
strcasecmp

node *head = malloc(sizeof(node));


node *cursor = head; // assign new_node cursor to head

//so how traverse linked list?

node *cursor = head;
while (cursor !=NULL)
{
    // in this code i created a cursor which points to the value that head is pointing to
    //loop will continue as long as cursor doesnt reach NULL
    //do something
    cursor = cursor->next // reassign cursor to wtvr previosu node was poitnintg to
}

//unload walk through

node* cursor = head

while (cursor ! NULL) //
{

    node *temp = cursor;
    cursor = cursor ->next;
    free(temp);

}