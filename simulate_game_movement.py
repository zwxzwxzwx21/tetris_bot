import copy
import pygame # type: ignore
import time
from utility.pieces_index import PIECES_index,PIECES_index_sim_game_left,PIECES_index_sim_game_right
from spins_funcions import try_place_piece_with_kick    
from heuristic import aggregate,bumpiness,blockade,tetrisSlot,check_holes2,iDependency,analyze

from spins import SRS_I_piece_kick_table, SRS_rest_pieces_kick_table, SRS_180_kick_table
from board_operations.checking_valid_placements import get_piece_rightmost_index_from_origin, get_piece_leftmost_index_from_origin,get_piece_lowest_index_from_origin,get_piece_rightmost_index_from_origin_abs, get_piece_leftmost_index_from_origin_abs,get_piece_lowest_index_from_origin_abs, place_piece
def best_move_string_combiner(piece, xpos, rotation):
    return f"{piece}_x{xpos}_{rotation}" # XD

def rotate_left(rotation,board,piece,xpos,ypos):

    rotation_goal = ""
    if rotation == "flat_0":
        rotation_goal = "spin_L"
    elif rotation == "spin_L":
        rotation_goal = "flat_2"
    elif rotation == "flat_2":
        rotation_goal = "spin_R"
    elif rotation == "spin_R":
        rotation_goal = "flat_0"
    if piece == "I":
        kick_table = SRS_I_piece_kick_table
    else:
        kick_table = SRS_rest_pieces_kick_table
    position_array = [piece, rotation, xpos, ypos]
    new_position_array,spin=try_place_piece_with_kick(board, kick_table, position_array, rotation_goal,print_offset=True)
    return new_position_array

def rotate_right(rotation,board,piece,xpos,ypos):
    rotation_goal = ""
    if rotation == "flat_0":
        rotation_goal = "spin_R"
    elif rotation == "spin_R":
        rotation_goal = "flat_2"
    elif rotation == "flat_2":
        rotation_goal = "spin_L"
    elif rotation == "spin_L":
        rotation_goal = "flat_0"
    if piece == "I":
        kick_table = SRS_I_piece_kick_table
    else:
        kick_table = SRS_rest_pieces_kick_table
    position_array = [piece, rotation, xpos, ypos]
    new_position_array,spin= try_place_piece_with_kick(board, kick_table, position_array, rotation_goal,print_offset=True)
    return new_position_array

def rotate_180(rotation,board,piece,xpos,ypos):
    rotation_goal = ""
    if rotation == "flat_0":
        rotation_goal = "flat_2"
    elif rotation == "spin_R":
        rotation_goal = "spin_L"
    elif rotation == "flat_2":
        rotation_goal = "flat_0"
    elif rotation == "spin_L":
        rotation_goal = "spin_R"
    kick_table = SRS_180_kick_table
    position_array = [piece, rotation, xpos, ypos]
    new_position_array,spin = try_place_piece_with_kick(board, kick_table, position_array, rotation_goal,print_offset=True)
    return new_position_array

def simulate_move(board, move, y_pos,key_pressed, held_piece, das_info, up_y_movement=True):
    """
    das_info: dict with {'left': bool, 'right': bool} - True means DAS is charged and ARR triggered
    """
    
    new_position_array = None

    if key_pressed is not None:
         print(f"Simulating move: {move} at y position {y_pos}")
    # Simulating move: S_x1_flat_0 at y position 19
    #time.sleep(811.1)  # Simulate a short delay for the move
    piece, xpos, rotation1, rotation2 = move.split('_')
    x = int(xpos[1:])
    change_held_piece_flag = False
    rotation = rotation1 + "_" + rotation2
    if piece != "O":
        pieces_cords = PIECES_index[piece][rotation]
        #print(f"{pieces_cords }, rotation={rotation}")
        #print(f"9- rightmost: {9-PIECES_index_sim_game_right[piece][rotation]}, rightmost: {PIECES_index_sim_game_right[piece][rotation]}, leftmost: {PIECES_index_sim_game_left[piece][rotation]}, rotation: {rotation}, lowest: {get_piece_lowest_index_from_origin_abs(pieces_cords)}")
    
    # handle DAS moves
    if das_info.get('right', False):
        if int(x) < 9-PIECES_index_sim_game_right[piece][rotation]:
            x = int(x) + 1
    elif das_info.get('left', False):
        if int(x) > PIECES_index_sim_game_left[piece][rotation]:
            x = int(x) - 1
    elif das_info.get('down', False):
        if piece == "O":
            if y_pos < 19:
                y_pos += 1
        elif y_pos < 19-get_piece_lowest_index_from_origin(pieces_cords):
            y_pos += 1
    
    # initial tap
    if key_pressed == pygame.K_RIGHT:
        if int(x) < 9-PIECES_index_sim_game_right[piece][rotation]:
            x = int(x) + 1
            
    elif key_pressed == pygame.K_LEFT:
        if int(x) > PIECES_index_sim_game_left[piece][rotation]:
            x = int(x) - 1
    
    elif key_pressed == pygame.K_RSHIFT or key_pressed == pygame.K_LSHIFT:
        if y_pos > 0 and up_y_movement:
            y_pos -= 1
    
    elif key_pressed == pygame.K_DOWN:
        if piece == "O":
            if y_pos < 19:
                y_pos += 1
        elif y_pos < 19-get_piece_lowest_index_from_origin(pieces_cords):
            y_pos += 1  

    elif key_pressed == pygame.K_c and piece != "O":
        new_position_array = rotate_left(rotation, board, piece, x, y_pos)
        pieces_cords = PIECES_index[piece][rotation]

    elif key_pressed == pygame.K_v and piece != "O":
        new_position_array = rotate_right(rotation, board, piece, x, y_pos)
        pieces_cords = PIECES_index[piece][rotation]

    elif key_pressed == pygame.K_x and piece != "O":
        pass# error i cba solving xd
        # problem is that keys are being incorrect and insetad of having rotation flat_0 for example, its 0-2 etc
        #print("Simulate move: 180 rotate piece")
        #new_position_array = rotate_180(rotation, board, piece, x, y_pos)
        #pieces_cords = PIECES_index[piece][rotation]
    
    elif key_pressed == pygame.K_r:
        board = [[' ' for _ in range(10)] for _ in range(20)]
    
    elif key_pressed == pygame.K_UP:
            
        rotation = "flat_0" # doesnt matter, can be changed by a user
        x = 4
        y_pos = 4
        change_held_piece_flag = True

        print(f"piece: {piece}, held_piece: {held_piece}, queue: ")    

    # make it so it will encount ghost piece instead of already placed piece
    board_analyze = copy.deepcopy(board)
    board_analyze = place_piece(PIECES_index[piece][rotation], piece, board_analyze, int(x), y_pos, rotation)[0]

    #print(f"creating best move string from new position array: piece={piece}, x={x}, rotation={rotation}")
    best_move_string = best_move_string_combiner(piece, x,rotation)
    if isinstance(new_position_array, tuple) or isinstance(new_position_array, list):
        x = new_position_array[2]
        y_pos = new_position_array[3]
        rotation = new_position_array[1]
        best_move_string = best_move_string_combiner(piece, x,rotation)
    if key_pressed is not None:    
        print(f"New simulated move: {best_move_string} at y position {y_pos}")

        print("\n")

        analyze(board_analyze,0)
   # print(f"returning best move string: {best_move_string}")
    return board, best_move_string,y_pos, key_pressed, held_piece ,change_held_piece_flag

# TODO 
# fix the kick table of pieces, i piece is broken 100%

# fix the X position limit on pieces, rotations allow the piece to go out of bounds
# on top of that, some pieces just cant move left or right enough due to starting position being off

# pygame.K_LEFT - Left arrow key
# pygame.K_RIGHT - Right arrow key  
# pygame.K_UP - Up arrow key
# pygame.K_DOWN - Down arrow key
# pygame.K_SPACE - Space bar
# pygame.K_z - Z key
# pygame.K_x - X key
# pygame.K_c - C key
# pygame.K_RETURN - Enter key
# pygame.K_ESCAPE - Escape key