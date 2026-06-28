import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
def test_BnB_finding_better_solution_than_bruteforce():

    """depth 1 takes the Tspin double because it gives the most attack
    depth > 1 takes the Tspin single because it results in PC later"""

    queue = ["T","L"]
    board =[
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O"," "," "," ","O","O",],
        ["O","O","O","O","O","O"," ","O","O","O",] ] 


    from bruteforcing import find_best_placement


    a = find_best_placement(board, queue, combo=None,stats= None,held_piece=None)
    assert a is not None, "find_best_placement returned None, expected a valid move"
    assert a[0] == ["T_x6_flat_2"], f"Expected best move to be 'T_x6_flat_2', but got {a[0]}"

    from BnB import branch_and_bound_search
    result_bnb = branch_and_bound_search(board, queue, 2, held_piece=None)
    assert result_bnb is not None, "branch_and_bound_search returned None, expected a valid move"
    assert result_bnb['sequence'] == [('T', 'spin_L', 6, 18, False), ('L', 'spin_L', 7, 18, False)]
    