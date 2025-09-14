import copy
from pprint import pp
#from BoardRealTimeView import 
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
import random

uneven_loss = random.uniform(0, 30)
holes_punishment = random.uniform(0, 100)
height_diff_punishment = random.uniform(0, 50)
attack_bonus = random.uniform(0, 50)
print(
    f"uneven_loss: {uneven_loss}, holes_punishment: {holes_punishment}, height_diff_punishment: {height_diff_punishment}, attack_bonus: {attack_bonus}"
)
def loss(feature: dict, uneven_loss, holes_punishment, height_diff_punishment, attack_bonus) -> float:
    return (
        uneven_loss * feature["uneven"]
        + holes_punishment * feature["holes"]
        + max(feature["max_height"] - 4, 0)
        + height_diff_punishment * feature["different_heights"]
        # - attack_bonus * feature["attack"][0]
    )


def find_best_placement(board, queue, combo,stats):
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

            if (current_loss := loss(feature, uneven_loss, holes_punishment, height_diff_punishment, attack_bonus)) < best_loss:
                best_move = f"{current_piece}_x{x}_{rotation_name}"
                move_history = [best_move]
                best_loss = current_loss
                best_feature = feature
                total_attack += feature["attack"][0]
                total_lines += cleared_lines
                
    pp(best_feature)
    print()
    if GAMEOVER:
        print(
            f"DATA: \n uneven_loss: {uneven_loss},\n holes_punishment: {holes_punishment},\n height_diff_punishment: {height_diff_punishment},\n attack_bonus: {attack_bonus}\n cleared lines: {(stats.single + stats.double + stats.triple + stats.tetris)}\n total attack: {stats.total_attack}\n"
)       
        from coefficients_calculation import save_game_stats
        save_game_stats(
            uneven_loss=uneven_loss,
            holes_punishment=holes_punishment, 
            height_diff_punishment=height_diff_punishment,
            attack_bonus=attack_bonus,
            lines_cleared=(stats.single + stats.double + stats.triple + stats.tetris),
            total_attack=stats.total_attack,
            seed=stats.seed  # Dodaj parametr seed do funkcji
        )
        return None
    assert move_history
    return move_history, best_move
