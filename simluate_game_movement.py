import pygame
import time
from utility.pieces_index import PIECES_index
from spins_funcions import try_place_piece_with_kick    
from spins import SRS_I_piece_kick_table, SRS_rest_pieces_kick_table, SRS_180_kick_table
from board_operations.checking_valid_placements import get_piece_rightmost_index_from_origin, get_piece_leftmost_index_from_origin,get_piece_lowest_index_from_origin
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
    new_position_array,spin=try_place_piece_with_kick(board, kick_table, position_array, rotation_goal)
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
    new_position_array,spin= try_place_piece_with_kick(board, kick_table, position_array, rotation_goal)
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
    new_position_array,spin = try_place_piece_with_kick(board, kick_table, position_array, rotation_goal)
    return new_position_array

def simulate_move(board, move, y_pos,key_pressed,up_y_movement=True):

    new_position_array = None

    if key_pressed is not None:
         print(f"Simulating move: {move} at y position {y_pos}")
    # Simulating move: S_x1_flat_0 at y position 19
    #time.sleep(811.1)  # Simulate a short delay for the move
    piece, xpos, rotation1, rotation2 = move.split('_')
    x = int(xpos[1:])
    rotation = rotation1 + "_" + rotation2
    pieces_cords = PIECES_index[piece][rotation]
    
    if key_pressed == pygame.K_RIGHT:
        print("Simulate move: Move piece right")
        if int(x) < 9-get_piece_rightmost_index_from_origin(pieces_cords):  # Assuming board width is 10
            x = str(int(x) + 1)
    
    elif key_pressed == pygame.K_LEFT:
        if int(x) > get_piece_leftmost_index_from_origin(pieces_cords)+2:
            x = str(int(x) - 1)
        print("Simulate move: Move piece left")
    
    elif key_pressed == pygame.K_UP:
        if y_pos > 0 and up_y_movement:
            y_pos -= 1
        print("Simulate move: Rotate piece")
    
    elif key_pressed == pygame.K_DOWN:
        if y_pos < 19-get_piece_lowest_index_from_origin(pieces_cords):
            y_pos += 1
        print("Simulate move: Soft drop")

    elif key_pressed == pygame.K_SPACE:
        print("Simulate move: Hard drop")


    elif key_pressed == pygame.K_v and piece != "O":
        print("Simulate move: Rotate piece counter-clockwise")
        new_position_array = rotate_left(rotation, board, piece, x, y_pos)
        pieces_cords = PIECES_index[piece][rotation]

    elif key_pressed == pygame.K_c and piece != "O":
        print("Simulate move: Rotate piece clockwise")
        new_position_array = rotate_right(rotation, board, piece, x, y_pos)
        pieces_cords = PIECES_index[piece][rotation]

    elif key_pressed == pygame.K_b and piece != "O":
        pass# error i cba solving xd
        
        #print("Simulate move: 180 rotate piece")
        #new_position_array = rotate_180(rotation, board, piece, x, y_pos)
        #pieces_cords = PIECES_index[piece][rotation]

    best_move_string = best_move_string_combiner(piece, x,rotation)
    if isinstance(new_position_array, tuple) or isinstance(new_position_array, list):
        x = new_position_array[2]
        y_pos = new_position_array[3]
        rotation = new_position_array[1]
        best_move_string = best_move_string_combiner(piece, x,rotation)
    if key_pressed is not None:    
        print(f"New simulated move: {best_move_string} at y position {y_pos}")

        print("\n")
    return board, best_move_string,y_pos, key_pressed

# TODO TOMORROW
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