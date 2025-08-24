import copy
import time 
import logging

from utility.print_board import board as board_ # yeah i know its stupid that its in print_board.py i dun care
from utility.print_board import print_board  # Importing print_board for debugging output
from tetrio_parsing.calculate_attack import count_lines_clear 
from utility.pieces import PIECES  # importing piece lookup table
from board_operations.stack_checking import check_holes, uneven_stack_est, height_difference
from board_operations.checking_valid_placements import drop_piece 
from board_operations.board_operations import clear_lines
# Ensure PIECES is properly imported or defined
if not PIECES:
    raise ImportError("PIECES dictionary could not be imported or is empty.")
DEBUG = True

rotations = {
    'I': ['flat', 'spin'],
    'O': ['flat'],
    'S': ['flat', 'spin'],
    'Z': ['flat', 'spin'],
    'L': ['flat', '180', 'cw', 'ccw'],
    'J': ['flat', '180', 'cw', 'ccw'],
    'T': ['flat', '180', 'cw', 'ccw']
}
MOVES_DONE = 0
MOVES_REMOVED = 0  
TIME_LIMIT = 999  # Maximum time (in seconds) allowed for the search
UNEVEN_THRESHOLD = 1.1  # Prune stacks that are too uneven
MAX_HEIGHT_DIFF = 6 # Prune stacks that are too tall

def find_best_placement(board, queue, combo):
    
    best_attack = 0
    best_move = None
    attack = 0
    attack_move_array = [[],0,0] # test array that connects move with attack, idk if tuple would be better, i think its not mutable
    #move, attack, combo
    def recursive_search(board, queue, current_piece_index, move_history, combo, attack):
        logging.debug(f"current_piece_index: {current_piece_index}, queue: {queue}")
        nonlocal best_move, best_attack
        global MOVES_DONE, MOVES_REMOVED
        
        # --- END CONDITION ---
        if best_attack < attack:
            best_attack = attack
            attack_move_array[1] = attack
            attack_move_array[0] = move_history
        logging.debug(move_history)
        logging.debug(attack_move_array)
        if current_piece_index >= len(queue):
            best_move = attack_move_array[0]
            return

        # --- PIECE LOOKUP ---
        current_piece = queue[current_piece_index]
        #another of those that never will happen but why no
        if current_piece not in PIECES:
            if DEBUG:
                logging.debug(f"Error: Piece '{current_piece}' is not defined in PIECES.")
            return

        # --- ROTATIONS & POSITIONS ---
        for rotation_name, piece_shape in PIECES[current_piece].items():
            max_x = 10 - len(piece_shape[0])
            for x in range(max_x + 1):
                # --- DROP PIECE ---
                new_board = drop_piece(piece_shape, copy.deepcopy(board), x)
                board_after_clear,cleared_lines = clear_lines(new_board)
                #print_board(board_after_clear)

                attack_for_clear,attack_move_array[2] = count_lines_clear(cleared_lines,combo,board_after_clear)
                attack += attack_for_clear
                MOVES_DONE += 1
                if new_board is None:
                    continue
                
                # --- HEIGHT & UNEVEN CHECK ---
                height_diff, heights = height_difference(board_after_clear)
                uneven = uneven_stack_est(heights)

                # --- HOLES CHECK ---
                holes = check_holes(board_after_clear)

                if (uneven > UNEVEN_THRESHOLD or 
                    height_diff > MAX_HEIGHT_DIFF or check_holes(board_after_clear) > 0):
                    MOVES_REMOVED += 1 
                    continue

                # --- RECURSIVE CALL ---
                move = f"{current_piece}_x{x}_{rotation_name}"
                
                recursive_search(
                    board_after_clear,
                    queue,
                    current_piece_index + 1,
                    [*move_history, move],
                    attack_move_array[2],
                    attack
                )
            
    recursive_search(board, queue, 0, [], combo, attack)
    return best_move, best_attack
