import numpy as np

ele=[]
for i in range (10):
    ele.append(i)
ele[0]='-'      #We do not use this
turn = 'X'

def print_board():

    for i in range (3):
        for j in range (1,4):
            print(f" {ele[i*3+j]} | ",end="")
        print()

print_board()

def check_winner():
    for i in range (3):
        if(ele[i*3+1]==ele[i*3+2]==ele[i*3+3]):
            print(f'{ele[i*3+1]} won ')
            return True
    for i in range (1,4):
        if(ele[i]==ele[i+3]==ele[i+6]):
            print(f'{ele[i]} won ')
            return True
    if(ele[1]==ele[5]==ele[9]):
        print(f'{ele[1]} won ')
        return True
    if(ele[3]==ele[5]==ele[7]):
        print(f'{ele[3]} won ')
        return True
    if any(isinstance(i, (int)) for i in ele)!=True:        #All squares taken with no result
        print("The game is a tie")
        return True

def game(turn):
    while check_winner() != True:
        choice = int(input(f"Choose the square number for {turn}: "))
        if np.isreal( ele[choice]):
            ele[choice] = turn
        else:
            print("The square is already taken")
            game(turn)
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'
        print_board()

game(turn)