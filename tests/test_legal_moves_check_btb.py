import os
import sys

import pytest
from search_for_best_move import search_for_best_move

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


queue = ["O"] # O DOESNT have rotations so its easier to seave through things we dont care about 

board_with_unreachable_position =[
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
    [" "," "," "," "," "," "," "," "," "," ",],
    [" "," "," "," "," ","T","T"," "," "," ",],
    [" "," "," "," ","T"," "," ","T"," "," ",],
    [" "," "," "," "," "," "," "," "," "," ",]
]
queue_tricky_move = ["T"] # T has rotations and can be used to test if the search is able to find the best move in a tricky situation
queue_tricky_move_2 = ["S"] # T has rotations and can be used to test if the search is able to find the best move in a tricky situation
board_with_tricky_move =[
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
    [" "," "," "," "," ","O"," "," ","O"," ",],
    [" "," "," "," "," ","O"," "," ","O"," ",],
    [" "," "," "," ","O"," "," "," ","O"," ",],
    [" "," "," "," ","O"," ","O","O"," "," ",],
    [" "," "," "," ","O"," "," ","O"," "," ",],
    [" "," "," "," ","O"," "," ","O"," "," ",]
]

def test_bnb_finds_best_move_in_tricky_position():
    
    # piece info array example ("T",'flat_0',x(fore xample 4),y(for example 15))
    result = search_for_best_move('T_x5_spin_R', board_with_tricky_move, 18)    
    assert result is not None, "search_for_best_move returned None, expected a valid move"
    result2 = search_for_best_move('S_x5_spin_R', board_with_tricky_move, 18)
    assert result2 is not None, "search_for_best_move returned None, expected a valid move"
    # check if it does not find the impossble move
    result3 = search_for_best_move('O_x5_flat_0', board_with_tricky_move, 19)
    assert result3 is None, "search_for_best_move returned a move, expected None for an impossible move"
    
# how to run tests in git : 
# python -m pytest -q --disable-warnings --tb=short


