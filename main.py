# -*- coding: utf-8 -*-
import pyautogui
import copy
import time
import threading

from utility.print_board import print_board
from utility.pieces import PIECES  # importing piece lookup table

from board_operations.stack_checking import compare_to_avg, check_heights, check_holes, check_i_dep, uneven_stack_est, height_difference, get_heights
from board_operations.checking_valid_placements import drop_piece, place_piece, can_place
from board_operations.board_operations import clear_lines, apply_gravity

from tetrio_parsing.screen_reading import get_next_piece, read_queue
from tetrio_parsing.movement import move_piece

from GenerateBag import create_bag, add_piece_from_bag

from BoardRealTimeView import TetrisBoardViewer

# Ensure PIECES is properly imported or defined
if not PIECES:
    raise ImportError("PIECES dictionary could not be imported or is empty.")

from bruteforcing import find_best_placement

# Initialize empty board and piece queue/bag
queue = create_bag()
bag = create_bag()
board = [[' ' for _ in range(10)] for _ in range(20)]

# Create the Tetris board viewer window (Pygame)
viewer = TetrisBoardViewer(board)

# Shared stats object for PPS (Pieces Per Second)
class GameStats:
    """
    Holds statistics for the current game session.
    Currently only tracks PPS (pieces per second).
    """
    def __init__(self):
        self.pps = 0.0

stats = GameStats()

def game_loop():
    """
    Main game loop for the Tetris AI/bot.
    Continuously finds and places the best move, updates the board and viewer,
    and tracks performance statistics (PPS).
    """
    pieces_placed = 0
    start_time = time.perf_counter()
    while True:
        global board, queue, bag
        print("\n=== Current Queue ===")
        print(queue)
        
        # Find the best move for the current board and queue
        best_board, best_move = find_best_placement(board, queue)
        
        if not best_board:
            print("No valid placement found")
            break
        
        # Parse the move string and apply the move
        piece_type, x, rotation = best_move.split('_')
        x = int(x[1:])
        piece_shape = PIECES[piece_type][rotation]
        new_board = drop_piece(piece_shape, board, x)
        
        # Clear lines if needed
        new_board = clear_lines(new_board)
       
        # Update the board and viewer
        board[:] = new_board  
        viewer.update_board(board)
        print(f"\nPlaced: {piece_type} at x={x}, rotation={rotation}")
       
        print_board(board)
        # Add new piece(s) to the queue from the bag and remove the used one
        queue, bag = add_piece_from_bag(queue, bag)
        queue.pop(0)

        # PPS calculation (average pieces placed per second)
        pieces_placed += 1
        elapsed = time.perf_counter() - start_time
        if elapsed > 0:
            stats.pps = pieces_placed / elapsed
            print(f"PPS (Pieces Per Second): {stats.pps:.2f}")

# Example: you can now access stats.pps from anywhere, e.g. in your viewer or another thread

# Start the game loop in a separate thread so the viewer remains responsive
game_thread = threading.Thread(target=game_loop, daemon=True)
game_thread.start()

# Start the viewer's main loop (blocks until window is closed)
viewer.mainloop()

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

