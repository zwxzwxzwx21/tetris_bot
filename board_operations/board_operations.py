# all the functions that directly manipulate the board 
# this file deserve a namechange
import numpy as np
def convert_board_numpy(board):
    arr = np.array(board)
    if arr.shape == (20,10):
        return np.array(board).T
    return arr
    

def clear_lines(board):
    """
    Removes all full lines from the board and adds empty lines at the top.
    """
    new_board = []
    lines_cleared = 0

    for col in board:
        if all(cell != ' ' for cell in col):
            lines_cleared += 1
        else:
            new_board.append(col)

    # adds empty rows at the top for cleared lines
    for _ in range(lines_cleared):
        new_board.insert(0, [' ' for _ in range(10)])
    # doesn't have to return lines_cleared, it does so to count quads and other clears
    return new_board, lines_cleared
