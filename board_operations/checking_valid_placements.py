from shutil import copy
import sys
import os
from time import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# called by bruteforcer

def find_drop_height(board, xpos):
    """
    Finds the height at which a piece would land if dropped in the given column.
    """
    for y in range(len(board)):  
        if board[y][xpos] != ' ':  
            return y - 1  
    return len(board) - 1 # retuns last index of board, being 19 normally 

def can_place(piece, board, ypos, xpos, print_debug=True):
    """
    Checks if a piece can be placed at the given position on the board.
    """
    if print_debug:
        print(f"can_place check at x:{xpos}, y:{ypos} with piece:{piece}")
    for (dx, dy) in piece:
        x, y = xpos + dx, ypos + dy
        if y >= len(board) or x < 0 or x >= len(board[0]) or board[y][x] != ' ':
            return False
    brd,a = place_piece(piece, 'V', board, xpos, ypos, print_debug=False)  
    if print_debug: print_board(brd) 
    return True
def soft_drop_simulation(piece, board, col,print_ = False):
    """
    Simulates dropping a piece in the given column and returns a new board.
    Does not modify the original board.
    """
    board_copy = [row.copy() for row in board]  # deep copy
    row = 0
    while can_place(piece, board_copy, row + 1, col,print_):
        row += 1
    if row == 0: 
        return None
    board_copy = place_piece(piece, board_copy, row, col,print_)
    return board_copy
 # ^  this function doenst seem to do much so id remove it at some point when im done wtih spins ^ 
def soft_drop_simulation_returning_ypos(piece, board, col,print_ = False):
    """
    Simulates dropping a piece in the given column and returns a ypos of the piece after dropping.
    Does not modify the original board.
    """
    board_copy = [row.copy() for row in board]  # deep copy
    row = 0
    while can_place(piece, board_copy, row + 1, col,print_):
        row += 1
    if row == 0: 
        return 19
    
    return row
def find_lowest_y_for_piece(piece,board,col):
    board_copy = [row.copy() for row in board]
    row = 0
    while can_place(piece, board_copy, row + 1, col,print_debug=False):
        row += 1
        if can_place(piece, board_copy, row + 1, col,print_debug=False) == False:
            return row
    if row == 0: 
        return 20
    return row

def place_piece(piece_pos_array, piece_type, board, x, y, print_debug=True):
    """
    Places a piece on the board at the specified position.
    doesnt modify the board, needs to use returns now
    returns true or false if succeded or failed
    """
    if print_debug:
        print(f"x: {x},x len {len(board[0])-len(piece_pos_array)},y: {y},y len: {len(board)-len(piece_pos_array)}")
    assert 0 <= x <= len(board[0])-max(dx for dx, dy in piece_pos_array) - 1 , "x out of bounds"
    assert 0 <= y <= len(board) - max(dy for dx, dy in piece_pos_array) - 1, "y out of bounds"

    new_board = [row.copy() for row in board]
    old_board = [row.copy() for row in board]
    #piece_tuple_array = PIECES_index[piece_pos_array[0]][piece_pos_array[1]]
    for (dx,dy) in piece_pos_array:
        if print_debug:
            print(x + dx, y + dy, "place piece", piece_type, "<-")
        if new_board[y + dy][x + dx] == ' ':
                new_board[y + dy][x + dx] = piece_type
                if print_debug:
                    print('placing piece at:', x + dx, y + dy)
                #print_board(new_board)
        else:
            if print_debug:
                print('returning old board cuz piece cant be placed, failed at :', x + dx, y + dy)
            return old_board,False
    return new_board , True
def can_place2(piece, board, xpos, ypos):
    """
    Places a piece on the board at the specified position.
    doesnt modify the board, needs to use returns now
    """
    rows = len(board)
    cols = len(board[0])
    piece_h = len(piece)
    piece_w = len(piece[0])
    # bounds check
    if xpos < 0 or ypos < 0 or xpos + piece_h > rows or ypos + piece_w > cols:
        return False # ^ this can be replaces with assert
    # collision check
    for (dx,dy) in piece:
            if board[xpos + dy][ypos + dx] != ' ':
                return False
    return True
from utility.pieces_index import PIECES_index
from utility.print_board import print_board
from utility.pieces import *
def sideways_movement_simulation(board, piece, rotation, x_pos, y_pos, piece_info_array):
    '''returns array'''
    # if one position after softdrop unlocks every x pos (for example with a flat board)
    # you can use formula 10- width of block, and if in one for loop, 10-width entries were added
    # into piece_info_array, that means that we have a flat board and we DO NOT need to go through
    # every single x position, just that one on the same y level
    
    #from utility.pieces import PIECES
    piece_val  = piece# like 'T' or 'L' neede dlater
    piece = PIECES_index[piece][rotation]
    #print(piece)
    piece_width = get_piece_width(piece)
    #print(piece_width)
    piece_info_arrays_array = []
    col_x = x_pos
    while col_x > 0:
        if not can_place2(piece, board, y_pos, col_x - 1):
            break
        col_x -= 1
        entry = [piece_val, rotation, col_x, y_pos]
        if entry not in piece_info_arrays_array:
            piece_info_arrays_array.append(entry)
        
    col_x = x_pos
    while col_x < 10 - piece_width:
        if not can_place2(piece, board, y_pos, col_x + 1):
            break
        col_x += 1
        entry = [piece_val, rotation, col_x, y_pos]
        if entry not in piece_info_arrays_array:
            piece_info_arrays_array.append(entry)
    print(piece_info_arrays_array)
    return  piece_info_arrays_array
    # position array is array that has:
    # [rotation,y_pos], its with a purpose to keep track of branches and not run into infinite loops
    # if one of the branch will yeald a result we already got higher, we can omit that immediately

def get_piece_width(piece):
    '''returns the piece width in int'''
    min_x = min(dx for dx, dy in piece)  
    max_x = max(dx for dx, dy in piece)  
    piece_width = max_x - min_x + 1  
    return piece_width

def get_piece_height(piece):   
    '''returns the piece height in int'''
    min_y = min(dy for dx, dy in piece)  
    max_y = max(dy for dx, dy in piece)  
    piece_height = max_y - min_y + 1  
    return piece_height

def get_piece_lowest_index_from_origin(piece):
    '''this function returns the lowest Y from the origin of piece (0,0), [1,1]'''
    min_y = max(dy for dx, dy in piece)  
    return min_y

def get_piece_leftmost_index_from_origin(piece):
    '''this function returns the leftmost X from the origin of piece (0,0), [1,1]'''
    min_x = min(dx for dx, dy in piece)  
    return min_x

def get_piece_rightmost_index_from_origin(piece):
    '''this function returns the rightmost X from the origin of piece (0,0), [1,1]'''
    max_x = max(dx for dx, dy in piece)  
    return max_x