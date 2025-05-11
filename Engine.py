from Board import Player1, Player2, Empty, Size, EvalFunction, GetCandidateMoves
from Minimax import Minimax

DepthLimit = 3

def PrintBoard(board):
    print("  ", end="")
    for col in range(Size):
        print(f"{col:2}", end=" ")
    print()
    for row in range(Size):
        print(f"{row:2} ", end="")
        for col in range(Size):
            print(f"{board[row][col]:2}", end=" ")
        print()

def GetAvailableMoves(board):
    return [(i, j) for i in range(Size) for j in range(Size) if board[i][j] == Empty]

def GetAiMove(board, algorithm="minimax", aiPlayer=Player2):
    if algorithm.lower() != "minimax":
        raise NotImplementedError("Only Minimax is implemented currently.")
    isMax = (aiPlayer == Player1)
    _, move = Minimax(board, DepthLimit, isMax, DepthLimit)

    if move:
        board[move[0]][move[1]] = aiPlayer
        print(f"AI ({aiPlayer}) played at: {move}")
    else:
        print("No valid moves found.")
    return move

def PlayHumanVsAi(board):
    currentPlayer = Player1

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
