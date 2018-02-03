import os
import string
import sys
import random
from time import sleep

# definitions


def clear(): return os.system('clear')


def red(name):
    print ("\033[91m {}\033[00m" .format(name))


def yellow(name):
    print ("\033[93m {}\033[0m" .format(name))


def menu():
    red("          ||||||||      ||       |||||||")
    red("             ||         ||       ||       ")
    red("             ||         ||       ||       ")
    red("             ||         ||       |||||||\n")
    red("          ||||||||    |||||||    |||||||")
    red("             ||       ||   ||    ||       ")
    red("             ||       |||||||    ||       ")
    red("             ||       ||   ||    ||||||| \n")
    red("          ||||||||    |||||||    |||||||")
    red("             ||       ||   ||    ||--- ")
    red("             ||       ||   ||    ||--- ")
    red("             ||       |||||||    |||||||\n")
    yellow("          Welcome to the Tic Tac Toe game!\n          Please select one of the following:")
    yellow("         'M' for Multiplayer (2 players)\n          'S' for Singleplayer (vs AI)\n          'R' for rules\n          'E' to exit")


def rules():
    print("The goal is to get 3 symbols in a row.\n" 
    "Each person must switch taking turns, first X, then O.\n" 
    "Players must use the board given to them,\n" 
    "they cannot add extra sides on to the board.\n"
    "In order to win, the 3 letters must all connect\n"
    "in a straight line in one direction, up or down, \nleft or right, or diagonally.")


state = 0  # (state of the game) value of put(xo) for users
aistate = 0  # (state of the game) value of AI_put(xo) for CPU, singleplayer mode

fields = ["-"] * 9  # List  of fields

# keyfields should have been interpreted as cut list of fields like
# fields [start, stop, step] :
keyfields = [[2, 7, 2],
             [0, 9, 4],
             [0, 7, 3],
             [1, 8, 3],
             [2, 9, 3],
             [6, 9, 1],
             [3, 6, 1],
             [0, 3, 1]]

sep = "        "


def refresh_board(fields):
    clear()  # clearing terminal
    board = ("\n\n" + sep*2 + sep.join(fields[6:9]) + "\n\n\n\n" +
                      sep*2 + sep.join(fields[3:6]) + "\n\n\n\n" +
                      sep*2 + sep.join(fields[0:3]) + "\n\n")
    return board


def ask_player(xo):
    while True:
        try:
            num = int(input(
                            "   Player " + xo +
                            " use numerical keyboard as coordinates:\n "
                            + sep*3))
            break
        except ValueError:
            print("Please make sure to enter a number")
    return num


def put(xo, num, fields):  # Function of putting "X" or "O" by users
    if fields[num - 1] == "-":
        fields[num - 1] = xo
        if fields.count("-") == 0:
            print(refresh_board(fields))
            print("/n                       DRAW!\n")
            return 2
        elif (fields[0:3].count(xo) == 3
              or fields[3:6].count(xo) == 3
              or fields[6:9].count(xo) == 3
              or (fields[0:7:3].count(xo) == 3)
              or (fields[1:8:3].count(xo) == 3)
              or (fields[2:9:3].count(xo) == 3)
              or (fields[2:7:2].count(xo) == 3)
              or (fields[0:9:4].count(xo) == 3)):
            print(refresh_board(fields))
            print("                   User " + xo + " won!\n")
            return 2
        print(refresh_board(fields))
        return 0
    else:
        print("Choose another location!\n ")
        return 1


def check_attack_fields(start, stop, step, fields, xo):
    if fields[start:stop:step].count('-') == 1:
        if fields[start:stop:step].count(xo) == 2:
            if fields[start] == '-':
                return start
            if fields[start + step] == '-':
                return start + step
            if fields[stop - 1] == '-':
                return stop - 1
        return -1
    return -1


def check_defend_fields(start, stop, step, fields, xo):
    if fields[start:stop:step].count('-') == 1:
        if fields[start:stop:step].count(xo) == 0:
            if fields[start] == '-':
                return start
            if fields[start + step] == '-':
                return start + step
            if fields[stop - 1] == '-':
                return stop - 1
        return -1
    return -1


def check_balanced_fields(start, stop, step, fields, xo):
    if fields[start:stop:step].count('-') == 2:
        if fields[start:stop:step].count(xo) == 1:
            if fields[start] == '-':
                return start
            if fields[start + step] == '-':
                return start + step
            if fields[stop - 1] == '-':
                return stop - 1
        return -1
    return -1


def check_else_fields(start, stop, step, fields, xo):
    if fields[start:stop:step].count('-') >= 1:
        if fields[start:stop:step].count(xo) >= 1:
            if fields[start] == '-':
                return start
            if fields[start + step] == '-':
                return start + step
            if fields[stop - 1] == '-':
                return stop - 1
        return -1
    return -1


def target_f(keyfields, fields, xo):

    for [start, stop, step] in keyfields:
        f = check_attack_fields(start, stop, step, fields, xo)
        if f > -1:
            '''attack'''
            return f

    for [start, stop, step] in keyfields:
        f = check_defend_fields(start, stop, step, fields, xo)
        if f > -1:
            '''defend'''
            return f

    for [start, stop, step] in keyfields:
        f = check_balanced_fields(start, stop, step, fields, xo)
        if f > -1:
            '''balanced tactic'''
            return f

    for [start, stop, step] in keyfields:
        f = check_else_fields(start, stop, step, fields, xo)
        if f > -1:
            '''tactic for else cases'''
            return f

    if f == -1:
        f = random.randrange(0,9)
        print('error of game')
        return sys.exit


def AI_put(xo, level, fields):  # Function of putting "X" or "O" by computer

    if fields.count(xo) == 0:  # if there is no AI symbols on board
        if level == 'y':  # if hard level is choosen
            target = 4  # target = index of field
            while fields[target] != "-":
                target = random.choice([0, 2, 6, 8])
        else:  # lower level
            target = random.randrange(1, 9, 2)
            while fields[target] != "-":
                target = random.randrange(1, 9, 2)

    else:  # if there are more than 1 AI symbols on board
        target = target_f(keyfields, fields, xo)

    fields[target] = xo  # put symbol into index - target

    # checking if the victory occured:
    if (fields[0:3].count(xo) == 3
        or fields[3:6].count(xo) == 3
        or fields[6:9].count(xo) == 3
        or (fields[0:7:3].count(xo) == 3)
        or (fields[1:8:3].count(xo) == 3)
        or (fields[2:9:3].count(xo) == 3)
        or (fields[2:7:2].count(xo) == 3)
            or (fields[0:9:4].count(xo) == 3)):
        print(refresh_board(fields))
        print("                  User " + xo + " won!")
        return 2
    elif fields.count("-") == 0:
        print(refresh_board(fields))
        print("\n                       DRAW!\n")
        return 2
    else:
        print(refresh_board(fields))
        return 0

# multiplayer:


def multiplayer():
    state = 0
    print(refresh_board(fields))
    while state != 2:
        num = ask_player('X')
        state = put('X', num, fields)
        if state == 2:
            break

        while state == 1:
            num = ask_player('X')
            state = put('X', num, fields)
            if state == 2:
                break

        num = ask_player('O')
        state = put("O", num, fields)
        if state == 2:
            break

        while state == 1:
            num = ask_player('O')
            state = put("O", num, fields)
            if state == 2:
                break

# Singleplayer mode VS Computer:


def singleplayer(level):
    state = 0
    aistate = 0
    while True:
        while True:
            try:
                menu2 = int(
                    input("      Do you want to be a first or second player? (1 or 2): "))
                break
            except ValueError:
                print(
                    "      PLease make sure to enter a number! 1 to start first, 2 to start second")
        if menu2 == 1:  # User starts as first
            print(refresh_board(fields))
            while state != 2:
                # User moves:
                num = ask_player('X')
                state = put("X", num, fields)
                if state == 2:
                    break

                while state == 1:
                    num = ask_player('X')
                    state = put("X", num, fields)
                    if state == 2:
                        break

                # Computer moves:
                sleep(2)
                aistate = AI_put("O", level, fields)
                if aistate == 2:
                    break

        elif menu2 == 2:  # Computer starts as first
            print(refresh_board(fields))
            while state != 2 or aistate != 2:
                # Computer moves:
                sleep(2)
                aistate = AI_put("X", level, fields)
                if aistate == 2:
                    break

                # User moves:
                num = ask_player('O')
                state = put("O", num, fields)
                if state == 2:
                    break

                while state == 1:
                    num = ask_player('O')
                    state = put("O", num, fields)
                    if state == 2:
                        break

        else:
            print("        Please enter 1 to play first and 2 to play second")
        break

##############################  Main Code  ###############################


clear()
menu()
while True:

    choice = (input()).lower()

    # choosing the game mode:
    if choice == "m":  # multiplayer choosen
        multiplayer()
        break

    elif choice == "s":  # singleplayer choosen
        print('      Do you want to play on the hard level or not? ')
        while True:  # choosing the level
            level = input('      Enter y or n\n').lower()
            if level == 'y' or level == 'n':
                break
        singleplayer(level)
        break

    elif choice == "r":  # show rules
        rules()

    elif choice == "e":  # closing game
        sys.exit()  
    else:
        print("      Make sure to enter 'm' for Multiplayer, 's' for Singleplayer, 'e' to exit ")
