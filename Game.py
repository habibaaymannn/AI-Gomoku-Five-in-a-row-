import math

size = 15
player1 = 'X'
player2 = 'O'
empty ='-'

# class Gomoku
# def AIvsAI():
# def HumanVsAI():
# def miniStep():
# def AlphaStep():

def evalFunction(board):
    #horizontal check
    for row in range(size):
        for i in range(size - 4):
            if board[row][i] == board[row][i+1] == board[row][i+2] == board[row][i+3] == board[row][i+4]:
                if board[row][i] == player1:
                    return 1
                elif board[row][i] == player2:
                    return -1

    #vertical check
    for col in range(size):
        for i in range(size - 4):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == board[i+4][col]:
                if board[i][col] == player1:
                    return 1
                elif board[i][col] == player2:
                    return -1

    #diagonal check
    for i in range(size - 4):
        for j in range(size - 4):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4]:
                if board[i][j] == player1:
                    return 1
                elif board[i][j] == player2:
                    return -1
    #opposite diagonal check
    for i in range(size - 4):
        for j in range(4,size):
            if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == board[i + 4][j - 4]:
                if board[i][j] == player1:
                    return 1
                elif board[i][j] == player2:
                    return -1
    return 0
def getAvailableMoves(board):
    moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == empty:
                moves.append((i,j))
    return moves

#initial call : minimax(currentpos,3,true)
def minimax(board , depth , maxplayer):
    score = evalFunction(board)
    if depth == 0 or score != 0 :
         return score
    if maxplayer:
        maxEval = -math.inf
        for move in getAvailableMoves(board):
            board[move[0]][move[1]] = player1
            eval = minimax(board, depth - 1, False)
            board[move[0]][move[1]] = empty
            maxEval = max(maxEval, eval)
        return maxEval

    else:
        minEval = math.inf
        for move in getAvailableMoves(board):
            board[move[0]][move[1]] = player2
            eval = minimax(board, depth - 1, True)
            board[move[0]][move[1]] = empty
            minEval = min(minEval, eval)
        return minEval


if __name__ == "__main__":
    #print("Enter Game Mode, 0 [Human vs AI] or 1 [AI vs AI]:")
    #mode = int(input())
    
    print("Would you Like to enter the board state or start from scratch? 0 for Entering state, 1 to start fron scratch")
    choice = int(input())
    
    board = []
    if(choice):
        print("Board:")
        for i in range(size):
            board.append(['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
            print(board[i])
            
    else:
        print(f"Enter the board row by row ({size} rows). Use '{player1}' for Player 1, '{player2}' for Player 2, and '{empty}' for empty calls.")
        for i in range(size):
            while True:
                row = input(f"Row {i}: ").strip()
                if len(row) == size and all(c in [player1, player2, empty] for c in row):
                    board.append(list(row))
                    break
                else:
                    print("Invalid row. Please enter exactly", size, "characters using only X, O, or -")
        print("Board:")
        for i in range(size):
            print(board[i])

    # if(mode):
    #     HumanVsAI()
    # else:
    #    AIvsAI()
