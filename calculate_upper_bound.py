""" 
the idea here is that looking ahead in X moves we can tell if:
-board has a PC chance, which could be calculated with something like this:
-- we take highest point on the board (X) and the amount of pieces on the board (Y)
-- and use formula: (X*10 (board width) - Y)/4 > depth = PC impossible (if formula is false, that does not imply that pc is possible)
---TODO idea: if the upper condition is not met, we can run a PC solver and try to find the solution on given board and pieces, then just go for the pc 
--- HOWEVER key detail is that pc may become unreachable after we commit for it (enemy can send garbage that we have to tank) so i guess we have to rerun the search for it
- if the bot does not have a PC chance but its in a spot that could have a Tspin chance, we make the bots upper bound lower yet still high enough so it prioritizes tspin over just stacking
- the same applies with tetris well and their reachability

- if nothing above applies, as in we cant rely on tspins and wells for tetrises, we just have to stack, so upper bound stays rather low
"""

from config import BOARD_WIDTH
from config import _OPTIMISTIC_FUTURE_STEP
from board_operations.stack_checking import find_highest_y, count_minos
import math 
class CalculateUpperBound():
    def __init__(self, board, queue, held_piece, depth): # idk if held piece should be there but im leaving it for now
        self.board = board
        self.queue = queue
        self.held_piece = held_piece
        self.depth = depth
        self.upper_bound = _OPTIMISTIC_FUTURE_STEP # bound we will 
        #self.calculate_upper_bound()
        
    def is_pc_possible(self):
        higest_y_with_parity = find_highest_y(self.board) # highestY returns height from 0 index on Y axis so board height of 4 yields 16, to fix it just do 20-result
        higest_y_with_parity = 20 - higest_y_with_parity
        if higest_y_with_parity % 2 == 1: # board does not have even height 
            higest_y_with_parity += 1 # we add one to make it even, this is because pc requires even height to be possible
        
        if (higest_y_with_parity*BOARD_WIDTH - count_minos(self.board))/4 <= self.depth: 
            return True
        return False

    #return self.upper_bound
    
    