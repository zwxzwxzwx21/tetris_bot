import copy
import time 

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

# --- 
# This module contains the core brute-force search logic for Tetris.
# It evaluates all possible placements for a given queue of pieces and returns the best move.
# The search uses branch and bound to prune unpromising branches and is limited by a time threshold.
# ---

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
    """
    Finds the best placement for the current queue of pieces using recursive search.
    Uses branch and bound to prune branches that cannot improve the best score found so far.
    Returns the resulting board and the move string for the first move in the best sequence.
    """
    start_time = time.perf_counter()
    best_attack = 0
    best_board = None
    best_move = None
    attack = 0
    def recursive_search(board, queue, current_piece_index, move_history, combo, attack):
        print(current_piece_index,queue )
        nonlocal best_board, best_move, best_attack
        global MOVES_DONE, MOVES_REMOVED
        t_rec_start = time.perf_counter()
        #print('test')
        # --- TIME LIMIT ---
        # this one seems pointless really
        if time.perf_counter() - start_time > TIME_LIMIT:
            return

        # --- END CONDITION ---
        if current_piece_index >= len(queue):
            best_board = board
            best_move = move_history[0] 
            best_attack = attack
            return

        # --- PIECE LOOKUP ---
        current_piece = queue[current_piece_index]
        if current_piece not in PIECES:
            print(f"Error: Piece '{current_piece}' is not defined in PIECES.")
            return

        # --- ROTATIONS & POSITIONS ---
        for rotation_name, piece_shape in PIECES[current_piece].items():
            t_rot_start = time.perf_counter()
            max_x = 10 - len(piece_shape[0])
            for x in range(max_x + 1):
                # --- DROP PIECE ---
                new_board = drop_piece(piece_shape, copy.deepcopy(board), x)
                board_after_clear,cleared_lines = clear_lines(new_board)
                #print_board(board_after_clear)
                
                attack,combo = count_lines_clear(cleared_lines,combo,board_after_clear)
                #print(f"attack: {attack}\ncombo: {combo}" )
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
                t0 = time.perf_counter()
                move = f"{current_piece}_x{x}_{rotation_name}"
                
                print_board(board_after_clear)  # Debugging output
                
                recursive_search(
                    board_after_clear,
                    queue,
                    current_piece_index + 1,
                    [*move_history, move],
                    combo,
                    attack
                )
                t1 = time.perf_counter()
                ms = (t1 - t0) * 1000
                if ms > 1:
                    print(f"recursive_search call: {ms:.2f} ms")

            t_rot_end = time.perf_counter()
            ms_rot = (t_rot_end - t_rot_start) * 1000
            if ms_rot > 1:
                print(f"rotation loop (piece {current_piece}, rot {rotation_name}): {ms_rot:.2f} ms")

        t_rec_end = time.perf_counter()
        ms_rec = (t_rec_end - t_rec_start) * 1000
        if ms_rec > 1:
            print(f"recursive_search total: {ms_rec:.2f} ms (piece {current_piece}, idx {current_piece_index})")

    # Start the recursive search from the current board and queue
    recursive_search(board, queue, 0, [], combo, attack)
    return best_board, best_move, best_attack

# ---
# How and when to use:
# - Call find_best_placement(board, queue) to get the best move for the current state.
# - Use in your main game loop to drive the AI's decisions.
# - The search is limited by TIME_LIMIT for performance.
# - You can tune the evaluation function and pruning thresholds for different play styles or AI goals.
# ---

'''a,b =find_best_placement(board_, ['O','I','S'])  
for row in a:
    print(' '.join(row))
print("Best move:", b)
print("Moves done:", MOVES_DONE)
print("Moves removed:", MOVES_REMOVED)'''