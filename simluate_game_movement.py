import pygame
import time
from utility.pieces_index import PIECES_index

def best_move_string_combiner(piece, xpos, rotation):
    return f"{piece}_{xpos}_{rotation}" # XD

def simulate_move(board, move, y_pos,key_pressed,up_y_movement=True):
    print(f"Simulating move: {move} at y position {y_pos}")
    # Simulating move: S_x1_flat_0 at y position 19
    #time.sleep(811.1)  # Simulate a short delay for the move
    piece, xpos, rotation1, rotation2 = move.split('_')
    rotation = rotation1 + "_" + rotation2
    pieces_cords = PIECES_index[piece][rotation]
    if key_pressed == pygame.K_RIGHT:
        print("Simulate move: Move piece right")
    elif key_pressed == pygame.K_LEFT:
        print("Simulate move: Move piece left")
    elif key_pressed == pygame.K_UP:
        print("Simulate move: Rotate piece")
    elif key_pressed == pygame.K_DOWN:
        print("Simulate move: Soft drop")
    elif key_pressed == pygame.K_SPACE:
        print("Simulate move: Hard drop")
    
    best_move_string = best_move_string_combiner(piece, xpos,rotation)



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