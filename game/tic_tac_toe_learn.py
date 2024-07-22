import numpy as np

BOARD_ROWS = 3
BOARD_COLS = 3
end = False
board = np.zeros((BOARD_ROWS, BOARD_COLS))
state1 = []
state2 = []
reward = np.zeros(19683)
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
    
def backprop():
    winner = win()

    if winner == 1:
        curr = 1
        for i in reversed(state1):
            reward[i] += 0.2 * (0.9 * curr - reward[i])
            curr = reward[i] 
        
        curr = -0.1
        for i in reversed(state2):
            reward[i] += 0.2 * (0.9 * curr - reward[i])
            curr = reward[i] 
            
    if winner == -1:
        curr = -0.1
        for i in reversed(state1):
            reward[i] += 0.2 * (0.9 * curr - reward[i])
            curr = reward[i] 
            
        curr = 1
        for i in reversed(state2):
            reward[i] += 0.2 * (0.9 * curr - reward[i])
            curr = reward[i] 
            
    if winner == 0:
        curr = 0.5
        for i in reversed(state1):
            reward[i] += 0.2 * (0.9 * curr - reward[i])
            curr = reward[i] 
        
        curr = 0.5
        for i in reversed(state2):
            reward[i] += 0.2 * (0.9 * curr - reward[i])
            curr = reward[i] 

def comp_learn():
    present = available()
    if len(present) == 0:
        return
    global board
    
    if np.random.uniform(0, 1) <= 0.3:
        i = np.random.choice(len(present))
        board[present[i]] = player
        if player == 1:
            state1.append(get_hash(board))
        if player == -1:
            state2.append(get_hash(board))
        return
        
    next_state = []
    for i in range(0, len(present)):
        curr_state = np.copy(board)
        curr_state[present[i]] = player
        next_state.append(curr_state)

    max_state = None
    max_reward = -9999
    
    for i in next_state:
        curr_reward = reward[get_hash(i)]
        if max_reward < curr_reward:
            max_reward = curr_reward
            max_state = i
            
    # if max_reward < 0:
    #     i = np.random.choice(len(present))
    #     board[present[i]] = player
    #     if player == 1:
    #         state1.append(get_hash(board))
    #     if player == -1:
    #         state2.append(get_hash(board))
    #     return
    
    board = np.copy(max_state)
    if player == 1:
        state1.append(get_hash(board))
    if player == -1:
        state2.append(get_hash(board))
        
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
    
    file = open('reward1.txt', 'r')
    arr = []
    for i in file:
        i = i.strip()
        arr.append(float(i))
    file.close()
    
    for i in next_state:
        # curr_reward = reward[get_hash(i)]
        curr_reward = arr[get_hash(i)]
        if max_reward < curr_reward:
            max_reward = curr_reward
            max_state = i
            
    # if max_reward == 0:
    #     i = np.random.choice(len(present))
    #     board[present[i]] = player
    #     # if player == 1:
    #     #     state1.append(get_hash(board))
    #     # if player == -1:
    #     #     state2.append(get_hash(board))
    #     return
    
    board = np.copy(max_state)
    # if player == 1:
    #     state1.append(get_hash(board))
    # if player == -1:
    #     state2.append(get_hash(board))
        
def p1():
    present = available()
    if len(present) == 0:
        return
    i = np.random.choice(len(present))
    board[present[i]] = 1   
    
def p2():
    present = available()
    if len(present) == 0:
        return
    i = np.random.choice(len(present))
    board[present[i]] = -1

def reset():
    global board, state1, state2, end, player
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    state1 = []
    state2 = []
    end = False
    player = 1

def human():
    present = available()
    i = int(input())
    if board[int((i - 1)/3)][int((i - 1) % 3)] == 0:
        board[int((i - 1)/3)][int((i - 1) % 3)] = -1
    
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
    print()

def train():
    global player
    # Training 1 with random
    for i in range(0, 10000):
        if(i % 10000 == 0):
            print("training: {}".format(i))
        while (win() == None):
            comp_learn()
            if (win() == None):
                p2()
        backprop()
        reset()
    
    # Training 2 with random    
    for i in range(0, 10000):
        player = -1
        if(i % 10000 == 0):
            print("training: {}".format(i))
        while (win() == None):
            p1()
            if (win() == None):
                comp_learn()
        backprop()
        reset()
    
    # Training with self
    for i in range(0, 10000):
        if(i % 10000 == 0):
            print("training: {}".format(i))
        while end is False:
            comp_learn()
            player = -1 * player
        backprop()
        reset()
    
    # Training 1 with random    
    for i in range(0, 10000):
        if(i % 10000 == 0):
            print("training: {}".format(i))
        while (win() == None):
            comp_learn()
            if (win() == None):
                p2()
        backprop()
        reset()
    
def store(file):
    for i in reward:
        file.write(str(i))
        file.write("\n")
    file.close()

def testing():
    # Test with learn
    one = 0
    two = 0
    t = 0
    for i in range(0, 10000):
        while (win() == None):
            comp_learn()
            if (win() == None):
                p2()
        if(win() == 1):
            one += 1
        if(win() == -1):
            two += 1
        t += 1
        reset()
    print("{} {} {} {}".format(one, two, t - one - two, t))
    
    #Test with play
    one = 0
    two = 0
    t = 0
    for i in range(0, 10000):
        # if(i%100 == 0):
            # print(i)
        while (win() == None):
            comp_play()
            if (win() == None):
                p2()
        if(win() == 1):
            one += 1
        if(win() == -1):
            two += 1
        t += 1
        reset()
    print("{} {} {} {}".format(one, two, t - one - two, t))

    #Random Test
    first = 0
    second = 0
    total = 0
    # player = -1
    for i in range(0, 10000):
        while (win() == None):
            p1()
            if (win() == None):
                p2()
        if(win() == 1):
            first += 1
        if(win() == -1):
            second += 1
        total += 1
        reset()
    print("{} {} {} {}".format(first, second, total - first - second, total))

if __name__ == "__main__":

    # train()        
    # # write in file
    # file = open("reward.txt", "w")
    # store(file)
    # testing()
    
    while (win() == None):
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