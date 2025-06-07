# called by bruteforcer

# ---
# This module contains functions for checking valid placements and simulating piece drops.
# Used by the brute-force AI and main game logic to determine where pieces can be placed.
# Functions here do not modify the original board unless explicitly stated.
# ---

def find_drop_height(board, xpos):
    """
    Finds the height at which a piece would land if dropped in the given column.
    Args:
        board (list of lists): The current board state.
        xpos (int): The column to check.
    Returns:
        int: The row index where the piece would land.
    Usage:
        - Use to determine where a piece will land before placing it.
        - Useful for AI evaluation and move simulation.
    """
    for y in range(len(board)):  
        if board[y][xpos] != ' ':  
            return y - 1  
    return len(board) - 1 # retuns last index of board, being 19 normally 

def can_place(piece, board, row, col):
    """
    Checks if a piece can be placed at the given position on the board.
    Args:
        piece (list of lists): The piece shape.
        board (list of lists): The current board state.
        row (int): The top row for placement.
        col (int): The left column for placement.
    Returns:
        bool: True if the piece can be placed, False otherwise.
    Usage:
        - Called during drop simulation to check if a piece fits.
        - Used by AI and game logic to validate moves.
    """
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                y, x = row + dy, col + dx
                if y >= len(board) or x < 0 or x >= len(board[0]) or board[y][x] != ' ':
                    return False
    return True

def drop_piece(piece, board, col):
    """
    Simulates dropping a piece in the given column and returns a new board.
    Does not modify the original board.
    Args:
        piece (list of lists): The piece shape.
        board (list of lists): The current board state.
        col (int): The column to drop the piece into.
    Returns:
        list of lists: The new board state after the piece is placed.
    Usage:
        - Used by the brute-forcer and AI to simulate moves.
        - Call to get the resulting board after a drop.
    """
    board_copy = [row.copy() for row in board]  # Deep copy
    row = 0
    while can_place(piece, board_copy, row + 1, col):
        row += 1
    place_piece(piece, board_copy, row, col)
    return board_copy

def place_piece(piece, board, row, col):
    """
    Places a piece on the board at the specified position.
    Modifies the board in-place.
    Args:
        piece (list of lists): The piece shape.
        board (list of lists): The board to modify.
        row (int): The top row for placement.
        col (int): The left column for placement.
    Usage:
        - Used internally by drop_piece and by game logic to place pieces.
        - Modifies the board directly.
    """
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                board[row + dy][col + dx] = cell
    # print("place piece x pos",col + dx)

# ---
# How and when to use:
# - Use drop_piece() to simulate a move without changing the original board.
# - Use can_place() to check if a move is valid before placing a piece.
# - Use place_piece() to actually place a piece on a board (modifies in-place).
# - These functions are intended for use in the brute-forcer, AI, and main game loop.
# ---