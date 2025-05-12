import tkinter as tk

BOARD_SIZE = 15
CELL_SIZE = 40
STONE_RADIUS = 15

# Pastel color choices
BACKGROUND_COLOR = '#E8E8F2'  # Light lavender pastel background
LINE_COLOR = '#D0D0E3'  # Soft pastel grayish-blue for grid lines
BOARD_BORDER_COLOR = '#B2A1D3'  # Soft pastel lavender for the board border
SHADOW_COLOR = '#B3B3C6'  # Light gray shadow color for stones
BLACK_STONE_COLOR = '#2C2C54'  # Dark purple for black stones
WHITE_STONE_COLOR = '#FFFFFF'  # White for the white stones
STONE_OUTLINE_COLOR = '#A6A6D9'  # Soft light purple outline for the stones

class GomokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gomoku (Five in a Row)")
        
        # Set the background to pastel lavender
        self.canvas = tk.Canvas(root, width=BOARD_SIZE * CELL_SIZE, height=BOARD_SIZE * CELL_SIZE, bg=BACKGROUND_COLOR)
        self.canvas.pack()

        # Creating the board as a 2D list of None values
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'black'  # Alternate between black and white
        self.draw_grid()
        
        # Binding mouse click to place a stone
        self.canvas.bind("<Button-1>", self.place_stone)

    def draw_grid(self):
        # Draw vertical and horizontal lines with soft pastel blue
        for i in range(BOARD_SIZE):
            # Vertical lines (softer grayish-blue color)
            self.canvas.create_line(CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2,
                                    CELL_SIZE // 2 + i * CELL_SIZE, CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE,
                                    width=2, fill=LINE_COLOR)
            # Horizontal lines (soft pastel grayish-blue color)
            self.canvas.create_line(CELL_SIZE // 2, CELL_SIZE // 2 + i * CELL_SIZE,
                                    CELL_SIZE // 2 + (BOARD_SIZE - 1) * CELL_SIZE, CELL_SIZE // 2 + i * CELL_SIZE,
                                    width=2, fill=LINE_COLOR)

        # Center the board to have a neat visual margin with a rounded pastel border
        self.canvas.create_rectangle(CELL_SIZE // 2, CELL_SIZE // 2,
                                     (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2, 
                                     (BOARD_SIZE - 1) * CELL_SIZE + CELL_SIZE // 2,
                                     outline=BOARD_BORDER_COLOR, width=6, stipple='gray75')  # Light lavender color for border
    
    def place_stone(self, event):
        # Calculate row and column based on mouse click coordinates
        col = int(round((event.x - CELL_SIZE // 2) / CELL_SIZE))
        row = int(round((event.y - CELL_SIZE // 2) / CELL_SIZE))
        
        # Ensure the move is within bounds and the cell is empty
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.draw_stone(row, col, self.current_player)
            self.current_player = 'white' if self.current_player == 'black' else 'black'

    def draw_stone(self, row, col, color):
        # Stone position calculation
        x = CELL_SIZE // 2 + col * CELL_SIZE
        y = CELL_SIZE // 2 + row * CELL_SIZE
        
        # Modern stone design: smooth edges and slight shadow
        shadow_offset = 3  # Create a subtle shadow effect
        if color == 'black':
            # Black stone with a subtle shadow and a deep purple shade
            self.canvas.create_oval(x - STONE_RADIUS + shadow_offset, y - STONE_RADIUS + shadow_offset,
                                    x + STONE_RADIUS + shadow_offset, y + STONE_RADIUS + shadow_offset,
                                    fill=SHADOW_COLOR, outline='', width=1)
            self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                    x + STONE_RADIUS, y + STONE_RADIUS,
                                    fill=BLACK_STONE_COLOR, outline=STONE_OUTLINE_COLOR, width=2)
        elif color == 'white':
            # White stone with a subtle shadow and a soft white shade
            self.canvas.create_oval(x - STONE_RADIUS + shadow_offset, y - STONE_RADIUS + shadow_offset,
                                    x + STONE_RADIUS + shadow_offset, y + STONE_RADIUS + shadow_offset,
                                    fill=SHADOW_COLOR, outline='', width=1)
            self.canvas.create_oval(x - STONE_RADIUS, y - STONE_RADIUS,
                                    x + STONE_RADIUS, y + STONE_RADIUS,
                                    fill=WHITE_STONE_COLOR, outline=STONE_OUTLINE_COLOR, width=2)

if __name__ == "__main__":
    root = tk.Tk()
    game = GomokuGUI(root)
    root.mainloop()
