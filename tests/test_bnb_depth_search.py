import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from BnB import find_best_placement_bnb


def _empty_board():
    return [[" " for _ in range(10)] for _ in range(20)]

# this one below is a test to check if the function returns a valid move in the correct format, it does not check if the move is the best one, just that it returns a valid move
def test_find_best_placement_bnb_returns_bruteforcing_shape():
    board = _empty_board()
    queue = ["J", "L", "T"]

    placement = find_best_placement_bnb(board, queue, held_piece="S", depth=2)
    assert placement is not None

    move_history, best_move_str, best_move_y, used_hold = placement
    assert move_history == [best_move_str]

    piece, xpos_part, rotation_a, rotation_b = best_move_str.split("_")
    assert piece in {"I", "O", "T", "S", "Z", "J", "L"}
    assert xpos_part.startswith("x")
    assert rotation_a in {"flat", "spin"}
    assert rotation_b in {"0", "2", "L", "R"}
    assert isinstance(best_move_y, int)
    assert isinstance(used_hold, bool)
