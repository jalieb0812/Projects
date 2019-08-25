from sys import argv
import sys

from cs50 import get_string, get_int



#accept single command line argument(k) (no need to cehck if arguement is indeed numeric)
#if no comand line argyuments or or than 1, then print erro mesage and exit with return of 1
#prompt for "plaintext:" nand get a string
#output cypher text plus cypher text rotateed; non-alphbetical charachters remain unchagned. preserve case
# print noew line after cyoher text
#Given a string representing one Unicode character, return an integer representing the Unicode code point of that character.
#For example, ord('a') returns the integer 97 and ord('€') (Euro sign) returns 8364. This is the inverse of chr()

def caesar():
    if len(sys.argv) != 2:
        sys.exit("Usage: must have 2 command-line arguments")

    k = int(argv[1]) # the key turned into an int


    #if k > 26:
        #k = (26 +k) % 26


    plain_text = get_string("plain_text: ")
    cypher_text = ""
    c_letter = ""
    c_letter_num = 0

    #ord() turns letter to unicode; chr() turs unicode to letter; ci = (pi + k) % 26; A = 65, a = 97
    for p_letter in plain_text:

        p_letter_num = ord(p_letter)# turn p_lertter into int

        # wrap around key if key plus p_letter_num is greater than 26
        if (k + p_letter_num) > 26:
            k = (26 + k) % 26
        #check if not  letter:
        if p_letter.isalpha() == False:
            #if not a letter, then p_letter = c_letter
            c_letter = p_letter
            #append C_letter to cypher_word
            cypher_text = cypher_text + c_letter
        #check if letter:
        if p_letter.isalpha() == True:
            # turn letter to unicode ord(p_letter)
            p_letter_num = ord(p_letter)
            #then add key to  p_letter to get C_letter
            c_letter_num = p_letter_num + k
            if p_letter.islower() == True: # if lower case letter then use this formula to wrap arround
                if c_letter_num > 122:
                    c_letter_num = c_letter_num - 26
            else:
                if c_letter_num > 90:
                    c_letter_num = c_letter_num - 26


            #then turn c_letter back to  letter using chr()
            c_letter = chr(c_letter_num)
            #append c_letter to cypher_word
            cypher_text = cypher_text + c_letter


    print("cyphertext: ", cypher_text)

caesar()