import copy
from utility.print_board import print_board
from utility.pieces import * # importing piece lookuptable
from board_operations.stack_checking import compare_to_avg, check_heights, check_holes, check_i_dep, uneven_stack_est, height_difference
from board_operations.checking_valid_placements import drop_piece,place_piece,can_place

def bruteforce_placements(board, pieces, current_piece_index=0):
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
        'i_flat': 6  ,
        'i_spin': 9  ,

        'o_flat': 8  ,

        's_flat': 7  ,
        's_spin': 8  ,

        'z_flat': 7  ,
        'z_spin': 8  ,

        'l_180': 7  ,
        'l_ccw': 8  ,
        'l_cw': 8  ,
        'l_flat': 7  ,

        'j_180': 7 ,
        'j_ccw': 8  ,
        'j_cw': 8  ,
        'j_flat': 7  ,

        't_180': 7  ,
        't_ccw': 8  ,
        't_cw': 8  ,
        't_flat': 7  
    }

    piece_objects = {}
    for piece_type in PIECES:
        for rotation_name in PIECES[piece_type]:
            key = f"{piece_type.lower()}_{rotation_name}"
            piece_objects[key] = PIECES[piece_type][rotation_name]

    if current_piece_index >= len(pieces):
        print(f"Final board after placing {len(pieces)} pieces:")
        print_board(board)
        return board

    current_piece_type = pieces[current_piece_index]

    for rotation_type in rotations[current_piece_type]:
        rotation_key = f"{current_piece_type.lower()}_{rotation_type}"
        max_x = column_ranges[rotation_key]

        for xpos in range(max_x):
            board_copy = copy.deepcopy(board)
            piece = piece_objects[rotation_key]
            
            if drop_piece(piece, board_copy, xpos):
                continue  # Skip invalid placements
                
            # Check board state
            if not check_holes(board_copy):
                max_diff, heights = height_difference(board_copy)
                
                
                height_ok = max_diff < 4
                uneven_ok = uneven_stack_est(heights) < 2
                no_i_dep = not check_i_dep(heights)
                
                
                if current_piece_type == 'I':
                    if height_ok and uneven_ok and no_i_dep:
                        result = bruteforce_placements(
                            board_copy, pieces, current_piece_index + 1
                        )
                        if result:
                            return result
                else:
                    if height_ok and uneven_ok and no_i_dep:
                        result = bruteforce_placements(
                            board_copy, pieces, current_piece_index + 1
                        )
                        if result:
                            return result

    return None  


   