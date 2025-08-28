import copy

from board_operations.board_operations import clear_lines
from board_operations.checking_valid_placements import drop_piece
from board_operations.stack_checking import (
    check_holes,
    get_heights,
    height_difference,
    uneven_stack_est,
)
from tetrio_parsing.calculate_attack import count_lines_clear
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


def find_best_placement(board, queue, combo):
    move_history = []
    best_move = None
    best_uneven = best_holes = best_height_diff = 0
    best_loss = 10000
    best_max_height = 20

    current_piece = queue[0]
    assert current_piece in PIECES

    for rotation_name, piece_shape in PIECES[current_piece].items():
        max_x = 10 - len(piece_shape[0])
        for x in range(max_x + 1):
            print(f"considering {current_piece}_x{x}_{rotation_name}")
            new_board = drop_piece(piece_shape, copy.deepcopy(board), x)
            board_after_clear, cleared_lines = clear_lines(new_board)
            attack_for_clear, new_combo = count_lines_clear(
                cleared_lines, combo, board_after_clear
            )
            # --- HEIGHT & UNEVEN CHECK ---
            height_diff, _ = height_difference(board_after_clear)
            heights = get_heights(board_after_clear)
            max_height = max(heights)

            uneven = uneven_stack_est(heights)

            # --- HOLES CHECK ---
            holes = check_holes(board_after_clear)

            if (
                loss := 0 * uneven + 1 * holes + 0.0 * height_diff + max_height
            ) < best_loss:
                best_move = f"{current_piece}_x{x}_{rotation_name}"
                move_history = [best_move]
                (
                    best_loss,
                    best_uneven,
                    best_holes,
                    best_height_diff,
                    best_max_height,
                ) = (loss, uneven, holes, height_diff, max_height)
    print(f"""{best_loss=}
{best_uneven=}
{best_holes=}
{best_height_diff=}
{best_max_height=}""")
    assert move_history
    return move_history, best_move
