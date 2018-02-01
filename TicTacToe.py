import os
import string
import sys
import random
from time import sleep

# definitions


def clear(): return os.system('clear')


a = ["7", "8", "9"]
b = ["4", "5", "6"]
c = ["1", "2", "3"]

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

sep = "   "


def refresh_board():
    clear()  # clearing terminal
    board = ("\n" + sep.join(fields[6:9]) + "\n\n" +
             sep.join(fields[3:6]) + "\n\n" +
             sep.join(fields[0:3]) + "\n")
    return board


def schema():
    schema = ("Schema of numerical keyboard \n" +
              sep.join(a) + "\n\n" +
              sep.join(b) + "\n\n" +
              sep.join(c) + "\n")
    return schema


def ask_player(xo):
    while True:
        try:
            num = int(
                input(
                    "Player " +
                    xo +
                    " use numerical keyboard as coordinates: "))
            break
        except ValueError:
            print("Please make sure to enter a number")
    return num


def put(xo, num):  # Function of putting "X" or "O" by users
    if fields[num - 1] == "-":
        fields[num - 1] = xo
        if fields.count("-") == 0:
            print(refresh_board())
            print("\nDRAW!\n")
            return 2
        elif (fields[0:3].count(xo) == 3
              or fields[3:6].count(xo) == 3
              or fields[6:9].count(xo) == 3
              or (fields[0:7:3].count(xo) == 3)
              or (fields[1:8:3].count(xo) == 3)
              or (fields[2:9:3].count(xo) == 3)
              or (fields[2:7:2].count(xo) == 3)
              or (fields[0:9:4].count(xo) == 3)):
            print(refresh_board())
            print("User " + xo + " won!\n")
            return 2
        print(refresh_board())
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


def target_f(keyfields, fields, xo):

    for [start, stop, step] in keyfields:
        f = check_attack_fields(start, stop, step, fields, xo)
        if f > -1:
            '''print('attack')'''
            return f

    for [start, stop, step] in keyfields:
        f = check_defend_fields(start, stop, step, fields, xo)
        if f > -1:
            '''print('defend')'''
            return f

    for [start, stop, step] in keyfields:
        f = check_balanced_fields(start, stop, step, fields, xo)
        if f > -1:
            '''print('balanced tactic')'''
            return f

    if f == -1:
        print('wrong algorithm')
        sys.exit


def AI_put(xo):  # Function of putting "X" or "O" by computer
    if fields.count(xo) == 0:  # if there is no AI symbols on board
        target = 4  # target = index of field
        if fields[target] != "-":
            target = random.choice([0, 2, 6, 8])
        print(str(target) + ' for 0')

    else:  # if there are more than 1 AI symbols on board
        target = target_f(keyfields, fields, xo)
        print(str(target) + ' for else')

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
        print(refresh_board())
        print("User " + xo + " won!")
        return 2
    elif fields.count("-") == 0:
        print(refresh_board())
        print("\nDRAW!\n")
        return 2
    else:
        print(refresh_board())
        return 0

# multiplayer:


def multiplayer():
    state = 0
    print(refresh_board())
    while state != 2:
        num = ask_player('X')
        state = put('X', num)
        if state == 2:
            break

        while state == 1:
            num = ask_player('X')
            state = put('X', num)
            if state == 2:
                break

        num = ask_player('O')
        state = put("O", num)
        if state == 2:
            break

        while state == 1:
            num = ask_player('O')
            state = put("O", num)
            if state == 2:
                break

# Singleplayer mode VS Computer:


def singleplayer():
    state = 0
    aistate = 0
    while True:
        while True:
            try:
                menu2 = int(
                    input("Do you want to be a first or second player? (1 or 2): "))
                break
            except ValueError:
                print(
                    "PLease make sure to enter a number! 1 to start first, 2 to start second")
        if menu2 == 1:  # User starts as first
            print(refresh_board())
            while state != 2:
                # User moves:
                num = ask_player('X')
                state = put("X", num)
                if state == 2:
                    break

                while state == 1:
                    num = ask_player('X')
                    state = put("X", num)
                    if state == 2:
                        break

                # Computer moves:
                sleep(2)
                aistate = AI_put("O")
                if aistate == 2:
                    break

        elif menu2 == 2:  # Computer starts as first
            print(refresh_board())
            while state != 2 or aistate != 2:
                # Computer moves:
                sleep(2)
                aistate = AI_put("X")
                if aistate == 2:
                    break

                # User moves:
                num = ask_player('O')
                state = put("O", num)
                if state == 2:
                    break

                while state == 1:
                    num = ask_player('O')
                    state = put("O", num)
                    if state == 2:
                        break

        else:
            print("Please enter 1 to play first and 2 to play second")
        break


##############################  Main Code  ###############################

while True:

    print(schema())

    menu1 = (
        input(
            "Press 'm' to choose Multiplayer (2 players) "
            "or \n 's' for Singleplayer (vs computer) or 'e' to close game: ")).lower()

    # choosing the game mode:
    if menu1 == "m":
        multiplayer()
        break
    elif menu1 == "s":
        singleplayer()
        break
    elif menu1 == "e":
        sys.exit()  # closing game
    else:
        print("Make sure to enter 'm' for Multiplayer, 's' for Singleplayer, 'e' to exit ")
