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
from board_operations.stack_checking import find_highest_y, count_minos, is_tetris_well
import math 
# small problem i have with this function that i dont know how to fix yet is that it kinda works when bot puts itself in positions that could leave to good outcomes
# for example, if it would skim all the time, it would not look for pcs or tetrises (tho tspins could save something here) so we kinda pray that it puts itself in one of those situations to go for better moves

class CalculateUpperBound():
    def __init__(self, board, queue, held_piece, depth): # idk if held piece should be there but im leaving it for now
        self.board = board
        self.queue = queue
        self.held_piece = held_piece
        self.depth = depth
        self.upper_bound = _OPTIMISTIC_FUTURE_STEP # bound we will 
        #self.calculate_upper_bound()
        
    def is_pc_possible(self): # done, works with testcases
        # TODO if the board is empty, we have to check the depth and if the round just started or no
        # if the round just started we can try getting pc if depth is 10(with hold piece it would be 11 but we should be able to find pc with 10 too), if its midgame, we can look for a 2L pc (so check for combos like 2x) piece,L,I,J) so we only need depth 6 (5 can do too but using hold gives more chances for 2 line)
        higest_y_with_parity = find_highest_y(self.board) # highestY returns height from 0 index on Y axis so board height of 4 yields 16, to fix it just do 20-result
        higest_y_with_parity = 20 - higest_y_with_parity
        if higest_y_with_parity % 2 == 1: # board does not have even height 
            higest_y_with_parity += 1 # we add one to make it even, this is because pc requires even height to be possible
        if (higest_y_with_parity*BOARD_WIDTH - count_minos(self.board)) % 4 != 0:
            return False
        if (higest_y_with_parity*BOARD_WIDTH - count_minos(self.board))/4 <= self.depth: 
            return True
            # TODO run the PC solver to see if the PC is doable, if not, try checking for tspins instead
            # IF Pc is doable, we set _optimistic_future_step to a higher value, maybe 100 so it takes the PC over anything else
            # taht would work only if heuristic itself wants to do PC BTW !!!!!
        return False

    def is_tspin_possible(self):
        # TODO implement tspin check, maybe just check if there is a tspin setup on the board and if the next piece is T
        """
        now that one is tricky because what even is a tspin, we need unevenbboard check, heighdifference and possibility to judge how possible
        it would be to fill up the height diff with other blocks for tspins (donations) and things like t spin minis, and hamburger setups
        
        should have a check "is tspin in queue i guess but that isnt needed"
        """
        return False
    def is_tetris_well_possible(self, board):
        # TODO implement tetris well check, maybe just check if there is a tetris well on the board and if the next piece is I
        """ 
        here the idea would be to simply check if we can do a quad or a combo to quad with current pieces
        """
        """it should be splited in 2 cases:
        case 1: we have a well (it can be covered ) so we calculate if we can take tetris or downstack into tetris (mostly the second part)
        case 2: we try making well on our own, so we have to check the biggest disparity we have on the board that isnt covered,
        so for example we have spiky board that has holes like, depth 2, depth 4, and depth 5, we will focus on depth 5 hole and try filling up everything else, unless we dont have enough depth to fill up the blocks
        """
        
        # case 1 # example of  return: True(was succesful?), col, well_top(index in which highest I piece mino would be while tkaing quad), minos_above
        
        tetris_wall_esists, col ,index_of_top_well , spaces_above_the_well= is_tetris_well(board)
        
        """ 
        case 1 has a big issue that it only gives us where the well is, if there is one, 
        but we need to tell if the well is even accesible in x amount of pieces, that could be done in same wayas checking PC, 
        additionaly we can add some more points if the well is accesible in a combo, like make move 1 and see if the combo increases,
        if no, move is over, then do it with entire queue, assuming that the weill is still accesible in that amount of peisces
        
        # i take back things that are below but i keep it for clarity, if heuristic is good, it will take quads over normal clears, and it should be able to find a quad, doing another check here is useless
        another important thing is that quad can be accesible with a spin, when the well is technically covered, easy check woudl be to just run the check we do for bruteforce,
        if we can make the I piece go into that spot, taking a quad, so simulate game movement etc etc
        """
        
        
        return False
    # if all the functions above fail, we leave the uppoer bound as we cant do much
    #return self.upper_bound
    
    