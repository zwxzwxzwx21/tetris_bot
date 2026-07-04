
from __future__ import annotations

from typing import Callable

from board_operations.board_operations import clear_lines
from board_operations.checking_valid_placements import (
    can_place,
    find_lowest_y_for_piece,
    place_piece,
)
from config import BOARD_WIDTH, BOARD_HEIGHT, BNB_SEARCH_DEPTH,_OPTIMISTIC_FUTURE_STEP
from heuristic import analyze
from utility.pieces_index import PIECES_index

Move = tuple[str, str, int, int, bool]
BonusFn = Callable[[list[str], str | None, int, list[list[str]]], float]
from calculate_upper_bound import CalculateUpperBound

# _OPTIMISTIC_FUTURE_STEP = CalculateUpperBound.upper_bound


def _get_moves_from_all_valid(board, queue, held_piece):
    """Converts the result of all_valid_positions to BnB format (with used_hold).

    Args:
        board (list[list[str]]): The current board state.
        queue (list[str]): The current piece queue.
        held_piece (str | None): The currently held piece.
        
    Returns:
        list[Move]: A list of moves in BnB format.
    """
    if not queue:
        return []
    
    moves = []
    
    for piece, rot, x, y in all_valid_positions(queue[0], board, None, queue):
        moves.append((piece, rot, x, y, False))
    
    if held_piece is not None and held_piece != queue[0]:
        for piece, rot, x, y in all_valid_positions(held_piece, board, None, [held_piece]):
            moves.append((piece, rot, x, y, True))
    
    return moves


def _apply_move(board, queue, held_piece, move):
    """Applies a move to the board and returns the resulting state.

    Args:
        board (list[list[str]]): The current board state.
        queue (list[str]): The current piece queue.
        held_piece (str | None): The currently held piece.
        move (Move): The move to apply.

    Returns:
        tuple[list[list[str]], list[str], str | None, int] | None: A tuple containing the new board state, the updated queue, the updated held piece, and the number of cleared lines, or None if the move is invalid.        
    
    """
    if not queue:
        return None

    piece, rotation, xpos, ypos, used_hold = move
    piece_pos_array = PIECES_index[piece][rotation]

    placed_board, success = place_piece(
        piece_pos_array, piece, board, xpos, ypos, rotation,
        print_debug=False, where_called_from="BnB._apply_move"
    )
    
    if not success:
        return None

    board_after_clear, cleared_lines = clear_lines(placed_board)

    if used_hold:
        next_queue = list(queue)
        next_held_piece = None
    else:
        next_queue = list(queue[1:])
        next_held_piece = held_piece

    return board_after_clear, next_queue, next_held_piece, cleared_lines

def calculate_bonus(queue, held_piece, depth, board):  #TODO: implement a bonus function that can be used to tune the search
    
    _ = queue, held_piece, depth, board
    return 0.0


def branch_and_bound_search(
    board,
    queue,
    depth,
    held_piece,
    best_score_so_far=float("-inf"),
    bonus_fn: BonusFn = calculate_bonus,
):
    """Performs a branch and bound search to find the best move sequence.

    Args:
        board (list[list[str]]): The current board state.
        queue (list[str]): The current piece queue.
        depth (int): The search depth.
        held_piece (str | None): The currently held piece.
        best_score_so_far (float, optional): The best score found so far. Defaults to float("-inf").
        bonus_fn (BonusFn, optional): A function to calculate bonus scores. Defaults to calculate_bonus.

    Returns:
        dict: A dictionary containing the best score, the first move, the sequence of moves, and statistics about visited and pruned nodes.
    """
    effective_depth = min(depth, len(queue))
    if effective_depth <= 0 or not queue:
        return {
            "score": 0.0,
            "first_move": None,
            "sequence": [],
            "visited_nodes": 0,
            "pruned_nodes": 0,
        }

    stats = {"visited_nodes": 0, "pruned_nodes": 0}
    global_best_total = float(best_score_so_far)

    def _dfs(board_state, queue_state, hold_state, remaining_depth, running_total):
        nonlocal global_best_total
        stats["visited_nodes"] += 1

        if remaining_depth == 0 or not queue_state:
            if running_total > global_best_total:
                global_best_total = running_total
            return 0.0, []

        scored_moves = []
        for move in _get_moves_from_all_valid(board_state, queue_state, hold_state):
            transition = _apply_move(board_state, queue_state, hold_state, move)
            if transition is None:
                continue

            next_board, next_queue, next_hold, cleared_lines = transition
            move_score = analyze(next_board, cleared_lines) + bonus_fn(
                next_queue,
                next_hold,
                remaining_depth - 1,
                next_board,
            )
            scored_moves.append((move_score, move, next_board, next_queue, next_hold))

        if not scored_moves:
            if running_total > global_best_total:
                global_best_total = running_total
            return float("-inf"), []

        scored_moves.sort(key=lambda item: item[0], reverse=True)
        
        best_local_score = float("-inf")
        best_local_sequence = []

        for move_score, move, next_board, next_queue, next_hold in scored_moves:
            optimistic_upper = (
                running_total
                + move_score
                + (remaining_depth - 1) * _OPTIMISTIC_FUTURE_STEP
            )
            if optimistic_upper <= global_best_total:
                stats["pruned_nodes"] += 1
                continue

            child_score, child_sequence = _dfs(
                next_board,
                next_queue,
                next_hold,
                remaining_depth - 1,
                running_total + move_score,
            )

            if child_score == float("-inf"):
                total_score = move_score
                sequence = [move]
            else:
                total_score = move_score + child_score
                sequence = [move] + child_sequence

            if total_score > best_local_score:
                best_local_score = total_score
                best_local_sequence = sequence

                candidate_total = running_total + total_score
                if candidate_total > global_best_total:
                    global_best_total = candidate_total

        if best_local_score == float("-inf"):
            if running_total > global_best_total:
                global_best_total = running_total

        return best_local_score, best_local_sequence

    score, sequence = _dfs(
        [row.copy() for row in board],
        list(queue),
        held_piece,
        effective_depth,
        0.0,
    )

    return {
        "score": score,
        "first_move": sequence[0] if sequence else None,
        "sequence": sequence,
        "visited_nodes": stats["visited_nodes"],
        "pruned_nodes": stats["pruned_nodes"],
    }


def all_valid_positions(piece, board, held_piece, queue):
    """Generates all valid positions for a given piece on the board.
    
    Args:
        piece (str): The piece to place.
        board (list[list[str]]): The current board state.
        held_piece (str | None): The currently held piece.
        queue (list[str]): The current piece queue.

    Returns:
        list[tuple[str, str, int, int]]: A list of valid positions for the piece, each represented as a tuple containing the piece, its rotation, and its x and y coordinates.
    """
    arr_piece_info_array = []
    held_piece_checked_loop = 0 # if there is no held piece, we only check once
    max_piece_loops = 1 if held_piece is None else 2
    while held_piece_checked_loop < max_piece_loops: # i dont know if bool works, we have to check twice and do while doesnt exist in python
        
        current_piece = queue[0] if held_piece_checked_loop == 0 else held_piece
        assert current_piece in PIECES_index
        
        for rotation_name, piece_pos_array  in PIECES_index[current_piece].items():
            if current_piece == "O" and rotation_name in ["spin_R", "spin_L","flat_2"]:    
                continue  # O piece has no spins
            #start_x_pos = PIECES_startpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 1
            start_x_pos = min(dx for (dx, dy) in PIECES_index[current_piece][rotation_name]) * -1
            finish_x_pos = BOARD_WIDTH - 1 - max(dx for (dx, _dy) in PIECES_index[current_piece][rotation_name])
            #check all positions from the position we can place the piece on downwards,  if there is a place for a piece
            # add it to arrayt and see what results it gives (it may be inaccesible)
            for start_x in range(start_x_pos, finish_x_pos + 1):
                
                lowest_y = find_lowest_y_for_piece(PIECES_index[current_piece][rotation_name], board, start_x,rotation_name,current_piece)

                for y in range(lowest_y-0, BOARD_HEIGHT+1):  
                    if can_place(PIECES_index[current_piece][rotation_name], board, y, start_x,rotation_name,current_piece,print_debug=False):

                            arr_piece_info_array.append([current_piece, rotation_name, start_x, y])
        held_piece_checked_loop += 1
    
    possible_moves = []   
    for position_info in arr_piece_info_array:
        
        new_board, is_place_piece_successful = place_piece(PIECES_index[position_info[0]][position_info[1]],position_info[0], board, position_info[2], position_info[3], position_info[1],print_debug=False,where_called_from="bruteforcing, fuycntion: try best placement")
        if not is_place_piece_successful:
            
            continue
        possible_moves.append((position_info[0], position_info[1], position_info[2], position_info[3]))
    
    return possible_moves


def _move_to_goal_string(move: Move):
    
    """Converts a move into a string representation.

    Args:
        move (Move): The move to convert.

    Returns:
        str: The string representation of the move.
    """
        
    piece, rotation, xpos, _ypos, _used_hold = move
    return f"{piece}_x{xpos}_{rotation}"


def find_best_placement_bnb(
    board,
    queue,
    held_piece,
    depth=BNB_SEARCH_DEPTH,
    best_score_so_far=float("-inf"),
    bonus_fn: BonusFn = calculate_bonus,
):
    """
    Args:
        board (list[list[str]]): The current board state.
        queue (list[str]): The current piece queue.
        held_piece (str | None): The currently held piece.
        depth (int, optional): The search depth. Defaults to BNB_SEARCH_DEPTH.
        best_score_so_far (float, optional): The best score found so far. Defaults to float("-inf").
        bonus_fn (BonusFn, optional): A function to calculate bonus scores. Defaults to calculate_bonus.
        
    Returns:
      (move_history, best_move_str, best_move_y, used_hold)
    """

    result = branch_and_bound_search(
        board,
        queue,
        depth,
        held_piece,
        best_score_so_far=best_score_so_far,
        bonus_fn=bonus_fn,
    )
    best_move = result["first_move"]
    if best_move is None:
        return None

    best_move_str = _move_to_goal_string(best_move)
    best_move_y = best_move[3]
    used_hold = best_move[4]
    move_history = [best_move_str]
    return move_history, best_move_str, best_move_y, used_hold
