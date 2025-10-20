import copy
from logging import config
from pprint import pp
from board_operations.board_operations import clear_lines
from board_operations.checking_valid_placements import soft_drop_simulation
from board_operations.stack_checking import (
    check_holes2,
    get_heights,
    uneven_stack_est,
)
from tetrio_parsing.calculate_attack import count_lines_clear
from utility.pieces import PIECES, PIECES_soft_drop

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
    from board_operations.checking_valid_placements import find_lowest_y_for_piece, soft_drop_simulation
            
    best_feature = feature.copy()
    best_loss = 10000

    piece_info_array = []

    current_piece = queue[0]
    assert current_piece in PIECES_soft_drop
    # 
    for rotation_name, piece_shape in PIECES_soft_drop[current_piece].items():
        max_x = 10 - len(piece_shape[0])
        for x in range(max_x + 1):
            #new_board = soft_drop_simulation(piece_shape, copy.deepcopy(board), x)
            lowest_y = find_lowest_y_for_piece(piece_shape, board, x)
            piece_info_array.append([rotation_name, lowest_y]) # should be filled only with flat_0 at first
            
        new_board = simulate_kicks(board, piece_shape, rotation_name, x, lowest_y,piece_info_array)
        # ordering:
        # simulate soft drop
        # check if you can move left right
        # if no, then you know what range of positions youwill be working on, could be 1 or entire board (10 -piece lenghth)
        # rotate and apply kick table?
        # go through eachj rotation and if kick table doesnt apply 3 times in row just skip rotating anymore

        # almost every single kick (unsure which not but idk) can be reversed with pressing opposite direction
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
            best_move = f"{current_piece}_x{x}_{rotation_name}"
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
