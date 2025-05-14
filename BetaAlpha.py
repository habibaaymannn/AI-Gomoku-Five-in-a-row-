import math
import random
import time
from Board import GetCandidateMoves, evalBoard, Empty, Player1, Player2

def BetaAlpha(board, depth, maxPlayer, depthLimit, alpha=-math.inf, beta=math.inf, nodeCount=[0]):
    nodeCount[0] += 1
    score = evalBoard(board, maxPlayer)

    if depth == 0 or abs(score) >= 100_000_000:
        return score, None

    # Generate candidate moves with heuristic scoring
    candidate_moves = GetCandidateMoves(board)
    candidate_moves.sort(key=lambda move: evalBoard(board, maxPlayer), reverse=maxPlayer)

    bestMoves = []
    if maxPlayer:
        maxEval = -math.inf
        for move in candidate_moves:
            board[move[0]][move[1]] = Player2
            eval, _ = BetaAlpha(board, depth - 1, False, depthLimit, alpha, beta, nodeCount)
            board[move[0]][move[1]] = Empty

            if eval > maxEval:
                maxEval = eval
                bestMoves = [move]
            elif eval == maxEval:
                bestMoves.append(move)

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        bestMove = random.choice(bestMoves) if bestMoves else None
        return maxEval, bestMove

    else:
        minEval = math.inf
        for move in candidate_moves:
            board[move[0]][move[1]] = Player1
            eval, _ = BetaAlpha(board, depth - 1, True, depthLimit, alpha, beta, nodeCount)
            board[move[0]][move[1]] = Empty

            if eval < minEval:
                minEval = eval
                bestMoves = [move]
            elif eval == minEval:
                bestMoves.append(move)

            beta = min(beta, eval)
            if beta <= alpha:
                break

        bestMove = random.choice(bestMoves) if bestMoves else None
        return minEval, bestMove