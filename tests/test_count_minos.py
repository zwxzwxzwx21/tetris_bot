import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from board_operations.stack_checking import count_minos
testcase =[ 
        [" "," "," "," "," "," "," "," "," "," ",],
        [" "," "," "," "," "," "," "," "," "," ",],
        ["O","O","O","O","O","O"," ","O","O","O",], # 9 
        ["O","O","O","O","O","O"," ","O","O","O",], # 18
        ["O","O","O","O","O","O"," ","O","O","O",], # 27
        ["O","O","O"," "," ","O"," ","O","O","O",], # 34
        ["O","O","O"," "," ","O","O","O","O","O",], # 42
        ["O","O","O"," "," ","O","O","O","O","O",], # 50
        ["O","O","O"," "," ","O","O"," ","O","O",], # 57
        ["O","O","O"," "," ","O","O"," ","O","O",], # 64
        ["O","O","O","O","O","O","O"," ","O","O",], # 73
        ["O","O","O","O","O","O","O"," ","O","O",], # 82
        ["O","O","O"," ","O","O","O"," ","O","O",], # 90
        ["O","O","O"," ","O","O","O","O","O","O",],
        ["O","O","O"," ","O","O","O","O","O","O",],
        ["O","O","O"," ","O","O","O","O","O","O",],
        ["O","O","O"," ","O","O","O","O","O","O",],
        ["O","O","O","O","O","O","O","O","O","O",],
        ["O","O","O","O","O","O","O","O","O","O",],
        ["O","O","O","O","O","O","O","O","O","O",] ]

def test_count_minos():
    assert count_minos(testcase, 2, 13) == 90
    
# to run in terminal: pytest tests/test_count_minos.py