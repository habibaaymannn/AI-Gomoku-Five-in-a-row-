Size = 15
Player1 = 'X'
Player2 = 'O'
Empty = '-'


def evalHorizontal(board, for_player, players_turn):
    evaluations = [0, 2, 0]  # [consecutive, blocks, score]
    player = Player2 if for_player else Player1
    for i in range(Size):
        for j in range(Size):
            if board[i][j] == player:
                evaluations[0] += 1
            elif board[i][j] == Empty:
                if evaluations[0] > 0:
                    evaluations[1] -= 1
                    evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1],
                                                                for_player == players_turn)
                    evaluations[0] = 0
                evaluations[1] = 1
            elif evaluations[0] > 0:
                evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1], for_player == players_turn)
                evaluations[0] = 0
                evaluations[1] = 2
            else:
                evaluations[1] = 2
        if evaluations[0] > 0:
            evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1], for_player == players_turn)
        evaluations[0] = 0
        evaluations[1] = 2
    return evaluations[2]


def evalVertical(board, for_player, players_turn):
    evaluations = [0, 2, 0]
    player = Player2 if for_player else Player1
    for j in range(Size):
        for i in range(Size):
            if board[i][j] == player:
                evaluations[0] += 1
            elif board[i][j] == Empty:
                if evaluations[0] > 0:
                    evaluations[1] -= 1
                    evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1],
                                                                for_player == players_turn)
                    evaluations[0] = 0
                evaluations[1] = 1
            elif evaluations[0] > 0:
                evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1], for_player == players_turn)
                evaluations[0] = 0
                evaluations[1] = 2
            else:
                evaluations[1] = 2
        if evaluations[0] > 0:
            evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1], for_player == players_turn)
        evaluations[0] = 0
        evaluations[1] = 2
    return evaluations[2]


def evalDiagonal(board, for_player, players_turn):
    evaluations = [0, 2, 0]
    player = Player2 if for_player else Player1
    # Bottom-left to top-right
    for k in range(2 * (Size - 1) + 1):
        i_start = max(0, k - Size + 1)
        i_end = min(Size - 1, k)
        for i in range(i_start, i_end + 1):
            j = k - i
            if board[i][j] == player:
                evaluations[0] += 1
            elif board[i][j] == Empty:
                if evaluations[0] > 0:
                    evaluations[1] -= 1
                    evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1],
                                                                for_player == players_turn)
                    evaluations[0] = 0
                evaluations[1] = 1
            elif evaluations[0] > 0:
                evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1], for_player == players_turn)
                evaluations[0] = 0
                evaluations[1] = 2
            else:
                evaluations[1] = 2
        if evaluations[0] > 0:
            evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1], for_player == players_turn)
        evaluations[0] = 0
        evaluations[1] = 2
    # Top-left to bottom-right
    for k in range(1 - Size, Size):
        i_start = max(0, k)
        i_end = min(Size + k - 1, Size - 1)
        for i in range(i_start, i_end + 1):
            j = i - k
            if board[i][j] == player:
                evaluations[0] += 1
            elif board[i][j] == Empty:
                if evaluations[0] > 0:
                    evaluations[1] -= 1
                    evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1],
                                                                for_player == players_turn)
                    evaluations[0] = 0
                evaluations[1] = 1
            elif evaluations[0] > 0:
                evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1], for_player == players_turn)
                evaluations[0] = 0
                evaluations[1] = 2
            else:
                evaluations[1] = 2
        if evaluations[0] > 0:
            evaluations[2] += calcConsecutiveScore(evaluations[0], evaluations[1], for_player == players_turn)
        evaluations[0] = 0
        evaluations[1] = 2
    return evaluations[2]

def calcConsecutiveScore(count, blocks, current_turn):
    win_score = 100_000_000
    win_guarantee = 1_000_000
    if blocks == 2 and count < 5:
        return 0
    if count >= 5:
        return win_score * (2 if count > 5 else 1)
    elif count == 4:
        if current_turn:
            return win_guarantee
        return win_guarantee // 4 if blocks == 0 else 200
    elif count == 3:
        if blocks == 0:
            return 50_000 if current_turn else 200
        return 10 if current_turn else 5
    elif count == 2:
        if blocks == 0:
            return 7 if current_turn else 5
        return 3
    return 1
def EvalFunction(board):
    x_score = getScore(board, False, False)
    o_score = getScore(board, True, True)
    if x_score >= 100_000_000:
        return 1
    if o_score >= 100_000_000:
        return -1
    return 0

def getScore(board, for_player, players_turn):
    return (evalHorizontal(board, for_player, players_turn) +
            evalVertical(board, for_player, players_turn) +
            evalDiagonal(board, for_player, players_turn))

def GetCandidateMoves(board):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
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
    def score_move(move):
        i, j = move
        score = 0
        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            if 0 <= ni < Size and 0 <= nj < Size and board[ni][nj] != Empty:
                score += 1
        return score

    candidate_list = list(candidates)
    candidate_list.sort(key=score_move, reverse=True)
    return candidate_list

def evalBoard(board, players_turn):
    x_score = getScore(board, False, players_turn)
    o_score = getScore(board, True, players_turn)

    if x_score >= 100_000_000:
        return -1  # Player1 wins
    if o_score >= 100_000_000:
        return 1  # Player2 wins

    block_weight = 1.5 if players_turn else 1.0
    win_weight = 2.0 if players_turn else 1.5

    x_score = max(1.0, x_score)
    o_score = max(1.0, o_score)

    return (o_score * win_weight) / (x_score * block_weight)


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