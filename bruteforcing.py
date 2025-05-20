import copy
from utility.print_board import print_board
from utility.pieces import PIECES  # importing piece lookup table

# Ensure PIECES is properly imported or defined
if not PIECES:
    raise ImportError("PIECES dictionary could not be imported or is empty.")

from board_operations.stack_checking import compare_to_avg, check_heights, check_holes, check_i_dep, uneven_stack_est, height_difference, get_heights
from board_operations.checking_valid_placements import drop_piece, place_piece, can_place
from tetrio_parsing.movement import move_piece
from board_operations.board_operations import clear_lines, apply_gravity
import time 

# --- 
# This module contains the core brute-force search logic for Tetris AI.
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

column_ranges  = {
    'i_flat': 6,
    'i_spin': 9,
    'o_flat': 8,
    's_flat': 7,
    's_spin': 8,
    'z_flat': 7,
    'z_spin': 8,
    'l_180': 7,
    'l_ccw': 8,
    'l_cw': 8,
    'l_flat': 7,
    'j_180': 7,
    'j_ccw': 8,
    'j_cw': 8,
    'j_flat': 7,
    't_180': 7,
    't_ccw': 8,
    't_cw': 8,
    't_flat': 7  
}

TIME_LIMIT = 3  # Maximum time (in seconds) allowed for the search
UNEVEN_THRESHOLD = 1.1  # Prune stacks that are too uneven
MAX_HEIGHT_DIFF = 11    # Prune stacks that are too tall

def evaluate_board(board):
    """
    Evaluates the board state using a simple heuristic:
    score = (number of holes) * 10 + (height difference)
    Lower scores are better.
    """
    holes = check_holes(board)
    height_diff, _ = height_difference(board)
    return holes * 10 + height_diff

def find_best_placement(board, queue):
    """
    Finds the best placement for the current queue of pieces using recursive search.
    Uses branch and bound to prune branches that cannot improve the best score found so far.
    Returns the resulting board and the move string for the first move in the best sequence.
    """
    start_time = time.perf_counter()
    best_board = None
    best_move = None
    best_score = float('inf')

    def recursive_search(board, queue, current_piece_index, move_history):
        nonlocal best_board, best_move, best_score

        # Stop searching if time limit exceeded
        if time.perf_counter() - start_time > TIME_LIMIT:
            return

        # Evaluate current board and prune if not better than best found so far
        score = evaluate_board(board)
        if score >= best_score:
            return  # Branch and Bound: prune this branch

        # If all pieces in the queue have been placed, update the best result
        if current_piece_index >= len(queue):
            best_board = board
            best_move = move_history[0]
            best_score = score
            return

        current_piece = queue[current_piece_index]
        if current_piece not in PIECES:
            print(f"Error: Piece '{current_piece}' is not defined in PIECES.")
            return

        # Try all rotations and horizontal positions for the current piece
        for rotation_name, piece_shape in PIECES[current_piece].items():
            max_x = 10 - len(piece_shape[0])
            for x in range(max_x + 1):
                new_board = drop_piece(piece_shape, copy.deepcopy(board), x)
                if new_board is None:
                    continue

                # Prune placements that are too uneven, too tall, or have holes
                height_diff, heights = height_difference(new_board)
                uneven = uneven_stack_est(heights)
                if (uneven > UNEVEN_THRESHOLD or 
                    height_diff > MAX_HEIGHT_DIFF or 
                    check_holes(new_board)):
                    continue

                move = f"{current_piece}_x{x}_{rotation_name}"
                recursive_search(
                    new_board,
                    queue,
                    current_piece_index + 1,
                    [*move_history, move]
                )

    # Start the recursive search from the current board and queue
    recursive_search(board, queue, 0, [])
    return best_board, best_move

# ---
# How and when to use:
# - Call find_best_placement(board, queue) to get the best move for the current state.
# - Use in your main game loop to drive the AI's decisions.
# - The search is limited by TIME_LIMIT for performance.
# - You can tune the evaluation function and pruning thresholds for different play styles or AI goals.
# ---