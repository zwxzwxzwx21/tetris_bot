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

def can_place(piece, board, row, col):
    """
    Checks if a piece can be placed at the given position on the board.
    """
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                y, x = row + dy, col + dx
                if y >= len(board) or x < 0 or x >= len(board[0]) or board[y][x] != ' ':
                    return False
    return True

def soft_drop_simulation(piece, board, col):
    """
    Simulates dropping a piece in the given column and returns a new board.
    Does not modify the original board.
    """
    board_copy = [row.copy() for row in board]  # deep copy
    row = 0
    while can_place(piece, board_copy, row + 1, col):
        row += 1
    if row == 0: 
        return None
    board_copy = place_piece(piece, board_copy, row, col)
    return board_copy
 # ^  this function doenst seem to do much so id remove it at some point when im done wtih spins ^ 

def find_lowest_y_for_piece(piece,board,col):
    board_copy = [row.copy() for row in board]
    row = 0
    while can_place(piece, board_copy, row + 1, col):
        row += 1
    if row == 0: 
        return 20
    return row

def place_piece(piece, board, x, y):
    """
    Places a piece on the board at the specified position.
    doesnt modify the board, needs to use returns now
    returns true or false if succeded or failed
    """
    print(f"x: {x},x len {len(board[0])-len(piece)},y: {y},y len: {len(board)-len(piece)}")
    assert 0 <= x <= len(board[0])-len(piece) , "x out of bounds"
    assert 0 <= y <= len(board)- len(piece) , "y out of bounds" # maybe error
    
    new_board = [row.copy() for row in board]
    old_board = [row.copy() for row in board]
    for dx, piece_row in enumerate(piece):
        for dy, cell in enumerate(piece_row):
                print(x + dx, y + dy, "place piece", cell, "<-")
                if new_board[x + dx][y + dy] == ' ':
                    if cell != ' ':
                        new_board[x + dx][y + dy] = cell
                        print('placing piece at:', x + dx, y + dy)
                    print_board(new_board)
                elif new_board[x + dx][y + dy] != ' ' and cell == ' ':
                    pass # ? 
                else:
                    
                    print('returning old board cuz piece cant be placed, failed at :', x + dx, y + dy)
                    return old_board,False
    return new_board , True
def can_place2(piece, board, x, y):
    """
    Places a piece on the board at the specified position.
    doesnt modify the board, needs to use returns now
    """
    rows = len(board)
    cols = len(board[0])
    piece_h = len(piece)
    piece_w = len(piece[0])
    # bounds check
    if x < 0 or y < 0 or x + piece_h > rows or y + piece_w > cols:
        return False
    # collision check
    for dy, prow in enumerate(piece):
        for dx, cell in enumerate(prow):
            if cell != ' ' and board[x + dy][y + dx] != ' ':
                return False
    return True
from utility.print_board import print_board
from utility.pieces import *
def sideways_movement_simulation(board,piece,rotation,x_pos,y_pos,piece_info_array):
    # if one position after softdrop unlocks every x pos (for example with a flat board)
    # you can use formula 10- width of block, and if in one for loop, 10-width entries were added
    # into piece_info_array, that means that we have a flat board and we DO NOT need to go through
    # every single x position, just that one on the same y level
    
    from utility.pieces import PIECES
    piece_val  = piece# like 'T' or 'L' neede dlater
    piece = PIECES[piece][rotation]
    #print(piece)
    piece_width = len(piece[0])
    #print(piece_width)

    col_x = x_pos
    while col_x > 0:
        if not can_place2(piece, board, y_pos, col_x - 1):
            break
        col_x -= 1
        entry = [piece_val, rotation, col_x, y_pos]
        if entry not in piece_info_array:
            piece_info_array.append(entry)
        
    col_x = x_pos
    while col_x < 10 - piece_width:
        if not can_place2(piece, board, y_pos, col_x + 1):
            break
        col_x += 1
        entry = [piece_val, rotation, col_x, y_pos]
        if entry not in piece_info_array:
            piece_info_array.append(entry)
    print(piece_info_array)
    return piece_info_array
    # position array is array that has:
    # [rotation,y_pos], its with a purpose to keep track of branches and not run into infinite loops
    # if one of the branch will yeald a result we already got higher, we can omit that immediately

