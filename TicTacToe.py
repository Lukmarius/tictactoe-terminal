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

fields = ["-"] *9 #List  of fields

def refresh_board():
    #os.system('clear') # clearing terminal
    board = "\n"+ sep.join(fields[6:9]) +"\n\n"+ sep.join(fields[3:6]) +"\n\n"+ sep.join(fields[0:3]) +"\n"
    return board

def schema():
    schema =  "Schema of numerical keyboard \n"+ sep1.join(a) +"\n"+ sep1.join(b) +"\n"+ sep1.join(c) +"\n"
    return schema

def ask_player(xo):
    while True:
        try:
            num = int(input("Player " + xo + " use numerical keyboard as coordinates: "))
            break
        except ValueError:
            print("Please make sure to enter a number")
    return num

def put(xo, num): # Function of putting "X" or "O" by users
    if fields[num-1] == "-":
        fields[num-1] = xo
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
            print("User " + xo + " won!")
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
            if fields[stop-1] == '-':
                return stop - 1
        return -1
    return -1

def check_defend_fields(start, stop, step, fields, xo):
    if fields[start:stop:step].count('-') == 1: 
        if fields[start] == '-':
            return start
        if fields[start + step] == '-':
            return start + step
        if fields[stop - 1] == '-':
            return stop - 1
    return -1

def target_f(fields, xo):
    f = check_attack_fields(2, 7, 2, fields, xo)
    if check_attack_fields(2, 7, 2, fields, xo) > -1:
        print(check_attack_fields(2, 7, 2, fields, xo))
        return check_attack_fields(2, 7, 2, fields, xo)

    elif check_attack_fields(0, 9, 4, fields, xo) > -1:
        print(check_attack_fields(0, 9, 4, fields, xo))
        return check_attack_fields(0, 9, 4, fields, xo)

    elif check_attack_fields(0, 7, 3, fields, xo) > -1:
        print(check_attack_fields(0, 7, 3, fields, xo))
        return check_attack_fields(0, 7, 3)

    elif check_attack_fields(1, 8, 3, fields, xo) > -1:
        print(check_attack_fields(1, 8, 3, fields, xo))
        return check_attack_fields(1, 8, 3, fields, xo)

    elif check_attack_fields(2, 9, 3, fields, xo) > -1:
        print(check_attack_fields(2, 9, 3, fields, xo))
        return check_attack_fields(2, 9, 3, fields, xo)

    elif check_attack_fields(6, 9, 1, fields, xo) > -1:
        print(check_attack_fields(6, 9, 1, fields, xo))
        return check_attack_fields(6, 9, 1, fields, xo)

    elif check_attack_fields(3, 6, 1, fields, xo) > -1:
        print(check_attack_fields(3, 6, 1, fields, xo))
        return check_attack_fields(3, 6, 1, fields, xo)

    elif check_attack_fields(0, 3, 1, fields, xo) > -1:
        print(check_attack_fields(0, 3, 1, fields, xo))
        return check_attack_fields(0, 3, 1, fields, xo)
        
    # for defending tactic if win is not possible:
    elif check_defend_fields(2, 7, 2, fields, xo) > -1:
        print(check_defend_fields(2, 7, 2, fields, xo))
        return check_attack_fields(2, 7, 2, fields, xo)

    elif check_defend_fields(0, 9, 4, fields, xo) > -1:
        print(check_defend_fields(0, 9, 4, fields, xo))
        return check_attack_fields(0, 9, 4, fields, xo)

    elif check_defend_fields(0, 7, 3, fields, xo) > -1:
        print(check_defend_fields(0, 7, 3, fields, xo))
        return check_attack_fields(0, 7, 3, fields, xo)

    elif check_defend_fields(1, 8, 3, fields, xo) > -1:
        print(check_defend_fields(1, 8, 3, fields, xo))
        return check_attack_fields(1, 8, 3, fields, xo)

    elif check_defend_fields(2, 9, 3, fields, xo) > -1:
        print(check_defend_fields(2, 9, 3, fields, xo))
        return check_attack_fields(2, 9, 3, fields, xo)

    elif check_defend_fields(6, 9, 1, fields, xo) > -1:
        print(check_defend_fields(6, 9, 1, fields, xo))
        return check_attack_fields(6, 9, 1, fields, xo)

    elif check_defend_fields(3, 6, 1, fields, xo) > -1:
        print(check_defend_fields(3, 6, 1, fields, xo))
        return check_attack_fields(3, 6, 1, fields, xo)

    elif check_defend_fields(0, 3, 1, fields, xo) > -1:
        print(check_defend_fields(0, 3, 1, fields, xo))
        return check_attack_fields(0, 3, 1, fields, xo)

    else: # ostateczność
        print('target_f else: ')
        target = random.randrange(0,9)
        while fields[target] != "-":
            target = random.randrange(0,9)
        return target
    


def AI_put(xo): # Function of putting "X" or "O" by computer
    if fields.count(xo) == 0:  # if there is no AI symbols on board
        target = 4
        if fields[target] != "-":
            target = random.choice([0, 2, 6, 8])
        print(str(target) + ' for 0')

    elif fields.count(xo) == 1:  # if there is 1 AI symbol on board
        target = random.choice([0, 2, 6, 8])
        while fields[target] != "-":
            target = random.choice([0, 2, 6, 8])
        print(str(target) + ' for 1')

    else:
        target = target_f(fields, xo)
        print(str(target) + ' for else')

    
    fields[target] = xo # put symbol into index - target

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
        break

##############################  Main Code  #######################################

while True:
    menu1 = (input("Press 'm' to choose Multiplayer (2 players) or \n 's' for Singleplayer (vs computer) or 'e' to close game: ")).lower()
    if  menu1 == "m":
        multiplayer()
        break
    elif menu1 == "s":
        singleplayer()
        break
    elif menu1 == "e":
        sys.exit()  # closing game
    else:
        print("Make sure to enter 'm' for Multiplayer, 's' for Singleplayer, 'e' to exit ")