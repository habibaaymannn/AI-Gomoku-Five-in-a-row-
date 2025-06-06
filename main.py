from Board import Size, Empty, Player1, Player2
from Engine import PlayHumanVsAi, PlayAiVsAi

def main():
    board = [[Empty for _ in range(Size)] for _ in range(Size)]

    try:
        choice = int(input("Would you like to enter the board state or start from scratch? (0 = enter board, 1 = start from scratch): "))
    except ValueError:
        choice = 1

    if choice == 1:
        print("Starting with empty board:")
    else:
        board_state = []
        print(f"Enter the board row by row ({Size} rows). Use '{Player1}' for Player 1, '{Player2}' for Player 2, and '{Empty}' for empty cells.")
        for i in range(Size):
            while True:
                row = input(f"Row {i}: ").strip()
                if len(row) == Size and all(c in [Player1, Player2, Empty] for c in row):
                    board_state.append(list(row))
                    break
                else:
                    print("Invalid row. Please enter exactly", Size, "characters using only X, O, or -")
        board = board_state
        print("Initial board:")

    print("\nChoose game mode:")
    print("1: Human vs AI")
    print("2: AI vs AI (Minimax vs AlphaBeta)")
    mode = input("Enter your choice (1 or 2): ").strip()

    if mode == "1":
        PlayHumanVsAi(board)
    elif mode == "2":
        PlayAiVsAi(board)
    else:
        print("Invalid choice. Defaulting to Human vs AI.")
        PlayHumanVsAi(board)

if __name__ == "__main__":
    main()
