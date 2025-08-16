# -*- coding: utf-8 -*-
# if someone is reading that, i may or may not have used some AI help for comments and such to make code more readable
# half of them i didnt even read but i dont remove them because fucking higlighting puts them there as it feels and it was usefull
# once!! so i wil lleave them, so like whateverr sorry algosith dont bother with them
# got an issue with that? better not or i will cry.

# to test the argparse better, try running it in console using:
# python .\main.py --rule, rules will be listed lower, as they are wip
from tetrio_parsing.calculate_attack import count_lines_clear 
from GenerateBag import create_bag
import copy
import time
import argparse # testing it
import threading

from tests.combo_attack_test import custom_board # probably stupid way to do that, idk better yet

from utility.print_board import print_board
from utility.pieces import PIECES

from board_operations.checking_valid_placements import drop_piece
from board_operations.board_operations import clear_lines

from GenerateBag import add_piece_from_bag 

#from BoardRealTimeView import TetrisBoardViewer
from bruteforcing import find_best_placement

if not PIECES:
    raise ImportError("PIECES dictionary could not be imported or is empty.")

DESIRED_QUEUE_PREVIEW_LENGTH = 5

class GameStats:
    def __init__(self):
        self.burst = [] #(PPS) stores 10 times piece was placed, then max-min
        self.pps = 0.0
        self.single = 0
        self.double = 0
        self.triple = 0
        self.tetris = 0
        self.combo = 0
        self.burst_attack = 0 # unused, stil; thinking about it


class TetrisGame:
    def __init__(self):
        self.board = [[' ' for _ in range(10)] for _ in range(20)]
        self.queue = []  
        self.bag = []   
        self.combo = 0  
        self.start_signal = [False]
        self.game_over_signal = [False]
        self.no_s_z_first_piece_signal = [False] 
        self.custom_bag = [False]
        self.stats = GameStats()
        self.slow_mode = [False]
        self.custom_board = [False]  

    def game_loop(self,viewer):
        
        print("game loop thread started, waiting for start signal")
        while not self.start_signal[0]: 
            time.sleep(0.1)
            if self.game_over_signal[0]: 
                print("game loop terminated before start")
                return 
            
        pieces_placed = 0
        actual_game_start_time = time.perf_counter()

        try:
            if not self.queue:
                print("queue fill")
                num_to_add = DESIRED_QUEUE_PREVIEW_LENGTH - len(self.queue)
                if num_to_add > 0:
                    self.queue, self.bag = add_piece_from_bag(
                        self.queue, 
                        self.bag, 
                        num_pieces=num_to_add, 
                        no_s_z_first_piece=self.no_s_z_first_piece_signal[0]
                    )
                if len(self.queue) < DESIRED_QUEUE_PREVIEW_LENGTH:
                    print("failed to fill queue")
                    return 

            while True:
                if self.game_over_signal[0]: 
                    print("game loop finished by game_over_signal")
                    break
                
                print("\n=== Current Queue ===")
                print(self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH]) 
                
                best_board_after_search, best_move_str = find_best_placement(self.board, self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH],self.combo)
                
                if not best_board_after_search: 
                    print("no valid placement")
                    break
                
                piece_type_placed = self.queue[0] 

                piece_type, x_str, rotation = best_move_str.split('_') 
                x = int(x_str[1:]) 
                
                piece_shape = PIECES[piece_type_placed][rotation] 
                
                board_after_drop = drop_piece(piece_shape, copy.deepcopy(self.board), x)
                if board_after_drop is None:
                    print(f"error: drop_piece failed for valid move: {best_move_str} with piece {piece_type_placed}")
                    print("cannot drop piece")
                    break
            
                board_after_clear, lines_cleared_count = clear_lines(board_after_drop)
                print(f"lines cleared: {lines_cleared_count}")
                attack, self.combo = count_lines_clear(lines_cleared_count,self.combo,board_after_clear)
                self.stats.combo = self.combo

                if lines_cleared_count == 1:
                    self.stats.single += 1
                elif lines_cleared_count == 2:
                    self.stats.double += 1
                elif lines_cleared_count == 3:
                    self.stats.triple += 1
                elif lines_cleared_count == 4:
                    self.stats.tetris += 1

                self.board[:] = board_after_clear
                if viewer: viewer.update_board(self.board)
                
                print(f"\nplaced: {piece_type_placed} by move {best_move_str}")
                print_board(self.board)
                
                if self.queue: 
                    self.queue.pop(0) # remove the used piece
                else: # should never happen
                    print("error: tried to pop from empty queue after placement")
                    break

                # add one new piece to the queue
                self.queue, self.bag = add_piece_from_bag(
                    self.queue, 
                    self.bag, 
                    num_pieces=1, 
                    no_s_z_first_piece=self.no_s_z_first_piece_signal[0]
                )

                pieces_placed += 1
                elapsed = time.perf_counter() - actual_game_start_time
                if len(self.stats.burst) < 10:
                    self.stats.burst.append(elapsed)
                else:
                    self.stats.burst.pop(0)
                    self.stats.burst.append(elapsed)
                print(self.stats.burst)
                if elapsed > 0:
                    self.stats.pps = pieces_placed / elapsed
                    self.stats.burst_pps = (len(self.stats.burst) - 1) / (max(self.stats.burst) - min(self.stats.burst)) if len(self.stats.burst) > 9 else 0
                    print(f"PPS: {self.stats.pps:.2f} burst: {self.stats.burst_pps/10}")
        
        finally:
            print("game loop finished")
            self.game_over_signal[0] = True

def parse_args():
    parser = argparse.ArgumentParser(description="Test arguments/rules")
    parser.add_argument(
        "--rule",
        choices=["40l","custom_bag","nosz","none", "custom_board", "slow"], 
        nargs = "+",
        default=[],
        help = "unsure what it does i guess its like, when you just ask for help, well there is none, youre left alone in the dark world"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    game = TetrisGame()
    
    game.start_signal[0] = True
    
    game.no_s_z_first_piece_signal[0] = "nosz" in args.rule 
    
    game.custom_bag[0] = "custom_bag" in args.rule
    if game.custom_bag[0]:
        game.bag = create_bag(custom_bag=True)
        print(f"custom bag mode enabled, using custom bag \n bag={game.bag}")
        time.sleep(3)
    game.custom_board[0] = "custom_board" in args.rule
    if game.custom_board[0]:
        game.board = custom_board
        print_board(game.board)
        time.sleep(5)
    game.slow_mode[0] = "slow" in args.rule
    game.game_loop(None)

# IMPORTANT:
# - the game loop will stop if no valid placement is found
# - stats.pps can be used in other modules (for display in the viewer).
#
# TODO:
# - add more advanced scoring/evaluation for moves.
# - implement perfect clear solver/mode.
# - add reset/restart logic for early Z/S pieces or other "unlucky" starts.
# - improve stack flatness/height evaluation for better bot performance.
# - improve the code working in a way that its usable on console, i look at it like this
# just make it work normally but do sth like, if there is a line clear,make it pink in console (assuming everything else is colored)
# and then next move just removes that line