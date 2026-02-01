import copy
from logging import config
from pprint import pp
import time
import random
import pandas as pd
import os
import config

from board_operations.board_operations import clear_lines
from board_operations.stack_checking import (
    check_holes2,
    get_heights,
    uneven_stack_est,
)
from tetrio_parsing.calculate_attack import count_lines_clear
from utility.print_board import print_board
from utility.pieces import PIECES, PIECES_soft_drop
from utility.pieces_index import PIECES_index, PIECES_xpos_indexing_value, PIECES_startpos_indexing_value

from search_for_best_move import search_for_best_move

from board_operations.checking_valid_placements import find_lowest_y_for_piece, can_place, place_piece,get_piece_leftmost_index_from_origin,get_piece_rightmost_index_from_origin,get_piece_height,get_piece_lowest_index_from_origin,get_piece_width

DEBUG = True

rotations = {
    "I": ["flat", "spin"],
    "O": ["flat"],
    "S": ["flat", "spin"],
    "Z": ["flat", "spin"],
    "L": ["flat", "180", "cw", "ccw"],
    "J": ["flat", "180", "cw", "ccw"],
    "T": ["flat", "180", "cw", "ccw"],
}


MOVES_DONE = 0
MOVES_REMOVED = 0
TIME_LIMIT = 999
UNEVEN_THRESHOLD = 1.1  
MAX_HEIGHT_DIFF = 6 
BRUTEFORCE_MODE = False

from heuristic import analyze
def loss(board, cleared_lines) -> float:
    return analyze(board,cleared_lines)

def find_best_placement(board, queue, combo, stats,held_piece):
    move_history = []
    GAMEOVER = False
    spin = False
    best_move = None
    total_lines = 0
     
    best_loss = -999999

    arr_piece_info_array = []
    list_of_best_moves = []
    current_piece = queue[0]
    assert current_piece in PIECES_index
    loop = 0
    
    for rotation_name, piece_pos_array  in PIECES_index[current_piece].items():
        
        temp_array = []
        #print((PIECES_startpos_indexing_value[current_piece][rotation_name],11-PIECES_xpos_indexing_value[current_piece][rotation_name]))
        start_x_pos = PIECES_startpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 1
        finish_x_pos = 11-PIECES_xpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 9
        for start_x in range(start_x_pos,finish_x_pos):
            
            lowest_y = find_lowest_y_for_piece(PIECES_index[current_piece][rotation_name], board, start_x,rotation_name,current_piece)

            for y in range(lowest_y-0, 21):  
                if can_place(PIECES_index[current_piece][rotation_name], board, y, start_x,rotation_name,current_piece,print_debug=False):

                        arr_piece_info_array.append([current_piece, rotation_name, start_x, y])
                        temp_array.append([current_piece, rotation_name, start_x, y])
    
        
    for position_info in arr_piece_info_array:
        
        new_board, is_place_piece_successful = place_piece(PIECES_index[position_info[0]][position_info[1]],position_info[0], board, position_info[2], position_info[3], position_info[1],print_debug=False,where_called_from="bruteforcing, fuycntion: try best placement")
        if not is_place_piece_successful:
            if config.PRINT_MODE:
                print(f"GAMEOVER, score (best loss) : {best_loss} ")
            GAMEOVER = True
            break
        board_after_clear, cleared_lines = clear_lines(new_board)
        if config.PRINT_MODE:
            print("cleared lines:", cleared_lines)
        # piece info array example ("T",'flat_0',x(fore xample 4),y(for example 15))
        
        # FIXED: evaluate board_after_clear, not new_board!
        print(loss(board_after_clear, cleared_lines),current_piece,position_info)
        if (current_loss := loss(board_after_clear, cleared_lines)) > best_loss:
            best_move = f"{position_info[0]}_x{position_info[2]}_{position_info[1]}"
            best_move_y_pos = position_info[3]
            move_history = [best_move]
            best_loss = current_loss
            total_lines += cleared_lines
            if config.PRINT_MODE:
                print("UPDATED BEST MOVE TO:", best_move, " with loss: ", best_loss)
            list_of_best_moves.append((best_move, best_move_y_pos))
    
    if held_piece is not None: 
        current_piece = held_piece
        print("TRYING WITH HELD PIECE:", current_piece)
        for rotation_name, piece_pos_array  in PIECES_index[current_piece].items():
        
            temp_array = []
            #print((PIECES_startpos_indexing_value[current_piece][rotation_name],11-PIECES_xpos_indexing_value[current_piece][rotation_name]))
            start_x_pos = PIECES_startpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 1
            finish_x_pos = 11-PIECES_xpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 9
            for start_x in range(start_x_pos,finish_x_pos):
                
                lowest_y = find_lowest_y_for_piece(PIECES_index[current_piece][rotation_name], board, start_x,rotation_name,current_piece)

                for y in range(lowest_y+1, 21):  
                    if can_place(PIECES_index[current_piece][rotation_name], board, y, start_x,rotation_name,current_piece,print_debug=False):

                            arr_piece_info_array.append([current_piece, rotation_name, start_x, y])
                            temp_array.append([current_piece, rotation_name, start_x, y])
        
        print(arr_piece_info_array)
        for position_info in arr_piece_info_array:
            
            new_board, is_place_piece_successful = place_piece(PIECES_index[position_info[0]][position_info[1]],position_info[0], board, position_info[2], position_info[3], position_info[1],print_debug=False,where_called_from="bruteforcing, fuycntion: try best placement")
            if not is_place_piece_successful:
                if config.PRINT_MODE:
                    print(f"GAMEOVER, score (best loss) : {best_loss} ")
                GAMEOVER = True
                break
            board_after_clear, cleared_lines = clear_lines(new_board)
            if config.PRINT_MODE:
                print("cleared lines:", cleared_lines)
            # piece info array example ("T",'flat_0',x(fore xample 4),y(for example 15))
            
            # FIXED: evaluate board_after_clear, not new_board!
            print(loss(board_after_clear, cleared_lines),current_piece,position_info)
            if (current_loss := loss(board_after_clear, cleared_lines)) > best_loss:
                best_move = f"{position_info[0]}_x{position_info[2]}_{position_info[1]}"
                best_move_y_pos = position_info[3]
                move_history = [best_move]
                best_loss = current_loss
                total_lines += cleared_lines
                if config.PRINT_MODE:
                    print("UPDATED BEST MOVE TO:", best_move, " with loss: ", best_loss)
                list_of_best_moves.append((best_move, best_move_y_pos))

    if config.PRINT_MODE:
        print()
    if GAMEOVER:
        lines_cleared = (stats.single + stats.double + stats.triple + stats.tetris)
         # ?
            
        return None
    assert move_history
    if config.PRINT_MODE:
        print(f"best move: {best_move} with loss: {best_loss}")
        print(list_of_best_moves)
    for best_move_from_list, best_move_y_position in reversed(list_of_best_moves):
        if config.PRINT_MODE:
            print(f"attempting to find sequence for best move: {best_move_from_list} at y pos {best_move_y_position}")
        
        if best_move_from_list is not None:
            goal_string = best_move_from_list
            sequence = search_for_best_move(goal_string, board, best_move_y_position)
            print("this is the sequence for:",goal_string,sequence)
            if sequence is not None:
                return move_history, best_move_from_list,best_move_y_position
    return None