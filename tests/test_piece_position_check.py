# this test checks if the positions of the pieces are correctly calculated, as there are a lot of problems with that apparently
# it compares every possible piece and its rotation to what is being yield from the function, and if there is a mismatch, that means there is a problem with the piece position checking, and the test will fail
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
 # python.exe -m pytest -q
from BnB import all_valid_positions
pieces = ["I", "T", "S", "Z", "J", "L"]
board = [[" " for _ in range(10)] for _ in range(20)]
from board_operations.checking_valid_placements import can_place, find_lowest_y_for_piece 
    
expected_positions_L = [
    
    ('L', 'flat_0', 1, 19),
    ('L', 'flat_0', 2, 19),
    ('L', 'flat_0', 3, 19),
    ('L', 'flat_0', 4, 19),
    ('L', 'flat_0', 5, 19),
    ('L', 'flat_0', 6, 19),
    ('L', 'flat_0', 7, 19),
    ('L', 'flat_0', 8, 19),
    
    ('L', 'flat_2', 1, 18),
    ('L', 'flat_2', 2, 18),
    ('L', 'flat_2', 3, 18),
    ('L', 'flat_2', 4, 18),
    ('L', 'flat_2', 5, 18),
    ('L', 'flat_2', 6, 18),
    ('L', 'flat_2', 7, 18),
    ('L', 'flat_2', 8, 18),
    
    ('L', 'spin_R', 0, 18),
    ('L', 'spin_R', 1, 18),
    ('L', 'spin_R', 2, 18),
    ('L', 'spin_R', 3, 18),
    ('L', 'spin_R', 4, 18),
    ('L', 'spin_R', 5, 18),
    ('L', 'spin_R', 6, 18),
    ('L', 'spin_R', 7, 18),
    ('L', 'spin_R', 8, 18),
    
    ('L', 'spin_L', 1, 18),
    ('L', 'spin_L', 2, 18),
    ('L', 'spin_L', 3, 18),
    ('L', 'spin_L', 4, 18),
    ('L', 'spin_L', 5, 18),
    ('L', 'spin_L', 6, 18),
    ('L', 'spin_L', 7, 18),
    ('L', 'spin_L', 8, 18),
    ('L', 'spin_L', 9, 18),
]

expected_positions_I = [
    
    ('I', 'flat_0', 1, 19),
    ('I', 'flat_0', 2, 19),
    ('I', 'flat_0', 3, 19),
    ('I', 'flat_0', 4, 19),
    ('I', 'flat_0', 5, 19),
    ('I', 'flat_0', 6, 19),
    ('I', 'flat_0', 7, 19),
    
    ('I', 'spin_L', 0, 17),
    ('I', 'spin_L', 1, 17),
    ('I', 'spin_L', 2, 17),
    ('I', 'spin_L', 3, 17),
    ('I', 'spin_L', 4, 17),
    ('I', 'spin_L', 5, 17),
    ('I', 'spin_L', 6, 17),
    ('I', 'spin_L', 7, 17),
    ('I', 'spin_L', 8, 17),
    ('I', 'spin_L', 9, 17),
    
    ('I', 'flat_2', 1, 18),
    ('I', 'flat_2', 2, 18),
    ('I', 'flat_2', 3, 18),
    ('I', 'flat_2', 4, 18),
    ('I', 'flat_2', 5, 18),
    ('I', 'flat_2', 6, 18),
    ('I', 'flat_2', 7, 18),
    
    ('I', 'spin_R', -1, 17),
    ('I', 'spin_R', 0, 17),
    ('I', 'spin_R', 1, 17),
    ('I', 'spin_R', 2, 17),
    ('I', 'spin_R', 3, 17),
    ('I', 'spin_R', 4, 17),
    ('I', 'spin_R', 5, 17),
    ('I', 'spin_R', 6, 17),
    ('I', 'spin_R', 7, 17),
    ('I', 'spin_R', 8, 17),
]

expected_position_J = [ 
                       
('J', 'flat_0', 1, 19),
('J', 'flat_0', 2, 19),
('J', 'flat_0', 3, 19),
('J', 'flat_0', 4, 19),
('J', 'flat_0', 5, 19),
('J', 'flat_0', 6, 19),
('J', 'flat_0', 7, 19),
('J', 'flat_0', 8, 19),

('J', 'flat_2', 1, 18),
('J', 'flat_2', 2, 18),
('J', 'flat_2', 3, 18),
('J', 'flat_2', 4, 18),
('J', 'flat_2', 5, 18),
('J', 'flat_2', 6, 18),
('J', 'flat_2', 7, 18),
('J', 'flat_2', 8, 18),

('J', 'spin_R', 0, 18),
('J', 'spin_R', 1, 18),
('J', 'spin_R', 2, 18),
('J', 'spin_R', 3, 18),
('J', 'spin_R', 4, 18),
('J', 'spin_R', 5, 18),
('J', 'spin_R', 6, 18),
('J', 'spin_R', 7, 18),
('J', 'spin_R', 8, 18),

('J', 'spin_L', 1, 18),
('J', 'spin_L', 2, 18),
('J', 'spin_L', 3, 18),
('J', 'spin_L', 4, 18),
('J', 'spin_L', 5, 18),
('J', 'spin_L', 6, 18),
('J', 'spin_L', 7, 18),
('J', 'spin_L', 8, 18),
('J', 'spin_L', 9, 18),
]

expected_position_O_optimal = [ # flat only as o doesnt have any rotations
    ('O', 'flat_0', 1, 19),
    ('O', 'flat_0', 2, 19),
    ('O', 'flat_0', 3, 19),
    ('O', 'flat_0', 4, 19),
    ('O', 'flat_0', 5, 19),
    ('O', 'flat_0', 6, 19),
    ('O', 'flat_0', 7, 19),
    ('O', 'flat_0', 8, 19),
    ('O', 'flat_0', 9, 19)
]

expected_position_Z = [
    ('Z', 'flat_0', 1, 19),
('Z', 'flat_0', 2, 19),
('Z', 'flat_0', 3, 19),
('Z', 'flat_0', 4, 19),
('Z', 'flat_0', 5, 19),
('Z', 'flat_0', 6, 19),
('Z', 'flat_0', 7, 19),
('Z', 'flat_0', 8, 19),

('Z', 'flat_2', 1, 18),
('Z', 'flat_2', 2, 18),
('Z', 'flat_2', 3, 18),
('Z', 'flat_2', 4, 18),
('Z', 'flat_2', 5, 18),
('Z', 'flat_2', 6, 18),
('Z', 'flat_2', 7, 18),
('Z', 'flat_2', 8, 18),

('Z', 'spin_L', 1, 18),
('Z', 'spin_L', 2, 18),
('Z', 'spin_L', 3, 18),
('Z', 'spin_L', 4, 18),
('Z', 'spin_L', 5, 18),
('Z', 'spin_L', 6, 18),
('Z', 'spin_L', 7, 18),
('Z', 'spin_L', 8, 18),
('Z', 'spin_L', 9, 18),

('Z', 'spin_R', 0, 18),
('Z', 'spin_R', 1, 18),
('Z', 'spin_R', 2, 18),
('Z', 'spin_R', 3, 18),
('Z', 'spin_R', 4, 18),
('Z', 'spin_R', 5, 18),
('Z', 'spin_R', 6, 18),
('Z', 'spin_R', 7, 18),
('Z', 'spin_R', 8, 18),
]

expected_position_T = [
    ('T', 'flat_0', 1, 19),
    ('T', 'flat_0', 2, 19),
    ('T', 'flat_0', 3, 19),
    ('T', 'flat_0', 4, 19),
    ('T', 'flat_0', 5, 19),
    ('T', 'flat_0', 6, 19),
    ('T', 'flat_0', 7, 19),
    ('T', 'flat_0', 8, 19),
    
    ('T', 'flat_2', 1, 18),
    ('T', 'flat_2', 2, 18),
    ('T', 'flat_2', 3, 18),
    ('T', 'flat_2', 4, 18),
    ('T', 'flat_2', 5, 18),
    ('T', 'flat_2', 6, 18),
    ('T', 'flat_2', 7, 18),
    ('T', 'flat_2', 8, 18),
    
    ('T', 'spin_R', 0, 18),
    ('T', 'spin_R', 1, 18),
    ('T', 'spin_R', 2, 18),
    ('T', 'spin_R', 3, 18),
    ('T', 'spin_R', 4, 18),
    ('T', 'spin_R', 5, 18),
    ('T', 'spin_R', 6, 18),
    ('T', 'spin_R', 7, 18),
    ('T', 'spin_R', 8, 18),
    
    ('T', 'spin_L', 1, 18),
    ('T', 'spin_L', 2, 18),
    ('T', 'spin_L', 3, 18),
    ('T', 'spin_L', 4, 18),
    ('T', 'spin_L', 5, 18),
    ('T', 'spin_L', 6, 18),
    ('T', 'spin_L', 7, 18),
    ('T', 'spin_L', 8, 18),
    ('T', 'spin_L', 9, 18),
]

expected_position_S = [
    ('S', 'flat_0', 1, 19),
    ('S', 'flat_0', 2, 19),
    ('S', 'flat_0', 3, 19),
    ('S', 'flat_0', 4, 19),
    ('S', 'flat_0', 5, 19),
    ('S', 'flat_0', 6, 19),
    ('S', 'flat_0', 7, 19),
    ('S', 'flat_0', 8, 19),
    
    ('S', 'flat_2', 1, 18),
    ('S', 'flat_2', 2, 18),
    ('S', 'flat_2', 3, 18),
    ('S', 'flat_2', 4, 18),
    ('S', 'flat_2', 5, 18),
    ('S', 'flat_2', 6, 18),
    ('S', 'flat_2', 7, 18),
    ('S', 'flat_2', 8, 18),
    
    ('S', 'spin_L', 1, 18),
    ('S', 'spin_L', 2, 18),
    ('S', 'spin_L', 3, 18),
    ('S', 'spin_L', 4, 18),
    ('S', 'spin_L', 5, 18),
    ('S', 'spin_L', 6, 18),
    ('S', 'spin_L', 7, 18),
    ('S', 'spin_L', 8, 18),
    ('S', 'spin_L', 9, 18),
    
    ('S', 'spin_R', 0, 18),
    ('S', 'spin_R', 1, 18),
    ('S', 'spin_R', 2, 18),
    ('S', 'spin_R', 3, 18),
    ('S', 'spin_R', 4, 18),
    ('S', 'spin_R', 5, 18),
    ('S', 'spin_R', 6, 18),
    ('S', 'spin_R', 7, 18),
    ('S', 'spin_R', 8, 18),
]

EXPECTED_BY_PIECE = {
    'I': expected_positions_I,
    'T': expected_position_T,
    'S': expected_position_S,
    'Z': expected_position_Z,
    'J': expected_position_J,
    'L': expected_positions_L,
    'O_optimal': expected_position_O_optimal
}

@pytest.mark.parametrize("piece", ["I", "T", "S", "Z", "J", "L"])
def test_all_valid_positions_match_expected(piece):
    board = [[" " for _ in range(10)] for _ in range(20)]
    actual = set(all_valid_positions(piece, board, held_piece=None, queue=[piece]))
    expected = set(EXPECTED_BY_PIECE[piece])

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    assert not missing and not extra, (
        f"{piece} mismatch | missing={len(missing)} extra={len(extra)} "
        f"| missing_sample={missing[:10]} extra_sample={extra[:10]}"
    )
def test_O_optimal_positions():
    board = [[" " for _ in range(10)] for _ in range(20)]
    actual = set(all_valid_positions('O', board, held_piece=None, queue=['O']))
    expected = set(EXPECTED_BY_PIECE['O_optimal'])

    missing = sorted(expected - actual)
    extra = sorted(actual - expected)

    assert not missing and not extra, (
        f"O optimal mismatch | missing={len(missing)} extra={len(extra)} "
        f"| missing_sample={missing[:10]} extra_sample={extra[:10]}"
    )