import copy
from pprint import pp

from board_operations.board_operations import clear_lines
from board_operations.checking_valid_placements import drop_piece
from board_operations.stack_checking import (
    check_holes2,
    get_heights,
    uneven_stack_est,
)
from utility.pieces import PIECES

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
TIME_LIMIT = 999  # Maximum time (in seconds) allowed for the search
UNEVEN_THRESHOLD = 1.1  # Prune stacks that are too uneven
MAX_HEIGHT_DIFF = 6  # Prune stacks that are too tall


def loss(feature: dict) -> float:
    return (
        0.4 * feature["uneven"]
        + 200 * feature["holes"]
        + max(feature["max_height"] - 4, 0)
        + 0.05 * feature["different_heights"]
    )


def find_best_placement(board, queue, combo):
    move_history = []
    best_move = None
    feature = {
        "uneven": 0,
        "holes": 0,
        "height_diff": 0,
        "max_height": 20,
        "different_heights": 30,
    }
    best_feature = feature.copy()
    best_loss = 10000

    current_piece = queue[0]
    assert current_piece in PIECES

    for rotation_name, piece_shape in PIECES[current_piece].items():
        max_x = 10 - len(piece_shape[0])
        for x in range(max_x + 1):
            print(f"considering {current_piece}_x{x}_{rotation_name}")
            new_board = drop_piece(piece_shape, copy.deepcopy(board), x)
            board_after_clear, cleared_lines = clear_lines(new_board)
            # --- HEIGHT & UNEVEN CHECK ---
            from board_operations.board_operations import convert_board_numpy

            # print(board_after_clear)
            board_after_clear = convert_board_numpy(board_after_clear)
            # print(board_after_clear)
            heights = get_heights(board_after_clear)
            feature["max_height"] = max(heights)

            feature["uneven"] = int(uneven_stack_est(heights))

            # --- HOLES CHECK ---
            feature["holes"] = check_holes2(board_after_clear)

            # --- DIFFERENT HEIGHT CHECK ---
            feature["different_heights"] = sum(
                heights[x] != heights[x + 1] for x in range(len(heights) - 1)
            )

            if (current_loss := loss(feature)) < best_loss:
                best_move = f"{current_piece}_x{x}_{rotation_name}"
                move_history = [best_move]
                best_loss = current_loss
                best_feature = feature

    pp(best_feature)
    print()
    assert move_history
    return move_history, best_move
