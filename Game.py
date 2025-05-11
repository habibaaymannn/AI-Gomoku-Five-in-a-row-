import math

BoardSize = 15
DepthLimit = 3
Player1 = 'X'
Player2 = 'O'
Empty = '-'


def CreateBoard(size=BoardSize):
    return [[Empty for _ in range(size)] for _ in range(size)]


def SetBoard(board, boardState):
    for i in range(len(boardState)):
        board[i] = boardState[i][:]


def PrintBoard(board):
    print("   ", end="")
    for col in range(BoardSize):
        print(f"{col:2}", end=" ")
    print()
    for row in range(BoardSize):
        print(f"{row:2} ", end="")
        for col in range(BoardSize):
            print(f"{board[row][col]:2}", end=" ")
        print()


def EvalFunction(board):
    for row in range(BoardSize):
        for i in range(BoardSize - 4):
            if board[row][i] == board[row][i+1] == board[row][i+2] == board[row][i+3] == board[row][i+4] != Empty:
                return 1 if board[row][i] == Player1 else -1

    for col in range(BoardSize):
        for i in range(BoardSize - 4):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == board[i+4][col] != Empty:
                return 1 if board[i][col] == Player1 else -1

    for i in range(BoardSize - 4):
        for j in range(BoardSize - 4):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] != Empty:
                return 1 if board[i][j] == Player1 else -1

    for i in range(BoardSize - 4):
        for j in range(4, BoardSize):
            if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == board[i+4][j-4] != Empty:
                return 1 if board[i][j] == Player1 else -1

    return 0


def GetCandidateMoves(board):
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    candidates = set()

    for i in range(BoardSize):
        for j in range(BoardSize):
            if board[i][j] != Empty:
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < BoardSize and 0 <= nj < BoardSize and board[ni][nj] == Empty:
                        candidates.add((ni, nj))

    if not candidates:
        return [(BoardSize // 2, BoardSize // 2)]
    return list(candidates)

# Minimax algorithm
def Minimax(board, depth, isMaxPlayer):
    score = EvalFunction(board)
    if depth == 0 or score != 0:
        return score, None

    bestMove = None
    if isMaxPlayer:
        maxEval = -math.inf
        for move in GetCandidateMoves(board):
            board[move[0]][move[1]] = Player1
            eval, _ = Minimax(board, depth - 1, False)
            board[move[0]][move[1]] = Empty
            if eval > maxEval:
                bestMove = move
            maxEval = max(maxEval, eval)
        return maxEval, bestMove
    else:
        minEval = math.inf
        for move in GetCandidateMoves(board):
            board[move[0]][move[1]] = Player2
            eval, _ = Minimax(board, depth - 1, True)
            board[move[0]][move[1]] = Empty
            if eval < minEval:
                bestMove = move
            minEval = min(minEval, eval)
        return minEval, bestMove

#  AI move
def GetAiMove(board, algorithm="minimax", aiPlayer=Player2):
    if algorithm.lower() != "minimax":
        raise NotImplementedError("Only Minimax is implemented currently.")

    isMax = (aiPlayer == Player1)
    _, move = Minimax(board, DepthLimit, isMax)

    if move:
        board[move[0]][move[1]] = aiPlayer
        print(f"AI ({aiPlayer}) played at: {move}")
    else:
        print("No valid moves found.")
    return move


def GetAvailableMoves(board):
    return [(i, j) for i in range(BoardSize) for j in range(BoardSize) if board[i][j] == Empty]

#  game loop
def PlayHumanVsAi(board):
    currentPlayer = Player1  # Human starts

    while True:
        PrintBoard(board)

        winner = EvalFunction(board)
        if winner == 1:
            print("Player X (Human) wins!")
            break
        elif winner == -1:
            print("Player O (AI) wins!")
            break
        elif not GetAvailableMoves(board):
            print("Game is a draw!")
            break

        if currentPlayer == Player1:
            while True:
                try:
                    move = input("Enter your move (row col): ").split()
                    x, y = int(move[0]), int(move[1])
                    if board[x][y] == Empty:
                        board[x][y] = Player1
                        break
                    else:
                        print("That cell is not empty.")
                except:
                    print("Invalid input. Please enter row and column numbers separated by a space.")
        else:
            print("AI is thinking...")
            GetAiMove(board, aiPlayer=Player2)

        currentPlayer = Player2 if currentPlayer == Player1 else Player1


if __name__ == "__main__":
    board = CreateBoard()

    try:
        choice = int(input("Would you like to enter the board state or start from scratch? (0 = enter board, 1 = start from scratch): "))
    except ValueError:
        choice = 1

    if choice == 1:
        print("Starting with empty board:")
        PrintBoard(board)
    else:
        boardState = []
        print(f"Enter the board row by row ({BoardSize} rows). Use '{Player1}' for Player 1, '{Player2}' for Player 2, and '{Empty}' for empty cells.")
        for i in range(BoardSize):
            while True:
                row = input(f"Row {i}: ").strip()
                if len(row) == BoardSize and all(c in [Player1, Player2, Empty] for c in row):
                    boardState.append(list(row))
                    break
                else:
                    print("Invalid row. Please enter exactly", BoardSize, "characters using only X, O, or -")
        SetBoard(board, boardState)
        print("Initial board:")
        PrintBoard(board)

    print("Starting Human vs AI game:")
    PlayHumanVsAi(board)
