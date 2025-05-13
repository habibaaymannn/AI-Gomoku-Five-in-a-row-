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

def count_sequence(board, i, j, dx, dy, player):
    count = 1  # the placed mark
    # go forward
    x, y = i + dx, j + dy
    while 0 <= x < Size and 0 <= y < Size and board[x][y] == player:
        count += 1
        x += dx
        y += dy
    # go backward
    x, y = i - dx, j - dy
    while 0 <= x < Size and 0 <= y < Size and board[x][y] == player:
        count += 1
        x -= dx
        y -= dy
    return count

def evaluate_strength(board, i, j, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    max_streak = 1
    for dx, dy in directions:
        streak = count_sequence(board, i, j, dx, dy, player)
        max_streak = max(max_streak, streak)
    return max_streak

def strength_to_score(strength, is_O):
    if strength >= 5:
        return 5 if is_O else -5
    elif strength == 4:
        return 4 if is_O else -4
    elif strength == 3:
        return 3 if is_O else -3
    elif strength == 2:
        return 2 if is_O else -2
    else:
        return 0

def ScoreCandidateMoves(board):
    candidates = GetCandidateMoves(board)
    scored_moves = []

    for i, j in candidates:
        board_copy = [row[:] for row in board]

        # Score for X
        board_copy[i][j] = Player1
        x_strength = evaluate_strength(board_copy, i, j, Player1)

        # Score for O
        board_copy[i][j] = Player2
        o_strength = evaluate_strength(board_copy, i, j, Player2)

        # Choose the stronger one and set sign accordingly
        if o_strength > x_strength:
            score = strength_to_score(o_strength, is_O=True)
        elif x_strength > o_strength:
            score = strength_to_score(x_strength, is_O=False)
        else:
            score = 0

        scored_moves.append(((i, j), score))

    return scored_moves
