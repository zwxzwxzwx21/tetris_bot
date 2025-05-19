# all the functions that directly manipulate the board 

# this file deserve a namechange

# ---
# This module contains functions for direct manipulation of the Tetris board.
# Use these functions to clear lines, apply gravity, and perform other board-level operations.
# These are called by the main game loop and AI logic to update the board state.
# ---

def clear_lines(board):
    """
    Removes all full lines from the board and adds empty lines at the top.
    Args:
        board (list of lists): The current board state.
    Returns:
        new_board (list of lists): The board after clearing lines.
    Usage:
        - Call after placing a piece to remove completed lines.
        - Use in the main game loop or AI logic.
    """
    new_board = []
    lines_cleared = 0

    for row in board:
        if all(cell != ' ' for cell in row):
            lines_cleared += 1
        else:
            new_board.append(row)

    # Add empty rows at the top for cleared lines
    for _ in range(lines_cleared):
        new_board.insert(0, [' ' for _ in range(10)])

    return new_board

def apply_gravity(board):
    """
    Applies gravity to the board, causing blocks to fall down into empty spaces.
    Args:
        board (list of lists): The current board state.
    Modifies:
        board (in-place): The board is updated so that all blocks fall to the lowest possible position.
    Usage:
        - Call after clearing lines or when simulating gravity.
        - Use in the main game loop or AI logic.
    """
    for col in range(10):
        blocks = []
        for row in range(len(board)):
            if board[row][col] != ' ':
                blocks.append(board[row][col])
        for row in range(len(board)-1, -1, -1):
            if blocks:
                board[row][col] = blocks.pop()
            else:
                board[row][col] = ' '

# ---
# How and when to use:
# - Use clear_lines(board) after every piece placement to remove filled lines.
# - Use apply_gravity(board) if you want to simulate gravity after line clears or other board changes.
# - These functions are intended for use in the main game loop, AI, or any board manipulation logic.
# ---