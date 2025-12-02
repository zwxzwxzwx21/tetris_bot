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
values = {
    "uneven_loss": {"default": 1, "max": 100},
    "holes_punishment": {"default": 2.5, "max": 100},
    "height_diff_punishment": {"default": 3, "max": 100},
    "attack_bonus": {"default": 0, "max": 100},
    "max_height_punishment": {"default": 0.5, "max": 100}
    
}

for vals, configs in values.items():
    value = random.uniform(0, configs["max"]) if BRUTEFORCE_MODE else configs["default"]
    globals()[vals] = value
if config.PRINT_MODE:
    print(
    f"uneven_loss: {uneven_loss}, holes_punishment: {holes_punishment}, height_diff_punishment: {height_diff_punishment}, attack_bonus: {attack_bonus}" # type: ignore
)

def loss(feature: dict, uneven_loss, holes_punishment, height_diff_punishment, attack_bonus, max_height_punishment) -> float:
    if config.PRINT_MODE:
        print("feature in loss function:", feature)
        print("feature values:", feature["uneven"], feature["holes"], feature["different_heights"], feature["attack"][0], feature["max_height"])
        print("calculating loss with values:", "uneven_loss:", uneven_loss*feature["uneven"], "holes_punishment:", holes_punishment*feature["holes"], "height_diff_punishment:", height_diff_punishment*feature["different_heights"], "attack_bonus:", attack_bonus*feature["attack"][0], "max_height_punishment:", max_height_punishment*max(feature["max_height"] - 4, 0))
        print("uneven_loss * feature[uneven] => ",uneven_loss," * " ,feature["uneven"]," ", uneven_loss * feature["uneven"])
        print("holes_punishment * feature[holes] => ",holes_punishment," * " ,feature["holes"]," ", holes_punishment * feature["holes"])
        print("height_diff_punishment * feature[different_heights] => ",height_diff_punishment," * " ,feature["different_heights"]," ", height_diff_punishment * feature["different_heights"])
        print("max_height_punishment * max(feature[max_height] - 4, 0) => ",max_height_punishment," * " ,max(feature["max_height"] - 4, 0)," ", max_height_punishment * max(feature["max_height"] - 4, 0))
        print("attack_bonus * feature[attack][0] => ",attack_bonus," * " ,feature["attack"][0]," ", attack_bonus * feature["attack"][0])
    return (
        uneven_loss * feature["uneven"]
        + holes_punishment * feature["holes"]
        + height_diff_punishment * feature["different_heights"]
        + max_height_punishment * max(feature["max_height"] - 4, 0) 
        - attack_bonus * feature["attack"][0]
    )

def find_best_placement(board, queue, combo, stats):
    move_history = []
    GAMEOVER = False
    spin = False
    check_sideways = False
    best_move = None
    total_lines = 0
    total_attack = 0
    feature = {
        "uneven": 2,
        "holes": 10,
        #"height_diff": 0.08169,
        "max_height": 0.1,
        "different_heights": 1.2,
        "attack": 1,
    }
    feature_backup = {
        "uneven": 1.5035,
        "holes": 1.411334,
        "height_diff": 0.08169,
        "max_height": 0.45217,
        "different_heights": 1,
        "attack": 2.313,
    }
     
    best_feature = feature.copy()
    best_loss = 10000

    arr_piece_info_array = []

    current_piece = queue[0]
    assert current_piece in PIECES_index
    for rotation_name, piece_pos_array  in PIECES_index[current_piece].items():
        
        temp_array = []
        print((PIECES_startpos_indexing_value[current_piece][rotation_name],11-PIECES_xpos_indexing_value[current_piece][rotation_name]))
        start_x_pos = PIECES_startpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 1
        finish_x_pos = 11-PIECES_xpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 9
        for start_x in range(start_x_pos,finish_x_pos):
            
            lowest_y = find_lowest_y_for_piece(PIECES_index[current_piece][rotation_name], board, start_x,rotation_name,current_piece)

            for y in range(lowest_y, 20):       
                if can_place(PIECES_index[current_piece][rotation_name], board, y, start_x,rotation_name,current_piece,print_debug=False):

                    arr_piece_info_array.append([current_piece, rotation_name, start_x, y])
                    temp_array.append([current_piece, rotation_name, start_x, y])
    
    for position_info in arr_piece_info_array:
        '''reachable_position = False
        
        if search_for_best_move(position_info,board,best_move_y_pos) is not None:
                print("verified best move found in search_for_best_move, {}".format(best_move))
                reachable_position = True
        else:
            best_move = None  # reset best move if not found in search
        if reachable_position == False:
            continue'''
        new_board, is_place_piece_successful = place_piece(PIECES_index[position_info[0]][position_info[1]],position_info[0], board, position_info[2], position_info[3], position_info[1],print_debug=False)
        if not is_place_piece_successful:
            if config.PRINT_MODE:
                print(f"GAMEOVER, score (best loss) : {best_loss} ")
            GAMEOVER = True
            break
        board_after_clear, cleared_lines = clear_lines(new_board)
        # piece info array example ("T",'flat_0',x(fore xample 4),y(for example 15))
        heights = get_heights(board_after_clear)
        feature["max_height"] = max(heights)
        feature["uneven"] = int(uneven_stack_est(heights))
        feature["holes"] = check_holes2(board_after_clear)
        feature["different_heights"] = sum(
            heights[x] != heights[x + 1] for x in range(len(heights) - 1)
        )
        feature["attack"] = count_lines_clear(cleared_lines, combo, board_after_clear)
        print_board(board_after_clear)
        print(position_info)
        if (current_loss := loss(feature, uneven_loss, holes_punishment,  # type: ignore
                                height_diff_punishment, attack_bonus, max_height_punishment)) < best_loss:# type: ignore
            #best_move = f"{current_piece}_x{start_x}_{rotation_name}"
            best_move = f"{position_info[0]}_x{position_info[2]}_{position_info[1]}"
            best_move_y_pos = position_info[3]
            move_history = [best_move]
            best_loss = current_loss
            best_feature = feature
            total_attack += feature["attack"][0]
            total_lines += cleared_lines
            print("UPDATED BEST MOVE TO:", best_move, " with loss: ", best_loss)
            
            
    if config.PRINT_MODE:
        pp(best_feature)
    if config.PRINT_MODE:
        print()
    if GAMEOVER:
        lines_cleared = (stats.single + stats.double + stats.triple + stats.tetris)
        if config.PRINT_MODE:
            print(
            f"DATA: \n uneven_loss: {uneven_loss},\n holes_punishment: {holes_punishment},\n" # type: ignore
            f"height_diff_punishment: {height_diff_punishment},\n attack_bonus: {attack_bonus},\n"# type: ignore
            f"max_height_punishment: {max_height_punishment}\n cleared lines: {lines_cleared}\n"# type: ignore
            f"total attack: {stats.total_attack}\n"
        )
            
        return None
    assert move_history
    print(f"best move: {best_move} with loss: {best_loss}")
    return move_history, best_move,best_move_y_pos
