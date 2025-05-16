import tkinter as tk
from tkinter import messagebox
from Board import Player1, Player2, Empty, Size, EvalFunction
from Engine import GetAiMove

BOARD_SIZE = 15
CELL_SIZE = 40
STONE_RADIUS = 15

BACKGROUND_COLOR = '#E8E8F2'
LINE_COLOR = '#D0D0E3'
BOARD_BORDER_COLOR = '#B2A1D3'
SHADOW_COLOR = '#B3B3C6'
BLACK_STONE_COLOR = '#2C2C54'
WHITE_STONE_COLOR = '#FFFFFF'
STONE_OUTLINE_COLOR = '#A6A6D9'


class GomokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku (Five in a Row)")

        self.board = [[Empty for _ in range(Size)] for _ in range(Size)]
        self.current_player = Player1
        self.game_over = False

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=10)

        # game mode selection
        self.mode_var = tk.StringVar(value="human_vs_ai")
        tk.Label(self.control_frame, text="Game Mode:").pack(side=tk.LEFT)
        tk.Radiobutton(self.control_frame, text="Human vs AI", variable=self.mode_var,
                       value="human_vs_ai").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(self.control_frame, text="AI vs AI", variable=self.mode_var,
                       value="ai_vs_ai").pack(side=tk.LEFT, padx=5)

        # new Game button
        tk.Button(self.control_frame, text="New Game", command=self.reset_game).pack(side=tk.LEFT, padx=10)

        self.canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        self.draw_grid()
        self.canvas.bind("<Button-1>", self.on_click)

        # start AI vs AI if selected
        if self.mode_var.get() == "ai_vs_ai":
            self.ai_move()

    def draw_grid(self):
        for i in range(BOARD_SIZE):
            # Vertical lines
            self.canvas.create_line(CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2,
                                    CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE,
                                    width=2, fill=LINE_COLOR)
            # Horizontal lines
            self.canvas.create_line(CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE,
                                    CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE, CELL_SIZE // 2 + i * CELL_SIZE,
                                    width=2, fill=LINE_COLOR)

        # Board border
        self.canvas.create_rectangle(CELL_SIZE // 2, CELL_SIZE // 2,
                                     (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2,
                                     (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2,
                                     outline=BOARD_BORDER_COLOR, width=6, stipple='gray75')

    def on_click(self, event):
        if self.game_over:
            return

        if self.mode_var.get() == "ai_vs_ai":
            return

        if self.current_player == Player2 and self.mode_var.get() == "human_vs_ai":
            return

        col = int(round((event.x - CELL_SIZE // 2) / CELL_SIZE))
        row = int(round((event.y - CELL_SIZE // 2) / CELL_SIZE))

        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == Empty:
            self.make_move(row, col)

            #this part that makes the human stone 'black' appears immediately
            self.root.update_idletasks()

            if not self.game_over and self.mode_var.get() == "human_vs_ai" and self.current_player == Player2:
                self.ai_move()

    def make_move(self, row, col):
        self.board[row][col] = self.current_player
        self.draw_stone(row, col, self.current_player)

        winner = EvalFunction(self.board)
        if winner != 0:
            self.game_over = True
            winner_name = "Black" if winner == 1 else "White"
            messagebox.showinfo("Game Over", f"{winner_name} wins!")
            return
        elif all(cell != Empty for row in self.board for cell in row):
            self.game_over = True
            messagebox.showinfo("Game Over", "The game is a draw!")
            return

        self.current_player = Player2 if self.current_player == Player1 else Player1

    def draw_stone(self, row, col, player):
        x = CELL_SIZE // 2 + col * CELL_SIZE
        y = CELL_SIZE // 2 + row * CELL_SIZE

        shadow_offset = 3
        if player == Player1:  
            self.canvas.create_oval(x - STONE_RADIUS + shadow_offset, y - STONE_RADIUS + shadow_offset,
                                    x + STONE_RADIUS + shadow_offset, y + STONE_RADIUS + shadow_offset,
                                    fill=SHADOW_COLOR, outline='', width=1)
            self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                    x + STONE_RADIUS, y + STONE_RADIUS,
                                    fill=BLACK_STONE_COLOR, outline=STONE_OUTLINE_COLOR, width=2)
        else:  
            self.canvas.create_oval(x - STONE_RADIUS + shadow_offset, y - STONE_RADIUS + shadow_offset,
                                    x + STONE_RADIUS + shadow_offset, y + STONE_RADIUS + shadow_offset,
                                    fill=SHADOW_COLOR, outline='', width=1)
            self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                    x + STONE_RADIUS, y + STONE_RADIUS,
                                    fill=WHITE_STONE_COLOR, outline=STONE_OUTLINE_COLOR, width=2)

    def ai_move(self):
        if self.game_over:
            return

        if self.mode_var.get() == "human_vs_ai":
            algorithm = "minimax"
        else:
            algorithm = "minimax" if self.current_player == Player1 else "alphabeta"

        move = GetAiMove(self.board, algorithm=algorithm, aiPlayer=self.current_player)

        if move:
            self.make_move(move[0], move[1])

            if not self.game_over and self.mode_var.get() == "ai_vs_ai":
                self.root.after(500, self.ai_move)  # small delay

    def reset_game(self):
        self.board = [[Empty for _ in range(Size)] for _ in range(Size)]
        self.current_player = Player1
        self.game_over = False

        self.canvas.delete("all")
        self.draw_grid()

        if self.mode_var.get() == "ai_vs_ai":
            self.ai_move()


if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGUI(root)
    root.mainloop()
