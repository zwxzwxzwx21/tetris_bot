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

def place_piece(piece, board, row, col):
    """
    Places a piece on the board at the specified position.
    doesnt modify the board, needs to use returns now
    """
    new_board = [row.copy() for row in board]
    old_board = [row.copy() for row in board]
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if new_board[row + dy][col + dx] == ' ':
                if cell != ' ':
                    new_board[row + dy][col + dx] = cell
                    #print('placing piece at:', row + dy, col + dx)
                
            elif new_board[row + dy][col + dx] != ' ' and cell == ' ':
                continue
            else:
                
                print('returning old board cuz piece cant be placed, failed at :', row + dy, col + dx)
                return old_board
    return new_board 
def can_place2(piece, board, row, col):
    """
    Places a piece on the board at the specified position.
    doesnt modify the board, needs to use returns now
    """
    new_board = [row.copy() for row in board]
    old_board = [row.copy() for row in board]
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if new_board[row + dy][col + dx] == ' ':
                if cell != ' ':
                    new_board[row + dy][col + dx] = cell
                    #print('placing piece at:', row + dy, col + dx)
                
            elif new_board[row + dy][col + dx] != ' ' and cell == ' ':
                continue
            else:
                
                print('returning old board cuz piece cant be placed, failed at :', row + dy, col + dx)
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
    row = x_pos
    max_left,max_right = False, False
    assert -1 < row < 11 # that HAJS to be wtohng
    while max_left == False:
        #tseting
        brd = [row.copy() for row in board]
        
        can_move_left = can_place2(piece, board, y_pos, row - 1)
        brd = place_piece(piece, brd, y_pos, row)

        #print_board(brd)
        #print("----")

        while can_move_left and -1 < row < 11:
            can_move_left = can_place2(piece, board, y_pos, row - 1)
            print(can_move_left, row)
            row -= 1
            if [piece_val, rotation, row, y_pos] not in piece_info_array:
                piece_info_array.append([piece_val, rotation, row, y_pos])
                print(f" from position x:{row} can move to left to x:{row-1}")
            brd = [row.copy() for row in board]
            brd = place_piece(piece, brd, y_pos, row)

            print_board(brd)
            print("----")
                
        max_left = True
        
        if not can_move_left:
            break

    '''while max_left == False and max_right == False:
        #tseting
        brd = [row.copy() for row in board]
        
        can_move_left = can_place(piece, board, y_pos, row - 1)
        brd = place_piece(piece, brd, y_pos, row)
        brd2 = [row.copy() for row in board]
        can_move_right = can_place(piece, board, y_pos, row + 1)
        brd2 = place_piece(piece, brd2, y_pos, row + 1)
        print_board(brd)
        print("----")
        print_board(brd2)
        
        while can_move_left and -1 < row < 11:
            row -= 1
            if [piece_val, rotation, row, y_pos] not in piece_info_array:
                piece_info_array.append([piece_val, rotation, row, y_pos])
                print(f" from position x:{row} can move to left to x:{row-1}")
                
        max_left = True
        while can_move_right and -1 < row < 11:
            row += 1
            if [piece_val, rotation, row, y_pos] not in piece_info_array:
                piece_info_array.append([piece_val, rotation, row, y_pos])
                print(f" from position x:{row} can move to right to x:{row+1}")
        max_right = True
        if not can_move_left and not can_move_right:
            break'''
    print(piece_info_array)
    return piece_info_array
    # position array is array that has:
    # [rotation,y_pos], its with a purpose to keep track of branches and not run into infinite loops
    # if one of the branch will yeald a result we already got higher, we can omit that immediately

