from cs50 import get_string
#program that gets your name and says hello

def get_name():
    name = get_string("What is your name?: ")
    print("hello,", name)


get_name()