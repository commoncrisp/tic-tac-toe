import time
import pickle

board = [[0,0,0],
         [0,0,0],
         [0,0,0]]

start = time.time()
def check_win(board):
    for x in range(0, 3):
        if board[0 + x][0] == 1 and board[0 + x][1] == 1 and board[0 + x][2] == 1:
            return 1
        
    for x in range(0, 3):
        if board[0][0 + x] == 1 and board[1][0 + x] == 1 and board[2][0 + x] == 1:
            return 1
        
    if board[0][0] == 1 and board[1][1] == 1 and board[2][2] == 1:
        return 1
    
    if board[0][2] == 1 and board[1][1] == 1 and board[2][0] == 1:
        return 1
    
    for x in range(0, 3):
        if board[0 + x][0] == 2 and board[0 + x][1] == 2 and board[0 + x][2] == 2:
            return 2
        
    for x in range(0, 3):
        if board[0][0 + x] == 2 and board[1][0 + x] == 2 and board[2][0 + x] == 2:
            return 2
        
    if board[0][0] == 2 and board[1][1] == 2 and board[2][2] == 2:
        return 2
    
    if board[0][2] == 2 and board[1][1] == 2 and board[2][0] == 2:
        return 2
            
    for row in board:
        if 0 in row:
            return 0
        
    return 3

def factorial(input):
    output = 1
    for x in range(1, input + 1):
        output *= x
    return output

result_of_moves = []
player_one_moves = []
player_two_moves = []
all_moves = []
def write_file():
    global all_moves
    global result_of_moves
    for x in range(1, 362881): 
        move = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        turn = 0
        board = [[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]]

        available_moves = list(range(9))  

        while check_win(board) == 0 and turn < 9:
        
            move_index = (x // factorial(8 - turn)) % len(available_moves)
            move[turn] = available_moves.pop(move_index)  

            board[int(move[turn] / 3)][move[turn] % 3] = 2 if turn % 2 == 1 else 1
            win = check_win(board)
            turn += 1

        all_moves.append(tuple(move))
        result_of_moves.append(win)
    end = time.time()
    print(end - start)
    with open("all_moves.pkl", "wb") as file:
        pickle.dump(all_moves, file)

    with open("result_of_moves.pkl", "wb") as file:
        pickle.dump(result_of_moves, file)
    
    return all_moves

 # def split_moves_between_players_and_pop():
    global result_of_moves
    global player_one_moves
    global player_two_moves
    all_moves = write_file()
    for x in range (len(all_moves)):
        player_one_moves.append((all_moves[x][0], all_moves[x][2], all_moves[x][4], all_moves[x][6], all_moves[x][8]))
        player_two_moves.append((all_moves[x][1], all_moves[x][3], all_moves[x][5], all_moves[x][7]))

    
    for x in range(len(result_of_moves) - 1, -1, -1):
        if result_of_moves[x] == 1:
            result_of_moves.pop(x)
            player_one_moves.pop(x)
            player_two_moves.pop(x)

def move_to_tie(previous_moves):
    global all_moves
    global result_of_moves
    amount_of_moves = len(previous_moves)

    available_moves = [i for i in range(9) if i not in previous_moves]
    non_losses_for_each_move = [0] * len(available_moves)

    for x in range(0, len(all_moves)):
        has_same_previous_moves = all(
            previous_moves[i] == all_moves[x][i] for i in range(amount_of_moves)
        )

        if has_same_previous_moves and result_of_moves[x] != 1:
            next_move = all_moves[x][amount_of_moves]

            if next_move in available_moves:
                move_index = available_moves.index(next_move)
                non_losses_for_each_move[move_index] += 1

    if len(previous_moves) % 2:
        mxv = max(non_losses_for_each_move)
        
        # If all moves have a score of 0, pick the first available move
        if mxv == 0:
            best_move = available_moves[0]
        else:
            best_move_index = non_losses_for_each_move.index(mxv)
            best_move = available_moves[best_move_index]

    else:
        mnv = min(non_losses_for_each_move)

        best_move_index = non_losses_for_each_move.index(mnv)
        best_move = available_moves[best_move_index]

    return best_move


def player_one_starts():
    previous_moves = []
    global all_moves
    global result_of_moves
    with open("all_moves.pkl", "rb") as file:
        all_moves = pickle.load(file)

    with open("result_of_moves.pkl", "rb") as file:
        result_of_moves = pickle.load(file)

    turn = int(input("Type 1 for player to start and 2 for ai to start"))

    won = False
    while not won:
        if turn == 1:
            position = int(input("where do you want to go?"))
            previous_moves.append(position)
            board[position // 3][position % 3] = 1
            turn = 2
            print('')
            for b in board:
                print(b)
            win = check_win(board)
            if win == 1:
                print("player won!")
                won = True

            if win == 2:
                print("AI won!")
                won = True

            if win == 3:
                print("Draw!")
                won = True
        
        elif not won:
            
            if len(previous_moves) == 3:
                if previous_moves[0] == 0 and previous_moves[2] == 8 or previous_moves[0] == 8 and previous_moves[2] == 0 or previous_moves[0] == 2 and previous_moves[2] == 6 or previous_moves[0] == 6 and previous_moves[2] == 2:
                    position = 1
            
                else:
                    position = move_to_tie(previous_moves)

            elif len(previous_moves) == 0:
                position = 0

            elif len(previous_moves) == 2:
                position = 8
            else:
                position = move_to_tie(previous_moves)
            previous_moves.append(position)
            board[position // 3][position % 3] = 2
            turn = 1
            print('')
            for b in board:
                print(b)

            win = check_win(board)
            if win == 1:
                print("player won!")
                won = True

            if win == 2:
                print("AI won!")
                won = True

            if win == 3:
                print("Draw!")
                won = True
        


player_one_starts()