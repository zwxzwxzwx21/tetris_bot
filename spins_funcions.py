
from board_operations.checking_valid_placements import place_piece    
from utility.pieces_index import PIECES_index

def is_valid_position(board, piece_coords, x, y):
    """Fast check if piece can be placed at x, y without copying board"""
    for dx, dy in piece_coords:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < 10 and 0 <= ny < 20):
            return False
        if board[ny][nx] != ' ':
            return False
    return True

def try_place_piece_with_kick(board,kick_table,info_array,rotation_goal):
    """this function tries to place a piece by using a spin, if it fails, it tries puttinga  kick offset on it
    when fails completely,returns none"""
    # rotation goal is either left right or 180, determines what offset to set 
    # this one makes the data sets like work, because you need same data twice which is different for some reason lol, i should fix it at some point

    
    rotated_piece = PIECES_index[info_array[0]][rotation_goal]
    
    str_piece_rotation_goal = rotation_goal
    rotation_goal = rotation_goal[-1]
    
    kick_key = info_array[1][-1]+'-'+rotation_goal
    
    for offset in kick_table[kick_key]:
        target_x = info_array[2] + int(offset[0])
        target_y = info_array[3] + int(offset[1])
        
        if is_valid_position(board, rotated_piece, target_x, target_y):
            if offset == (0,0):
                spin = False
            else:
                spin = True
            return [info_array[0],str_piece_rotation_goal,info_array[2] + int(offset[0]), info_array[3] + int(offset[1])],spin
            #distinguishing spins would be easier than just making sure they work so spins dont do mpre than normal clears

    return info_array, False

