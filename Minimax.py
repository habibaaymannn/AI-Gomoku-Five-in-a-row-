import math
import random
import time
from Board import GetCandidateMoves, evalBoard, Empty, Player1, Player2

def Minimax(board, depth, maxPlayer, depthLimit):
    # Initialize random seed
    random.seed(time.time())
    score = evalBoard(board, maxPlayer)

    if depth == 0 or abs(score) >= 100_000_000:
        return score, None

    bestMoves = []
    if maxPlayer:
        maxEval = -math.inf
        for move in GetCandidateMoves(board):
            board[move[0]][move[1]] = Player2
            eval, _ = Minimax(board, depth - 1, False, depthLimit)
            board[move[0]][move[1]] = Empty
            if eval > maxEval:
                maxEval = eval
                bestMoves = [move]
            elif eval == maxEval:
                bestMoves.append(move)
        bestMove = random.choice(bestMoves) if bestMoves else None
        return maxEval, bestMove
    else:
        minEval = math.inf
        for move in GetCandidateMoves(board):
            board[move[0]][move[1]] = Player1
            eval, _ = Minimax(board, depth - 1, True, depthLimit)
            board[move[0]][move[1]] = Empty
            if eval < minEval:
                minEval = eval
                bestMoves = [move]
            elif eval == minEval:
                bestMoves.append(move)
        bestMove = random.choice(bestMoves) if bestMoves else None
        return minEval, bestMove