from cs50 import get_string

def get_name():
    name = get_string("What is your name?: ")
    print("hello,", name)


get_name()