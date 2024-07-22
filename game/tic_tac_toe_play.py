import numpy as np
import os

BOARD_ROWS = 3
BOARD_COLS = 3
end = False
board = np.zeros((BOARD_ROWS, BOARD_COLS))
player = 1

def win():
    end = True
    #checking rows
    for i in range(0, BOARD_ROWS):
        if sum(board[i, :]) == 3:
            return 1
        
        if sum(board[i, :]) == -3:
            return -1
           
    #checking collumns 
    for i in range(0, BOARD_COLS):
        if sum(board[:, i]) == 3:
            return 1
        
        if sum(board[:, i]) == -3:
            return -1
        
    #checking diagonals
    if sum([board[i, i] for i in range(0, BOARD_ROWS)]) == 3:
        return 1
    if sum([board[i, i] for i in range(0, BOARD_ROWS)]) == -3:
        return -1
    
    if sum([board[i, BOARD_COLS - i - 1] for i in range(0, BOARD_COLS)]) == 3:
        return 1
    if sum([board[i, BOARD_COLS - i - 1] for i in range(0, BOARD_COLS)]) == -3:
        return -1

    if len(available()) == 0:
        return 0
    
    end = False
    return None

def get_hash(state):
    el = (state + 1).reshape(9)
    t = 0
    k = 1
    
    for i in el:
        t = t + i * k
        k = k * 3
        
    return int(t)
        
def comp_play():
    present = available()
    if len(present) == 0:
        return
    global board, player
        
    next_state = []
    for i in range(0, len(present)):
        curr_state = np.copy(board)
        curr_state[present[i]] = player
        next_state.append(curr_state)

    max_state = None
    max_reward = -9999
    
    file = open("reward1.txt", 'r')
    arr = []
    for i in file:
        i = i.strip()
        arr.append(float(i))
    file.close()
    
    for i in next_state:
        curr_reward = arr[get_hash(i)]
        if max_reward < curr_reward:
            max_reward = curr_reward
            max_state = i
    
    board = np.copy(max_state)

def reset():
    global board, state1, state2, end, player
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    end = False
    player = 1

def human():
    present = available()
    
    while (True):
        i = int(input("Enter your choice: "))
        if board[int((i - 1)/3)][int((i - 1) % 3)] == 0:
            board[int((i - 1)/3)][int((i - 1) % 3)] = -1
            return
        print("Invalid Choice!")

    
def available():
    global end
    present = []
    
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] == 0:
                present.append((i, j))
    
    if len(present) == 0:
        end = True
    return present

def show():
    print()
    for i in range(0, 3):
        str = " "
        for j in range(0, 3):
            if board[i][j] == 0:
                str += "  "
            elif board[i][j] == 1:
                str += "0 "
            else:
                str += "X "
            if(j != 2):
                str += "| "
        print(str)
        if(i!=2):
            print("-----------")


if __name__ == "__main__":
    
    play = 1
    while play == 1:
        reset()
        while (win() == None):
            os.system('cls')
            comp_play()
            show()
            print()
            if (win() == None):
                human()
        
        winner = win()
        if(winner == 1):
            print("Computer Wins!!")
        elif winner == -1:
            print("Human Wins!!")
        else:
            print("Match Draw!!")
        print()
        play = int(input("Play Again? \nPress 1 for yes 0 for No: "))