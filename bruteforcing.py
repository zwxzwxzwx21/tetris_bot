import copy
from logging import config
from pprint import pp
import time
from board_operations.board_operations import clear_lines
from board_operations.checking_valid_placements import can_place, soft_drop_simulation
from board_operations.stack_checking import (
    check_holes2,
    get_heights,
    uneven_stack_est,
)
from tetrio_parsing.calculate_attack import count_lines_clear
from utility.pieces import PIECES, PIECES_soft_drop
from utility.pieces_index import PIECES_index, PIECES_xpos_indexing_value, PIECES_startpos_indexing_value

import pandas as pd
import os

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
import random

MOVES_DONE = 0
MOVES_REMOVED = 0
TIME_LIMIT = 999
UNEVEN_THRESHOLD = 1.1  
MAX_HEIGHT_DIFF = 6 
BRUTEFORCE_MODE = False
import config
values = {
    "uneven_loss": {"default": 0.4, "max": 100},
    "holes_punishment": {"default": 2, "max": 100},
    "height_diff_punishment": {"default": 0.05, "max": 100},
    "attack_bonus": {"default": 0, "max": 100},
    "max_height_punishment": {"default": 1, "max": 100}
}

for vals, configs in values.items():
    value = random.uniform(0, configs["max"]) if BRUTEFORCE_MODE else configs["default"]
    globals()[vals] = value
if config.PRINT_MODE:
    print(
    f"uneven_loss: {uneven_loss}, holes_punishment: {holes_punishment}, height_diff_punishment: {height_diff_punishment}, attack_bonus: {attack_bonus}" # type: ignore
)
def loss(feature: dict, uneven_loss, holes_punishment, height_diff_punishment, attack_bonus, max_height_punishment) -> float:
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
        "uneven": 0,
        "holes": 0,
        "height_diff": 0,
        "max_height": 20,
        "different_heights": 30,
        "attack": 0,
    }

    from spins_funcions import simulate_kicks
    from board_operations.checking_valid_placements import find_lowest_y_for_piece, soft_drop_simulation,get_piece_leftmost_index_from_origin,get_piece_rightmost_index_from_origin,get_piece_height,get_piece_lowest_index_from_origin,get_piece_width
            
    best_feature = feature.copy()
    best_loss = 10000

    arr_piece_info_array = []

    current_piece = queue[0]
    assert current_piece in PIECES_index
    # 
    for rotation_name, piece_pos_array in PIECES_index[current_piece].items():
        
        piece_width = get_piece_width(PIECES_index[current_piece][rotation_name]) 
        print("piece width:",piece_width)
        temp_array = []
        for start_x in range(PIECES_startpos_indexing_value[current_piece][rotation_name],11-PIECES_xpos_indexing_value[current_piece][rotation_name]):
        #for start_x in range(7,8):
        #for start_x in range(abs(get_piece_leftmost_index_from_origin(PIECES_index[current_piece][rotation_name])), max_start_x):
        # TODO can do sth like this ^   
            
            lowest_y = find_lowest_y_for_piece(PIECES_index[current_piece][rotation_name], board, start_x)
            #print("lowest y for piece at x:",start_x," is ",lowest_y)
            for y in range(lowest_y, 20):
                print(lowest_y,"y:",y)
                if can_place(PIECES_index[current_piece][rotation_name], board, y, start_x):
                    print("can place at x: ", start_x, " y: ", y)
                    arr_piece_info_array.append([current_piece, rotation_name, start_x, y])
                    temp_array.append([current_piece, rotation_name, start_x, y])
            print(f"range: {PIECES_startpos_indexing_value[current_piece][rotation_name]} to {11-PIECES_xpos_indexing_value[current_piece][rotation_name]} for piece {current_piece} rotation {rotation_name}")
            time.sleep(0.1) 
        print(f"added {len(temp_array)} positions for rotation {rotation_name}")    
        time.sleep(2)  
    print("total positions to try:",len(arr_piece_info_array))


    time.sleep(2137)
    for position_info in arr_piece_info_array:
        new_board = simulate_kicks(board, arr_piece_info_array)
        if new_board is None:
            if config.PRINT_MODE:
                print(f"GAMEOVER, score (best loss) : {best_loss} ")
            GAMEOVER = True
            break
        board_after_clear, cleared_lines = clear_lines(new_board)

        heights = get_heights(board_after_clear)
        feature["max_height"] = max(heights)
        feature["uneven"] = int(uneven_stack_est(heights))
        feature["holes"] = check_holes2(board_after_clear)
        feature["different_heights"] = sum(
            heights[x] != heights[x + 1] for x in range(len(heights) - 1)
        )
        feature["attack"] = count_lines_clear(cleared_lines, combo, board_after_clear)

        if (current_loss := loss(feature, uneven_loss, holes_punishment,  # type: ignore
                                height_diff_punishment, attack_bonus, max_height_punishment)) < best_loss:# type: ignore
            best_move = f"{current_piece}_x{start_x}_{rotation_name}"
            move_history = [best_move]
            best_loss = current_loss
            best_feature = feature
            total_attack += feature["attack"][0]
            total_lines += cleared_lines
            
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
    return move_history, best_move
