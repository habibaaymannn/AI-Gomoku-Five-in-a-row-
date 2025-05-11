import math
from Board import GetCandidateMoves, EvalFunction, Empty, Player1, Player2

def Minimax(board, depth, maxPlayer, depthLimit):
    score = EvalFunction(board)
    if depth == 0 or score != 0:
        return score, None

    bestMove = None
    if maxPlayer:
        maxEval = -math.inf
        for move in GetCandidateMoves(board):
            board[move[0]][move[1]] = Player1
            eval, _ = Minimax(board, depth - 1, False, depthLimit)
            board[move[0]][move[1]] = Empty
            if eval > maxEval:
                bestMove = move
            maxEval = max(maxEval, eval)
        return maxEval, bestMove
    else:
        minEval = math.inf
        for move in GetCandidateMoves(board):
            board[move[0]][move[1]] = Player2
            eval, _ = Minimax(board, depth - 1, True, depthLimit)
            board[move[0]][move[1]] = Empty
            if eval < minEval:
                bestMove = move
            minEval = min(minEval, eval)
        return minEval, bestMove
