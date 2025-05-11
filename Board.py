Size = 15
Player1 = 'X'
Player2 = 'O'
Empty = '-'

def EvalFunction(board):
    for row in range(Size):
        for i in range(Size - 4):
            if board[row][i] == board[row][i+1] == board[row][i+2] == board[row][i+3] == board[row][i+4] != Empty:
                return 1 if board[row][i] == Player1 else -1

    for col in range(Size):
        for i in range(Size - 4):
            if board[i][col] == board[i+1][col] == board[i+2][col] == board[i+3][col] == board[i+4][col] != Empty:
                return 1 if board[i][col] == Player1 else -1

    for i in range(Size - 4):
        for j in range(Size - 4):
            if board[i][j] == board[i+1][j+1] == board[i+2][j+2] == board[i+3][j+3] == board[i+4][j+4] != Empty:
                return 1 if board[i][j] == Player1 else -1

    for i in range(Size - 4):
        for j in range(4, Size):
            if board[i][j] == board[i+1][j-1] == board[i+2][j-2] == board[i+3][j-3] == board[i+4][j-4] != Empty:
                return 1 if board[i][j] == Player1 else -1

    return 0

def GetCandidateMoves(board):
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    candidates = set()

    for i in range(Size):
        for j in range(Size):
            if board[i][j] != Empty:
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < Size and 0 <= nj < Size and board[ni][nj] == Empty:
                        candidates.add((ni, nj))

    if not candidates:
        return [(Size // 2, Size // 2)]
    return list(candidates)
