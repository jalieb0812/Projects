from cs50 import get_float

def cash():

    coin_counter = 0
    quarter = .25
    dime = .10
    nickel = .05
    penny = 0.01
    while True:
        change = get_float("Change owed: ")
        if change >= 0:
            break

    while change >= 0.25:

        change = change - 0.25
        coin_counter = coin_counter + 1

    while change  >= 0.10:

        change = change - 0.10
        coin_counter = coin_counter + 1

    while change >= .05:

        change = change - 0.05
        coin_counter = coin_counter + 1

    while change > .01:

        change = change - 0.01
        coin_counter = coin_counter + 1



    print(coin_counter)
    print()

cash()








    # return minimum number of coin