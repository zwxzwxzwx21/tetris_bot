# TODO this is basically a rewrite of bruteforcer, it will be replaced somehow some time ago
import copy

from heuristic import analyze
from board_operations.board_operations import clear_lines, solidify_piece
from board_operations.checking_valid_placements import can_place, find_lowest_y_for_piece, place_piece
from utility.pieces_index import PIECES_index
from utility.print_board import print_board, debug_print
from config import SEARCH_DEPTH, BOARD_WIDTH, BOARD_HEIGHT
depth = SEARCH_DEPTH


def _generate_harddrop_moves_for_piece(board, piece, used_hold):
    """Generate hard-drop placements for one piece in all rotations."""
    moves = []

    for rotation_name, piece_pos_array in PIECES_index[piece].items():
        min_dx = min(dx for (dx, _dy) in piece_pos_array)
        max_dx = max(dx for (dx, _dy) in piece_pos_array)

        x_min = -min_dx
        x_max = 9 - max_dx

        for xpos in range(x_min, x_max + 1):
            ypos = find_lowest_y_for_piece(
                piece_pos_array,
                board,
                xpos,
                rotation_name,
                piece,
            )
            if can_place(
                piece_pos_array,
                board,
                ypos,
                xpos,
                rotation_name,
                piece,
                print_debug=False,
            ):
                moves.append((piece, rotation_name, xpos, ypos, used_hold))

    return moves


def _generate_legal_moves(board, queue, held_piece):
    """Generate legal moves for current piece and optional hold piece."""
    if not queue:
        return []

    current_piece = queue[0]
    moves = _generate_harddrop_moves_for_piece(board, current_piece, used_hold=False)

    if held_piece is not None and held_piece != current_piece:
        moves.extend(
            _generate_harddrop_moves_for_piece(board, held_piece, used_hold=True)
        )

    return moves


def _apply_move(board, queue, held_piece, move):
    """
    Apply move and return next search state.

    Move format:
      (piece, rotation, xpos, ypos, used_hold)
    """
    if not queue:
        return None

    piece, rotation, xpos, ypos, used_hold = move
    placed_board, success = place_piece(
        PIECES_index[piece][rotation],
        piece,
        board,
        xpos,
        ypos,
        rotation,
        print_debug=False,
        where_called_from="BnB._apply_move",
    )

    if not success:
        return None

    board_after_clear, cleared_lines = clear_lines(placed_board)
    next_queue = queue[1:]
    next_held_piece = queue[0] if used_hold else held_piece

    return board_after_clear, next_queue, next_held_piece, cleared_lines


def brute_force_reference(board, queue, depth, held_piece):
    """
    depthlimited search (no pruning) for validating BnB.

    Returns a dict with:
      - score: best sequence score
      - first_move: first move of the best sequence or None
      - sequence: full best sequence as a move list
      - visited_nodes: how many nodes were explored
    """

    effective_depth = min(depth, len(queue))
    stats = {"visited_nodes": 0}

    def _dfs(board_state, queue_state, hold_state, remaining_depth):
        stats["visited_nodes"] += 1

        if remaining_depth == 0 or not queue_state:
            return 0.0, []

        best_score = float("-inf")
        best_sequence = []
        legal_moves = _generate_legal_moves(board_state, queue_state, hold_state)

        if not legal_moves:
            return float("-inf"), []

        for move in legal_moves:
            transition = _apply_move(board_state, queue_state, hold_state, move)
            if transition is None:
                continue

            next_board, next_queue, next_hold, cleared_lines = transition
            move_score = analyze(next_board, cleared_lines)

            child_score, child_sequence = _dfs(
                next_board,
                next_queue,
                next_hold,
                remaining_depth - 1,
            )

            if child_score == float("-inf"):
                total_score = move_score
                sequence = [move]
            else:
                total_score = move_score + child_score
                sequence = [move] + child_sequence

            if total_score > best_score:
                best_score = total_score
                best_sequence = sequence

        return best_score, best_sequence

    score, sequence = _dfs(
        [row.copy() for row in board],
        list(queue),
        held_piece,
        effective_depth,
    )

    return {
        "score": score,
        "first_move": sequence[0] if sequence else None,
        "sequence": sequence,
        "visited_nodes": stats["visited_nodes"],
    }


def run_reference_comparison(board, queue, held_piece, depth=2):
    """
    Helper for debugging search quality on small depths.
    Use this as a correctness baseline before pruning.
    """
    brute_result = brute_force_reference(board, queue, depth, held_piece)
    return {
        "depth": min(depth, len(queue)),
        "bruteforce": brute_result,
    }


def BnB(board, queue, depth, held_piece, best_score_so_far):
    if depth == 0:
        return analyze(board)

    best_score = float('-inf')
    best_first_move = None
    arr_piece_info_array = []
    
    for piece in [queue[0], held_piece]:
        for rotation_name, piece_pos_array  in PIECES_index[piece].items():
            
            #start_x_pos = PIECES_startpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 1
            start_x_pos = min(dx for (dx, dy) in PIECES_index[piece][rotation_name]) * -1
            finish_x_pos = 10-(max(dx for (dx, dy) in PIECES_index[piece][rotation_name]) - min(dx for (dx, dy) in PIECES_index[piece][rotation_name]))
            #check all positions from the position we can place the piece on downwards,  if there is a place for a piece
            # add it to arrayt and see what results it gives (it may be inaccesible)
            for start_x in range(start_x_pos,finish_x_pos):
                
                lowest_y = find_lowest_y_for_piece(PIECES_index[piece][rotation_name], board, start_x,rotation_name,piece)

                for y in range(lowest_y-0, 21):  
                    if can_place(PIECES_index[piece][rotation_name], board, y, start_x,rotation_name,piece,print_debug=False):

                            arr_piece_info_array.append([piece, rotation_name, start_x, y])
        positions = copy.deepcopy(arr_piece_info_array)
        positions.sort(key=lambda pos: analyze(board, clear_lines(board)), reverse=True)
        
        for (x, rotation) in positions:
            new_board = solidify_piece(piece, x, rotation, board) # place_piece returns bool
            new_board = clear_lines(new_board)
            upper_bound = analyze(new_board) + depth * calculate_bonus(queue, held_piece,depth, board)
            if upper_bound < best_score_so_far:
                continue
            
            score = BnB(new_board, queue[1:], depth - 1, held_piece, best_score_so_far)
            
            if score > best_score:
                best_score = score
                best_score_so_far = max(best_score_so_far, score)
                if depth == SEARCH_DEPTH: #rememmber only first move because we want to return it at the end
                    best_first_move = (piece, x, rotation)  
    if depth == SEARCH_DEPTH:
        return best_first_move
    else:
        return best_score

def calculate_bonus(queue, held_piece, depth, board):
    """
    at firsts depth shouldnt exceed queue, as queue is only 7, i will rework it later
    ideas for bonus:
    uncovered tspin slots
    tspin slots with overhang
    high well, tetris 
    amount of blocks that is on the same color of checkerboard, tho that seems rather useless
    
    """
    if depth < len(queue):
        for piece in queue[:depth]:
            next_piece = queue[depth]
    pass

def all_valid_positions(piece, board, held_piece, queue):
    arr_piece_info_array = []
    held_piece_checked_loop = 0 # if there is no held piece, we only check once
    max_piece_loops = 1 if held_piece is None else 2
    while held_piece_checked_loop < max_piece_loops: # i dont know if bool works, we have to check twice and do while doesnt exist in python
        
        current_piece = queue[0] if held_piece_checked_loop == 0 else held_piece
        debug_print(f"CURRENT PIECE: {current_piece} held piece: {held_piece} loop: {held_piece_checked_loop}", "bruteforcing.py, function: find_best_placement")
        assert current_piece in PIECES_index
        
        for rotation_name, piece_pos_array  in PIECES_index[current_piece].items():
            
            #start_x_pos = PIECES_startpos_indexing_value[current_piece][rotation_name] if current_piece != 'O' else 1
            start_x_pos = min(dx for (dx, dy) in PIECES_index[current_piece][rotation_name]) * -1
            finish_x_pos = BOARD_WIDTH-(max(dx for (dx, dy) in PIECES_index[current_piece][rotation_name]) - min(dx for (dx, dy) in PIECES_index[current_piece][rotation_name]))
            #check all positions from the position we can place the piece on downwards,  if there is a place for a piece
            # add it to arrayt and see what results it gives (it may be inaccesible)
            for start_x in range(start_x_pos,finish_x_pos):
                
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

def BnB(board, queue, depth, held_piece, best_score_so_far):
    
    if depth == 0:
        return analyze(board)
    
    best_score = -999999
    best_first_move = None
    
    for piece in [queue[0], held_piece]:
        for (x, rotation) in all_valid_positions(piece, board):
            
            new_board = place(piece, x, rotation, board)
            new_board = clear_lines(new_board)
            
            upper_bound = analyze(new_board) + depth * BONUS
            if upper_bound < best_score_so_far:
                continue 
            
            score = BnB(new_board, queue[1:], depth - 1, held_piece, best_score_so_far)
            
            if score > best_score:
                best_score = score
                best_score_so_far = max(best_score_so_far, score) 
                if depth == SEARCH_DEPTH:  
                    best_first_move = (piece, x, rotation)
    
    if depth == SEARCH_DEPTH:
        return best_first_move  
    else:
        return best_score  


#best_move = BnB(board, queue, SEARCH_DEPTH, held_piece, best_score_so_far=-999999)


'''
best_score_so_far is used for pruning - its the best score weve found in any branch so far, and if we find a branch that cant beat it, we skip it
best_score_so_far is passed down the recursion, and updated whenever we find a better score. 
This way, as we explore better branches, we can prune more of the worse branches.
on depth == SEARCH_DEPTH we return the first move that leads to the best score, 
on lower depths we return the best score so far, so upper levels can compare and update best_score_so_far for better pruning.
one improvement that significantly increases pruning efficiency is sorting positions before entering the loop


positions = all_valid_positions(piece, board)
positions.sort(key=lambda pos: quick_score(pos, board), reverse=True)
# best solutions are explored first -> best_score_so_far quickly increases -> more branches are pruned'''