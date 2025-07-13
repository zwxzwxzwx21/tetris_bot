# -*- coding: utf-8 -*-
# if someone is reading that, i may or may not have used some AI help for comments and such to make code more readable
# got an issue with that? better not or i will cry.

from tetrio_parsing.calculate_attack import count_lines_clear 
import copy
import time
import threading

from utility.print_board import print_board
from utility.pieces import PIECES

from board_operations.checking_valid_placements import drop_piece
from board_operations.board_operations import clear_lines

from GenerateBag import add_piece_from_bag 

from BoardRealTimeView import TetrisBoardViewer
from bruteforcing import find_best_placement

if not PIECES:
    raise ImportError("PIECES dictionary could not be imported or is empty.")

DESIRED_QUEUE_PREVIEW_LENGTH = 5

class GameStats:
    def __init__(self):
        self.burst = [] # stores 10 times piece was placed, then max-min
        self.pps = 0.0
        self.single = 0
        self.double = 0
        self.triple = 0
        self.tetris = 0
        self.combo = 0
stats = GameStats()

class TetrisGame:
    def __init__(self):
        self.board = [[' ' for _ in range(10)] for _ in range(20)]
        self.queue = []  
        self.bag = []   
        self.combo = 0  
        self.start_signal = [False]
        self.game_over_signal = [False]
        self.no_s_z_first_piece_signal = [False] 
        self.stats = GameStats()
    def start_game(self):
        print("Starting Tetris game...")
        self.viewer = TetrisBoardViewer(self.board, self.stats, self.start_signal, self.queue, self.game_over_signal, self.no_s_z_first_piece_signal)

    def game_loop(self,viewer):
        
        print("Game loop thread started, waiting for start signal...")
        while not self.start_signal[0]: 
            time.sleep(0.1)
            if self.game_over_signal[0]: 
                print("Game loop terminated before start by external signal.")
                return 
            
        pieces_placed = 0
        actual_game_start_time = time.perf_counter()

        try:
            if not self.queue:
                print("Initial queue fill...")
                num_to_add = DESIRED_QUEUE_PREVIEW_LENGTH - len(self.queue)
                if num_to_add > 0:
                    self.queue, self.bag = add_piece_from_bag(
                        self.queue, 
                        self.bag, 
                        num_pieces=num_to_add, 
                        no_s_z_first_piece=self.no_s_z_first_piece_signal[0]
                    )
                if len(self.queue) < DESIRED_QUEUE_PREVIEW_LENGTH:
                    print("Failed to fill initial queue sufficiently. Game Over.")
                    return 

            while True:
                if self.game_over_signal[0]: 
                    print("Game loop terminating due to game_over_signal.")
                    break
                
                print("\n=== Current Queue ===")
                print(self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH]) 
                
                best_board_after_search, best_move_str = find_best_placement(self.board, self.queue[:DESIRED_QUEUE_PREVIEW_LENGTH],self.combo)
                
                if not best_board_after_search: 
                    print("No valid placement found by bruteforcer. Ending game.")
                    break
                
                piece_type_placed = self.queue[0] 

                piece_type, x_str, rotation = best_move_str.split('_') 
                x = int(x_str[1:]) 
                
                piece_shape = PIECES[piece_type_placed][rotation] 
                
                board_after_drop = drop_piece(piece_shape, copy.deepcopy(self.board), x)
                if board_after_drop is None:
                    print(f"Error: drop_piece failed for supposedly valid move: {best_move_str} with piece {piece_type_placed}")
                    print("Game Over - Cannot drop piece.")
                    break
            
                board_after_clear, lines_cleared_count = clear_lines(board_after_drop)
                print(f"Lines cleared: {lines_cleared_count}")
                count_lines_clear(lines_cleared_count,self.combo)
                
                self.board[:] = board_after_clear
                if viewer: viewer.update_board(self.board)
                
                print(f"\nPlaced: {piece_type_placed} via move {best_move_str}")
                print_board(self.board)
                
                if self.queue: 
                    self.queue.pop(0) # Remove the used piece
                else: # should never happen
                    print("error: Tried to pop from empty queue after placement.")
                    break

                # Add one new piece to the queue
                self.queue, self.bag = add_piece_from_bag(
                    self.queue, 
                    self.bag, 
                    num_pieces=1, 
                    no_s_z_first_piece=self.no_s_z_first_piece_signal[0]
                )

                pieces_placed += 1
                elapsed = time.perf_counter() - actual_game_start_time
                if len(stats.burst) < 10:
                    stats.burst.append(elapsed)
                else:
                    stats.burst.pop(0)
                    stats.burst.append(elapsed)
                print(stats.burst)
                if elapsed > 0:
                    stats.pps = pieces_placed / elapsed
                    stats.burst_pps = (len(stats.burst) - 1) / (max(stats.burst) - min(stats.burst)) if len(stats.burst) > 9 else 0
                    print(f"PPS (Pieces Per Second): {stats.pps:.2f} burst: {stats.burst_pps/10}")

        finally:
            print("Game loop finished.")
            self.game_over_signal[0] = True
game = TetrisGame()
viewer = TetrisBoardViewer(game.board, stats, game.start_signal, game.queue, game.game_over_signal, game.no_s_z_first_piece_signal)

# start the game loop in a separate thread so the viewer remains responsive
game_thread = threading.Thread(target=lambda: game.game_loop(viewer), daemon=True)
game_thread.start()

viewer.mainloop(GUI_mode=False)

# --- 
# IMPORTANT: 
# - The game loop will stop if no valid placement is found.
# - stats.pps can be used in other modules (e.g., for display in the viewer).
# - This script is intended for AI/bot simulation, debugging, or visualization.
# - For headless or server-side use, remove or modify the viewer code.
#
# TODO:
# - Add more advanced scoring/evaluation for moves.
# - Implement perfect clear solver/mode.
# - Add reset/restart logic for early Z/S pieces or other "unlucky" starts.
# - Improve stack flatness/height evaluation for better AI performance.

