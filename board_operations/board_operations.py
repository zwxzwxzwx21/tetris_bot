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
    """
    new_board = []
    lines_cleared = 0

    for row in board:
        if all(cell != ' ' for cell in row):
            lines_cleared += 1
        else:
            new_board.append(row)

    # adds empty rows at the top for cleared lines
    for _ in range(lines_cleared):
        new_board.insert(0, [' ' for _ in range(10)])
    # doesn't have to return lines_cleared, it does so to count quads and other clears
    return new_board, lines_cleared



# ---
# How and when to use:
# - Use clear_lines(board) after every piece placement to remove filled lines.
# - Use apply_gravity(board) if you want to simulate gravity after line clears or other board changes.
# - These functions are intended for use in the main game loop, AI, or any board manipulation logic.
# ---