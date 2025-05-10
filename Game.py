import math

class Gomoku:
    def __init__(self, size=15, depth=3):
        self.size = size
        self.depth_limit = depth
        self.player1 = 'X'
        self.player2 = 'O'
        self.empty = '-'
        self.board = [[self.empty for _ in range(size)] for _ in range(size)]

    def setBoard(self, board_state):
        self.board = board_state

    def printBoard(self):
        print("   ", end="")
        for col in range(self.size):
            print(f"{col:2}", end=" ")
        print()
        for row in range(self.size):
            print(f"{row:2} ", end="")
            for col in range(self.size):
                print(f"{self.board[row][col]:2}", end=" ")
            print()

    def evalFunction(self):
        for row in range(self.size):
            for i in range(self.size - 4):
                if self.board[row][i] == self.board[row][i+1] == self.board[row][i+2] == self.board[row][i+3] == self.board[row][i+4] != self.empty:
                    return 1 if self.board[row][i] == self.player1 else -1

        for col in range(self.size):
            for i in range(self.size - 4):
                if self.board[i][col] == self.board[i+1][col] == self.board[i+2][col] == self.board[i+3][col] == self.board[i+4][col] != self.empty:
                    return 1 if self.board[i][col] == self.player1 else -1

        for i in range(self.size - 4):
            for j in range(self.size - 4):
                if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] == self.board[i+4][j+4] != self.empty:
                    return 1 if self.board[i][j] == self.player1 else -1

        for i in range(self.size - 4):
            for j in range(4, self.size):
                if self.board[i][j] == self.board[i+1][j-1] == self.board[i+2][j-2] == self.board[i+3][j-3] == self.board[i+4][j-4] != self.empty:
                    return 1 if self.board[i][j] == self.player1 else -1
        return 0

    def getCandidateMoves(self):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),         (0, 1),
                      (1, -1), (1, 0), (1, 1)]
        candidates = set()

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != self.empty:
                    for dx, dy in directions:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < self.size and 0 <= nj < self.size and self.board[ni][nj] == self.empty:
                            candidates.add((ni, nj))

        if not candidates:
            return [(self.size // 2, self.size // 2)]  # Start from center if board is empty
        return list(candidates)

    def minimax(self, board, depth, max_player):
        score = self.evalFunction()
        if depth == 0 or score != 0:
            return score, None

        best_move = None
        if max_player:
            maxEval = -math.inf
            for move in self.getCandidateMoves():
                board[move[0]][move[1]] = self.player1
                eval, _ = self.minimax(board, depth - 1, False)
                board[move[0]][move[1]] = self.empty
                if eval > maxEval:
                    best_move = move
                maxEval = max(maxEval, eval)
            return maxEval, best_move
        else:
            minEval = math.inf
            for move in self.getCandidateMoves():
                board[move[0]][move[1]] = self.player2
                eval, _ = self.minimax(board, depth - 1, True)
                board[move[0]][move[1]] = self.empty
                if eval < minEval:
                    best_move = move
                minEval = min(minEval, eval)
            return minEval, best_move

    def getAiMove(self, algorithm="minimax", ai_player='O'):
        if algorithm.lower() != "minimax":
            raise NotImplementedError("Only Minimax is implemented currently.")

        is_max = (ai_player == self.player1)
        _, move = self.minimax(self.board, self.depth_limit, is_max)

        if move:
            self.board[move[0]][move[1]] = ai_player
            print(f"AI ({ai_player}) played at: {move}")
        else:
            print("No valid moves found.")
        return move

    def getAvailableMoves(self):
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == self.empty]

    def playHumanVsAi(self):
        current_player = self.player1  # Human starts

        while True:
            self.printBoard()

            winner = self.evalFunction()
            if winner == 1:
                print("Player X (Human) wins!")
                break
            elif winner == -1:
                print("Player O (AI) wins!")
                break
            elif not self.getAvailableMoves():
                print("Game is a draw!")
                break

            if current_player == self.player1:
                while True:
                    try:
                        move = input("Enter your move (row col): ").split()
                        x, y = int(move[0]), int(move[1])
                        if self.board[x][y] == self.empty:
                            self.board[x][y] = self.player1
                            break
                        else:
                            print("That cell is not empty.")
                    except:
                        print("Invalid input. Please enter row and column numbers separated by a space.")
            else:
                print("AI is thinking...")
                self.getAiMove(ai_player=self.player2)

            current_player = self.player2 if current_player == self.player1 else self.player1


if __name__ == "__main__":
    game = Gomoku(size=15, depth=3)

    try:
        choice = int(input("Would you like to enter the board state or start from scratch? (0 = enter board, 1 = start from scratch): "))
    except ValueError:
        choice = 1

    if choice == 1:
        print("Starting with empty board:")
        game.printBoard()
    else:
        board_state = []
        print(f"Enter the board row by row ({game.size} rows). Use '{game.player1}' for Player 1, '{game.player2}' for Player 2, and '{game.empty}' for empty cells.")
        for i in range(game.size):
            while True:
                row = input(f"Row {i}: ").strip()
                if len(row) == game.size and all(c in [game.player1, game.player2, game.empty] for c in row):
                    board_state.append(list(row))
                    break
                else:
                    print("Invalid row. Please enter exactly", game.size, "characters using only X, O, or -")
        game.setBoard(board_state)
        print("Initial board:")
        game.printBoard()

    print("Starting Human vs AI game:")
    game.playHumanVsAi()
