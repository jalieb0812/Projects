from cs50 import get_string, get_int
# mario by jordan lieber


def Mario():

    while True:
        number = 0
        counter = 0

        number = get_int("Height: ")
        if number >= 1 and number <= 8:
            break

    num_counter = number
    while number > counter:

        for i in range(1):
            print(" " * (num_counter - 1), end="")
        for j in range(counter + 1):
            print("#", end="")
        print()

        counter = counter + 1
        num_counter = num_counter - 1



Mario()