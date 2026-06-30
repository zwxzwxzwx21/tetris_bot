import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from calculate_upper_bound import CalculateUpperBound
depth = 5 
queue = ["I", "O", "T", "S", "Z"]
board_PCalbe_at_depth_2 =[
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

board_PCalbe_at_depth_6_parity_example =[
    # should return false at 5 and true at 6 because of parity check
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
        ["O","O","O","O"," "," "," "," "," "," ",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O"," "," "," ","O","O",],
        ["O","O","O","O","O","O"," ","O","O","O",] ] 

board_not_PCable =[
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
        ["O","O","O","O","O"," "," "," "," "," ",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O"," "," "," ","O","O",],
        ["O","O","O","O","O","O"," ","O","O","O",] ] 


board_impossible_to_pc_example1 =[
    
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," ","x"," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        ["O","O","O","O"," "," "," "," "," "," ",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O"," "," "," ","O","O",],
        ["O","O","O","O","O","O"," ","O","O","O",] ] 


board_impossible_to_pc_example2 =[
    
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," ","x","x","x","x",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        ["O","O","O","O"," "," "," "," "," "," ",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O","O"," "," ","O","O",],
        ["O","O","O","O","O"," "," "," ","O","O",],
        ["O","O","O","O","O","O"," ","O","O","O",] ] 
from board_operations.stack_checking import count_minos, find_highest_y

def test_calculate_upper_bound_PCable_at_depth_2():
    from board_operations.stack_checking import count_minos, find_highest_y
    
    upper_bound_calculator = CalculateUpperBound(board_PCalbe_at_depth_2, queue, None, 2)
    
    assert upper_bound_calculator.is_pc_possible() == True, "Expected PC to be possible at depth 2"
def test_calculate_upper_bound_PCable_at_depth_3():
    upper_bound_calculator = CalculateUpperBound(board_PCalbe_at_depth_2, queue, None, 3)
    assert upper_bound_calculator.is_pc_possible() == True, "Expected PC to be possible at depth 3"
def test_calculate_upper_bound_PCable_at_depth_1():
    upper_bound_calculator = CalculateUpperBound(board_PCalbe_at_depth_2, queue, None, 1)
    assert upper_bound_calculator.is_pc_possible() == False, "Expected PC to be impossible at depth 1"
    
def test_calculate_upper_bound_PCable_at_depth_6_parity_example():
    upper_bound_calculator = CalculateUpperBound(board_PCalbe_at_depth_6_parity_example, queue, None, 5)
    assert upper_bound_calculator.is_pc_possible() == False, "Expected PC to be impossible at depth 5 due to parity"
def test_calculate_upper_bound_PCable_at_depth_6_parity_example_true():
    upper_bound_calculator = CalculateUpperBound(board_PCalbe_at_depth_6_parity_example, queue, None, 6)
    assert upper_bound_calculator.is_pc_possible() == True, "Expected PC to be possible at depth 6"
    
def test_calculate_upper_bound_not_PCable():
    upper_bound_calculator = CalculateUpperBound(board_not_PCable, queue, None, 5)
    assert upper_bound_calculator.is_pc_possible() == False, "Expected PC to be impossible at depth 5"
    
    
def test_calculate_upper_bound_not_PCable_depth_6():
    upper_bound_calculator = CalculateUpperBound(board_not_PCable, queue, None, 6)
    
    
    #assert result == True, f"h={h}, c={c}, formula={(h*10 - c)/4}"
    assert upper_bound_calculator.is_pc_possible() == False, "Expected PC to be impossible at depth 6"
    
def test_calculate_upper_bound_impossible_to_pc_example1():# uneven amount of blocks
    upper_bound_calculator = CalculateUpperBound(board_impossible_to_pc_example1, queue, None, 30)
    assert upper_bound_calculator.is_pc_possible() == False, "Expected PC to be impossible"
def test_calculate_upper_bound_impossible_to_pc_example2(): # not enough depth
    upper_bound_calculator = CalculateUpperBound(board_impossible_to_pc_example2, queue, None, 10)
    
    assert upper_bound_calculator.is_pc_possible() == False, "Expected PC to be impossible"
    
# to run tests just from this file use command 
#  ./.venv/Scripts/python -m pytest tests/test_calculate_upper_bound.py
 