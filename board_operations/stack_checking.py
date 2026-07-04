import logging

from config import BOARD_WIDTH

logging.basicConfig(
    format="%(levelname)s: %(filename)s: %(lineno)d: %(message)s", level=logging.DEBUG
)

def calculate_board_messiness(board, y1=0, y2=None):
    """the idea is that we have X holes in a line, and if there are no shifts in holes, so we can have line with hole on X 5
    for Y = 10, and hole on X 5 for Y = 11, then we have no shifts, so we dont need as many pieces as we would need
    if we hav a hole on x 4, which we need at least one more piece to clear, basically try to guess amount of pieces needed to get to the well
    """
    #board_garbage_array = [0] * BOARD_WIDTH
    shift_number = 0 
    if y2 is None:
        y2 = len(board)
    first_row = True
    for y in range(y1, y2):
        for x in range(BOARD_WIDTH):
            if board[y][x] == " ":
                if 0 < x < BOARD_WIDTH+1:
                    #TODO  fix the condition above as it skips sides
                    if not first_row:
                        if board[y+1][x] == " ": 
                            if board[y+1][x+1] == " ":
                                shift_number += 0.5
                            elif board[y+1][x-1] == " ":
                                shift_number += 0.5
                            # im aware it can count multiple shifts for one hole
                        else:
                            if board[y+1][x] != " ":
                                shift_number += 1
                                if board[y+1][x+1] == " ":
                                    shift_number += 1
                                elif board[y+1][x-1] == " ":
                                    shift_number += 1
                
                first_row = False
    
    return shift_number+2 # estimated number of pieces to fill up mboaard to get to the well
    # +2 because testcases show that its better to be a bit pesimistic 
def count_minos(board, y1=0, y2=None):
    """
    Counts the number of minos (non-empty cells) on the board.
    Only counts rows from y1 (inclusive) to y2 (exclusive).
    y=0 is top, y=20 is bottom.
    """
    if y2 is None:
        y2 = len(board)
    return sum(cell != " " for row in board[y1:y2] for cell in row)

def hole_exists(board, x, y):
    assert 0 <= x <= 9
    assert 0 <= y <= 19

    return (y == 0 or board[y - 1][x] != " ") and board[y][x] == " "


def check_holes(board):
    total = 0

    for y in range(1, 20):
        total += sum(hole_exists(board, x, y) for x in range(10))
    return total


def check_holes2(board):
    total = 0
    for x in range(10):
        y = 1
        while y < 20 and board[y][x] == " ":
            y += 1
        y += 1
        while y < 20:
            if board[y][x] == " ":
                total += 1
            y += 1
    return total


def height_difference(board):
    """
    Calculates the maximum height difference between columns and returns heights.
    """
    height_array = []
    for col in range(10):
        for row in range(19, -1, -1):
            if board[row][col] == " ":
                height_array.append(19 - row)
                break
        if len(height_array) == col - 1:
            height_array.append(0)
    max_diff = max(height_array) - min(height_array)
    return max_diff, height_array


def uneven_stack_est(height_array):
    """
    Calculates the unevenness of a stack by summing absolute differences between adjacent heights.
    """
    if len(height_array) < 2:
        return 0.0

    uneven_sum = sum(
        abs(height_array[j] - height_array[j + 1]) for j in range(len(height_array) - 1)
    )
    return uneven_sum / (len(height_array) - 1)


def get_heights(board):
    heights = []
    for col in range(len(board[0])):
        for row in range(len(board)):
            if board[row][col] != " ":
                heights.append(len(board) - row)
                break
        else:
            heights.append(0)
    return heights

def find_highest_y(board):
    for y in range(len(board)):
        if any(cell != ' ' for cell in board[y]):
            return y
    return len(board)

def is_tetris_well(board):
    BOARD_HEIGHT = len(board)
    BOARD_WIDTH = len(board[0])
    empty_cells_array = [0] * BOARD_WIDTH
    
    for height, row in enumerate(board):
        empty_cols = [col for col in range(BOARD_WIDTH) if row[col] == " "]
        
        if len(empty_cols) == 1:
            col = empty_cols[0]
            for i in range(BOARD_WIDTH):
                if i == col:
                    empty_cells_array[i] += 1
                else:
                    empty_cells_array[i] = 0
        else:
            empty_cells_array = [0] * BOARD_WIDTH
            continue
        
        for col, count in enumerate(empty_cells_array):
            if count >= 4:
                well_top = height - count + 1
                
                left_ok = (col > 0) and any(board[y][col-1] != " " for y in range(BOARD_HEIGHT))
                right_ok = (col < BOARD_WIDTH-1) and any(board[y][col+1] != " " for y in range(BOARD_HEIGHT))
                
                if not (left_ok or right_ok):
                    continue
                
                minos_above = well_top  
                for y_above in range(well_top):
                    if board[y_above][col] != " ":
                        minos_above = well_top - y_above
                        break
                
                return True, col, well_top, minos_above
    
    return False, None, None, None
