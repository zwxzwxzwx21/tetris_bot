from logging import config
from pprint import pp
import pandas as pd
from heuristic import analyze

from board_operations.board_operations import clear_lines
from board_operations.stack_checking import (
    check_holes2,
    get_heights,
    uneven_stack_est,
)
from tetrio_parsing.calculate_attack import count_lines_clear
from utility.print_board import print_board, debug_print
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

def loss(board, cleared_lines) -> float:
    return analyze(board,cleared_lines)

# MAKE SPINS RECOGNIZABLE
# mark kicks as spins and whenever one is performed, set a flag that a spin was done, this will be used for btb

def find_best_placement(board, queue, combo,stats,held_piece):
    move_history = []
    GAMEOVER = False
    best_move = None
    total_lines = 0
     
    best_loss = -999999

    arr_piece_info_array = []
    list_of_best_moves = []
    held_piece_checked_loop = 0 # if there is no held piece, we only check once
    max_piece_loops = 1 if held_piece is None else 2
    while held_piece_checked_loop < max_piece_loops: # i dont know if bool works, we have to check twice and do while doesnt exist in python
        
        current_piece = queue[0] if held_piece_checked_loop == 0 else held_piece
        debug_print(f"CURRENT PIECE: {current_piece} held piece: {held_piece} loop: {held_piece_checked_loop}", "bruteforcing.py, function: find_best_placement")
        print("current piece:", current_piece, "loop:", held_piece_checked_loop)
        assert current_piece in PIECES_index
        
        for rotation_name, piece_pos_array  in PIECES_index[current_piece].items():
            
            # o piece has no rotation so we just set values 
            start_x_pos = PIECES_startpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 1
            finish_x_pos = 11-PIECES_xpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 9
            #check all positions from the position we can place the piece on downwards,  if there is a place for a piece
            # add it to arrayt and see what results it gives (it may be inaccesible)
            for start_x in range(start_x_pos,finish_x_pos):
                
                lowest_y = find_lowest_y_for_piece(PIECES_index[current_piece][rotation_name], board, start_x,rotation_name,current_piece)

                for y in range(lowest_y-0, 21):  
                    if can_place(PIECES_index[current_piece][rotation_name], board, y, start_x,rotation_name,current_piece,print_debug=False):

                            arr_piece_info_array.append([current_piece, rotation_name, start_x, y])
        held_piece_checked_loop += 1
            
    for position_info in arr_piece_info_array:
        
        new_board, is_place_piece_successful = place_piece(PIECES_index[position_info[0]][position_info[1]],position_info[0], board, position_info[2], position_info[3], position_info[1],print_debug=False,where_called_from="bruteforcing, fuycntion: try best placement")
        if not is_place_piece_successful:
            debug_print(f"GAMEOVER, score (best loss) : {best_loss} ", "bruteforcing.py, function: find_best_placement")
            GAMEOVER = True
            break
        board_after_clear, cleared_lines = clear_lines(new_board)
        debug_print("cleared lines:", cleared_lines, "bruteforcing.py, function: find_best_placement")
        # piece info array example ("T",'flat_0',x(fore xample 4),y(for example 15))
        
        print(loss(board_after_clear, cleared_lines),position_info)
        if (current_loss := loss(board_after_clear, cleared_lines)) > best_loss:
            best_move = f"{position_info[0]}_x{position_info[2]}_{position_info[1]}"
            best_move_y_pos = position_info[3]
            move_history = [best_move]
            best_loss = current_loss
            total_lines += cleared_lines
            debug_print("UPDATED BEST MOVE TO:", best_move, " with loss: ", best_loss, "bruteforcing.py, function: find_best_placement")
            list_of_best_moves.append((best_move, best_move_y_pos))
        

    debug_print("\n")
    if GAMEOVER:
            
        return None
    assert move_history
    
    debug_print(f"best move: {best_move} with loss: {best_loss}", "bruteforcing.py, function: find_best_placement")
    print(list_of_best_moves, "bruteforcing.py, function: find_best_placement")
    # taking all the best moves and finding the sequence that leads to it, if it doesnt exist, we check the first one that does 
    for best_move_from_list, best_move_y_position in reversed(list_of_best_moves):
        print(f"attempting to find sequence for best move: {best_move_from_list} at y pos {best_move_y_position}", "bruteforcing.py, function: find_best_placement")
        
        if best_move_from_list is not None:
            goal_string = best_move_from_list
            sequence = search_for_best_move(goal_string, board, best_move_y_position)
            print("this is the sequence for:",goal_string,sequence) # this we dont debug print
            if sequence is not None:
                used_hold = best_move_from_list[0] == held_piece
                return move_history, best_move_from_list,best_move_y_position, used_hold
    return None