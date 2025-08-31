# all the functions that directly manipulate the board 
# this file deserve a namechange
import numpy as np
def convert_board_numpy(board):
    arr = np.array(board)
    if arr.shape == (20,10):
        return arr.T
    return arr
    

def clear_lines(board):
    """
    Removes all full lines from the board and adds empty lines at the top.
    """
    filled = [y for y in range(20) if np.all(board[:,y] != ' ')]
    
    width,height = board.shape
    filled_rows = [y for y in range(height) if np.all(board[:,y] != ' ')]
    cleared_lines = len(filled_rows)
    if cleared_lines == 0:
        return board, 0
    arrays_to_keep = np.array([y not in filled_rows for y in range(height)])
    left_arrays = board[:,arrays_to_keep]
    adjustment = np.full((width,cleared_lines), ' ', dtype=board.dtype)
    new_board = np.concatenate((adjustment, left_arrays), axis=1)
    return new_board, cleared_lines