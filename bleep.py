from cs50 import get_string
from sys import argv
import sys



def main():

    # TODO
    if len(sys.argv) != 2:
        sys.exit("Usage: must have 2 command-line arguments")

    # Determine dictionary to use
    words = sys.argv[1]

    banned_words = set()


    loaded = load(words)
    # Exit if set not loaded
    if not loaded:
        print(f"Could not load {banned_words}.")
        sys.exit(1)

    #for line in loaded:
        #print(line)
    #print(loaded)

    message = get_string("message: ")

    message_list = message.split()

    #print(message_list)

    message_set = set()


    for line in message_list:
        message_set.add(line.strip('\n'))

    #print(message_set)

    for line in message_list:
        word = ""


        if line.lower() not in loaded:
            print(line, "", end = "")

        else:
            for letter in line:
                letter = "*"
                word = word + letter
            print(word, "", end = "")
    print()




#def check(word):
    """Return true if word is in dictionary else false"""
   #return word.lower() in words

def load(words):
    """Load dictionary into memory, returning true if successful else false"""
    word_list = set()
    file = open(words, "r")
    for line in file:
        word_list.add(line.rstrip("\n"))
    file.close()
    return word_list

# open and read file from list of words and store them, one per a line, in a set
if __name__ == "__main__":
    main()


