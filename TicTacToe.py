import os
import string
import sys
import random
from time import sleep

#definitions



a = ["7", "8", "9"]
b = ["4", "5", "6"]
c = ["1", "2", "3"]
sep1 = " "
sep = "   "
state = 0 # (state of the game) value of put(xo) for users
aistate = 0 # (state of the game) value of AI_put(xo) for CPU, singleplayer mode

def ask_player(xo):
    while True:
        try:
            num = int(input("Player " + xo + " use numerical keyboard as coordinates: "))
            break
        except ValueError:
            print("Please make sure to enter a number")
    return num

def schema():
    schema =  "Schema of numerical keyboard \n"+ sep1.join(a) +"\n"+ sep1.join(b) +"\n"+ sep1.join(c) +"\n"
    return schema

fields = ["-"] *9 #List  of fields

def refresh_board():
    os.system('clear') # clearing terminal
    board = "\n"+ sep.join(fields[6:9]) +"\n\n"+ sep.join(fields[3:6]) +"\n\n"+ sep.join(fields[0:3]) +"\n"
    return board

def put(xo, num): # Function of putting "X" or "O" by users
    if fields[num-1] == "-":
        fields[num-1] = xo
        if fields.count("-") == 0:
            print(refresh_board())
            print("\nDRAW!\n")
            return 2
        elif (fields[0:3].count(xo) == 3 or fields[3:6].count(xo) == 3 or fields[6:9].count(xo) == 3
        or (fields[0].count(xo) + fields[3].count(xo) + fields[6].count(xo) == 3)
        or (fields[1].count(xo) + fields[4].count(xo) + fields[7].count(xo) == 3)
        or (fields[2].count(xo) + fields[5].count(xo) + fields[8].count(xo) == 3)
        or (fields[2].count(xo) + fields[4].count(xo) + fields[6].count(xo) == 3)
        or (fields[0].count(xo) + fields[4].count(xo) + fields[8].count(xo) == 3)):
            print(refresh_board())
            print("User " + xo + " won!")
            return 2
        print(refresh_board())
        return 0
    else:
        print("Choose another location!\n ")
        return 1

def AI_put(xo): # Function of putting "X" or "O" by computer
    if fields.count(xo) == 0:
        target = 4
        if fields[target] != "-":
            target = random.choice([0,2,6,8])

    elif fields.count(xo) == 1:
        i = fields.index(xo)
        if i == 4:
            target = random.choice([0,2,6,8])
            while fields[target] != "-":
                target = random.choice([0,2,6,8])
        else:
            target = i + random.choice([-2,-1,1,2])
            while fields[target] != "-":
                target = i + random.choice([-2,-1,1,2])
    else:
        target = random.choice([0,1,2,3,4,5,6,7,8])
        while fields[target] != "-":
            target = random.choice([0,1,2,3,4,5,6,7,8])

    fields[target] = xo
    if (fields[0:3].count(xo) == 3 or fields[3:6].count(xo) == 3 or fields[6:9].count(xo) == 3
    or (fields[0:7:3].count(xo) == 3)
    or (fields[1:8:3].count(xo) == 3)
    or (fields[2:9:3].count(xo) == 3)
    or (fields[2:5:2].count(xo) == 3)
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

################## multiplayer:

def multiplayer():
    state = 0
    print(schema())
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

################## Singleplayer mode VS Computer:

def singleplayer():
    state = 0
    aistate = 0
    while True:
        while True:
            try:
                menu2 = int(input("Do you want to be a first or second player? (1 or 2): "))
                break
            except ValueError:
                print("PLease make sure to enter a number! 1 to start first, 2 to start second")
        if  menu2 == 1: # User starts as first
            print(schema())
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

        elif menu2 == 2: # Computer starts as first
            print(schema())
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

##################  Main Code  #########################################
while True:
    menu1 = (input("Press 'm' to choose Multiplayer (2 players) or \n 's' for Singleplayer (vs computer) or 'e' to close game: ")).lower()
    if  menu1 == "m":
        multiplayer()
        break
    elif menu1 == "s":
        singleplayer()
        break
    elif menu1 == "e":
        sys.exit()
    else:
        print("Make sure to enter 'm' for Multiplayer, 's' for Singleplayer, 'e' to exit ")
######## closing game #######
