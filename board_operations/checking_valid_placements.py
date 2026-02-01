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

def can_place(piece_pos_array, board, ypos, xpos,rotation, piece,print_debug=False):
    """
    Checks if a piece can be placed at the given position on the board.
    """
    if print_debug:
        print(f"can_place check at x:{xpos}, y:{ypos} with piece:{piece_pos_array}")
    for (dx, dy) in piece_pos_array:
        x, y = xpos + dx, ypos + dy
        if y >= len(board) or x < 0 or x >= len(board[0]) or board[y][x] != ' ':
            return False
    brd,a = place_piece(piece_pos_array, piece, board, xpos, ypos, rotation ,print_debug=False,where_called_from="can_place in checking valid placements")  
    if print_debug: print_board(brd) 
    return True
 
def soft_drop_simulation_returning_ypos(piece_index_array, board, col,rotate,piece,print_ = False):
    """
    Simulates dropping a piece in the given column and returns a ypos of the piece after dropping.
    Does not modify the original board.
    """
    board_copy = [row.copy() for row in board]  # deep copy
    row = 0
    while can_place(piece_index_array, board_copy, row + 1, col, rotate,piece,print_):
        row += 1
    if row == 0: 
        return 19
    
    return row

def find_lowest_y_for_piece(piece_index_array,board,col,rotation,piece ):
    board_copy = [row.copy() for row in board]
    row = 0
    
    #print(can_place(piece_index_array, board_copy, row + 1, col,rotation,piece,print_debug=False))
    while can_place(piece_index_array, board_copy, row + 1, col,rotation,piece,print_debug=False):
        row += 1
        if can_place(piece_index_array, board_copy, row + 1, col,rotation,piece,print_debug=False) == False:
            return row
    if row == 0: 
        return 0
    return row

from utility.pieces_index import PIECES_lowest_point_from_origin, PIECES_startpos_indexing_value, PIECES_xpos_indexing_value
def place_piece(piece_index_array, piece, board, x, y,rotation, print_debug=False,where_called_from=""):

    """
    Places a piece on the board at the specified position.
    doesnt modify the board, needs to use returns now
    returns true or false if succeded or failed
    """
    
    if PIECES_startpos_indexing_value[piece][rotation] > x or x > len(board[0])-1-get_piece_rightmost_index_from_origin(PIECES_index[piece][rotation]):
        #print(f"x out of bounds {x} max available:{len(board[0])-get_piece_rightmost_index_from_origin(PIECES_index[piece][rotation])}")
        #print("if1 args causing error: ",piece_index_array, piece, x, y,rotation, where_called_from)
        
        return board,False
    if 0 > y or y > len(board) - PIECES_lowest_point_from_origin[piece][rotation]:
        #print(f"y out of bounds {y} max available:{len(board)-get_piece_height(piece_index_array)+1}")
        #print("if2 args causing error: ",piece_index_array, piece, board, x, y,rotation)
        return board,False
    new_board = [row.copy() for row in board]
    old_board = [row.copy() for row in board]

    for (dx,dy) in piece_index_array:

        if print_debug:
            print(x + dx, y + dy, "place piece", piece, "<-")

        #print(f"y= {y} + {dy} = {y + dy} x= {x} + {dx} = {x + dx}")
        if 0 <= x + dx < 10 and 0 <= y + dy < 20:   
            if new_board[y + dy][x + dx] == ' ':
                new_board[y + dy][x + dx] = piece
                if print_debug:
                    print('placing piece at:', x + dx, y + dy)
            else:
                if print_debug:
                    print('returning old board cuz piece cant be placed, failed at :', x + dx, y + dy)
                return old_board ,False
        else:
            if print_debug:
                print('returning old board cuz piece cant be placed, failed at :', x + dx, y + dy)
            return None ,False
        
    if y > 17:
        if print_debug:
            print_board(new_board) 
    return new_board , True
def can_place2(piece, board, xpos, ypos,side):
    """
    Places a piece on the board at the specified position.
    doesnt modify the board, needs to use returns now
    """

    for (dx,dy) in piece:

            try:
                if board[ypos + dy][xpos + dx] != ' ':
                    return False
            except IndexError:
                return False
    return True
from utility.pieces_index import PIECES_index
from utility.print_board import print_board
from utility.pieces import *
def sideways_movement_simulation(board, piece, rotation, x_pos, y_pos, piece_info_array):
    '''returns array'''
    #this shit broken as hell wuuh
    piece_val  = piece # like 'T' or 'L' needed later
    piece_index_array = PIECES_index[piece][rotation]
    piece_info_arrays_array = []
    col_x = x_pos

    while col_x + get_piece_leftmost_index_from_origin(piece_index_array) > 0:
        side = "to_left"

        if not can_place2(piece_index_array, board, col_x - 1,y_pos, side):
            break

        col_x -= 1
        entry = [piece_val, rotation, col_x, y_pos]
        if entry not in piece_info_arrays_array:
            piece_info_arrays_array.append(entry)
        
    col_x = x_pos
    while col_x < 10 - get_piece_rightmost_index_from_origin(piece_index_array):
        side = "to_right"

        if not can_place2(piece_index_array, board, col_x + 1, y_pos, side):
            break

        col_x += 1
        entry = [piece_val, rotation, col_x, y_pos]
        if entry not in piece_info_arrays_array:
            piece_info_arrays_array.append(entry)
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

def get_piece_lowest_index_from_origin_abs(piece):
    '''this function returns the lowest Y from the origin of piece (0,0), [1,1]'''
    min_y = max(dy for dx, dy in piece)  
    
    return min_y

def get_piece_leftmost_index_from_origin_abs(piece):
    '''this function returns the leftmost X from the origin of piece (0,0), [1,1]'''
    min_x = min(dx for dx, dy in piece)  
    
    return min_x

def get_piece_rightmost_index_from_origin_abs(piece):
    '''this function returns the rightmost X from the origin of piece (0,0), [1,1]'''
    max_x = max(dx for dx, dy in piece)  
    
    return max_x