import pygame
import time
from utility.pieces_index import PIECES_index
from board_operations.checking_valid_placements import get_piece_rightmost_index_from_origin, get_piece_leftmost_index_from_origin
def best_move_string_combiner(piece, xpos, rotation):
    return f"{piece}_x{xpos}_{rotation}" # XD

def simulate_move(board, move, y_pos,key_pressed,up_y_movement=True):
    print(f"Simulating move: {move} at y position {y_pos}")
    # Simulating move: S_x1_flat_0 at y position 19
    #time.sleep(811.1)  # Simulate a short delay for the move
    piece, xpos, rotation1, rotation2 = move.split('_')
    x = int(xpos[1:])
    rotation = rotation1 + "_" + rotation2
    pieces_cords = PIECES_index[piece][rotation]
    if key_pressed == pygame.K_RIGHT:
        print("Simulate move: Move piece right")
        if int(x) < 9-get_piece_rightmost_index_from_origin(PIECES_index[piece][rotation]):  # Assuming board width is 10
            x = str(int(x) + 1)
    elif key_pressed == pygame.K_LEFT:
        if int(x) > get_piece_leftmost_index_from_origin(PIECES_index[piece][rotation])+2:
            x = str(int(x) - 1)
        print("Simulate move: Move piece left")
    elif key_pressed == pygame.K_UP:
        if y_pos > 0 and up_y_movement:
            y_pos -= 1
        print("Simulate move: Rotate piece")
    elif key_pressed == pygame.K_DOWN:
        if y_pos < 19:
            y_pos += 1
        print("Simulate move: Soft drop")
    elif key_pressed == pygame.K_SPACE:
        print("Simulate move: Hard drop")
    
    best_move_string = best_move_string_combiner(piece, x,rotation)

    return board, best_move_string,y_pos, key_pressed
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