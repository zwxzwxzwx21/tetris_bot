# all the functions that directly manipulate the board
# this file deserve a namechange
import numpy as np


def convert_board_numpy(board):
    arr = np.array(board)
    if arr.shape == (20, 10):
        return arr.T
    return arr


def clear_lines(board):
    """
    Removes all full lines from the board and adds empty lines at the top.
    """
    # filled = np.all(board != " ", axis=-1)

    width, height = board.shape
    filled_rows = np.all(board != " ", axis=0)
    assert len(filled_rows) == 20
    cleared_lines = filled_rows.sum()
    if cleared_lines == 0:
        return board, 0
    arrays_to_keep = np.invert(filled_rows)

    new_board = board[:, arrays_to_keep]
    new_board = np.hstack(
        (np.full(shape=(10, cleared_lines), fill_value=" "), new_board)
    )
    return new_board, cleared_lines
