import math
from Board import GetCandidateMoves, EvalFunction, Empty, Player1, Player2

def BetaAlpha(board, depth, maxPlayer, depthLimit, alpha=-math.inf, beta=math.inf):
    score = EvalFunction(board)
    if depth == 0 or score != 0:
        return score, None

    bestMove = None
    if maxPlayer:
        maxEval = -math.inf
        for move in GetCandidateMoves(board):
            board[move[0]][move[1]] = Player1
            evaluate, _ = BetaAlpha(board, depth - 1, False, depthLimit, alpha, beta)
            board[move[0]][move[1]] = Empty
            if evaluate > maxEval:
                maxEval = evaluate
                bestMove = move
            alpha = max(alpha, evaluate)
            if beta <= alpha:
                break  # Beta cut-off
        return maxEval, bestMove
    else:
        minEval = math.inf
        for move in GetCandidateMoves(board):
            board[move[0]][move[1]] = Player2
            evaluate, _ = BetaAlpha(board, depth - 1, True, depthLimit, alpha, beta)
            board[move[0]][move[1]] = Empty
            if evaluate < minEval:
                minEval = evaluate
                bestMove = move
            beta = min(beta, evaluate)
            if beta <= alpha:
                break  # Alpha cut-off
        return minEval, bestMove
