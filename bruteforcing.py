import copy
from logging import config
from pprint import pp
from board_operations.board_operations import clear_lines
from board_operations.checking_valid_placements import drop_piece
from board_operations.stack_checking import (
    check_holes2,
    get_heights,
    uneven_stack_est,
)
from tetrio_parsing.calculate_attack import count_lines_clear
from utility.pieces import PIECES

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

def is_better_result(lines_cleared):
    filepath = "bruteforcer_stats.xlsx"
    if not os.path.exists(filepath):
        return True  
        
    try:
        existing_df = pd.read_excel(filepath)
        if existing_df.empty:
            return True
            
        best_lines = existing_df['lines_cleared'].max()
        return lines_cleared > best_lines
    except Exception as e:
        if config.PRINT_MODE:
            print(f"error checking previous results: {e}")
        return True  

def find_best_placement(board, queue, combo, stats):
    move_history = []
    GAMEOVER = False
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
    best_feature = feature.copy()
    best_loss = 10000

    current_piece = queue[0]
    assert current_piece in PIECES

    for rotation_name, piece_shape in PIECES[current_piece].items():
        max_x = 10 - len(piece_shape[0])
        for x in range(max_x + 1):
            new_board = drop_piece(piece_shape, copy.deepcopy(board), x)
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
        
        from coefficients_calculation import save_game_stats
        
        if is_better_result(lines_cleared):
            save_game_stats(
                uneven_loss=uneven_loss,# type: ignore
                holes_punishment=holes_punishment, # type: ignore
                height_diff_punishment=height_diff_punishment,# type: ignore
                attack_bonus=attack_bonus,# type: ignore
                max_height_punishment=max_height_punishment, # type: ignore
                lines_cleared=lines_cleared,
                total_attack=stats.total_attack,
                seed=stats.seed  
            )
            
        return None
    assert move_history
    return move_history, best_move
