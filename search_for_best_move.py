from board_operations.checking_valid_placements import find_lowest_y_for_piece, sideways_movement_simulation, place_piece, soft_drop_simulation_returning_ypos
from spins import SRS_rest_pieces_kick_table, SRS_I_piece_kick_table
from utility.print_board import print_board
from utility.pieces_index import PIECES_index, PIECES_startpos_indexing_value, PIECES_xpos_indexing_value
from spins_funcions import try_place_piece
import time
from collections import deque
PRINT_MODE = False
def search_for_best_move(goal, board, best_move_y_pos):
    
    '''this function would search for the best move to reach goal on board, goal is string like 'T_x4_flat_0'
    would return move history to reach that goal'''
    
    goal_parts = goal.split('_')  # ['T','x4','flat','0']
    piece = goal_parts[0]
    x_pos = int(goal_parts[1][1:])
    rotation = goal_parts[2] + '_' + goal_parts[3]  # flat_0
    y_pos = best_move_y_pos
    came_from = {}
    goal_as_pos_array = [piece, rotation, x_pos, y_pos]
    rotations = ["flat_0", "spin_R", "flat_2", "spin_L"]
    queue_of_positions = deque()  # this array is like: if we have an X position and we rotate it, if the new position is already in the array, we skip it, otherwise we could have infinite loops
    
    # piece info array example ("T",'flat_0',x(fore xample 4),y(for example 15))
    for rot in rotations:
        if piece == "O" and rot in ["spin_R", "spin_L","flat_2"]:
            continue  # O piece has no spins
        for dx in range(PIECES_startpos_indexing_value[piece][rot], 11 - PIECES_xpos_indexing_value[piece][rot]):
            lowest_Y = find_lowest_y_for_piece(PIECES_index[piece][rot], board, dx, rot, piece=piece)
            start_pos = [piece, rot, dx, lowest_Y]
            queue_of_positions.append(start_pos )  # apprends all the places available without tucking or spins/kicks
            came_from[tuple(start_pos)] = (None, "harddrop") 
    visited_positions = set() 
    
    while queue_of_positions:  # for every harddropped position, rotate it and see if we can reach new positions

        position_array = queue_of_positions.popleft()
        position_array_tuple = tuple(position_array.copy())
        new_pos = position_array.copy()
        if position_array_tuple in visited_positions:
            continue
        visited_positions.add(position_array_tuple)

        board_copy = [row.copy() for row in board]
        if position_array == goal_as_pos_array:
            print(f"goal found!! {position_array}")
            return reconstruct_path(came_from, position_array_tuple)
        if new_pos == goal_as_pos_array:
            print(f"goal found!! {position_array}")
            return reconstruct_path(came_from, position_array_tuple)

        if piece == "I":
            kick_table = SRS_I_piece_kick_table
        else:
            kick_table = SRS_rest_pieces_kick_table

        #=== ROTATIONS ===#      
        for rot_goal in rotations:  # trying to rotate to every possible rotation
       
            if rot_goal == position_array[1]: continue  # no need to try rotate into the same rotation
            if (position_array[1], rot_goal) in [('flat_0','flat_2'), ('flat_2','flat_0'), ('spin_R','spin_L'), ('spin_L','spin_R')]: continue
            rotated_position_array, spin = try_place_piece(board_copy, kick_table, position_array.copy(), rot_goal)
            if rotated_position_array is not None:
                rotated_tuple = tuple(rotated_position_array.copy())
                if  tuple(rotated_position_array) not in visited_positions: 
                    queue_of_positions.append(rotated_position_array.copy())
                    if rotated_tuple not in came_from:
                        came_from[tuple(rotated_position_array.copy())] = (position_array_tuple, f"rotate_{position_array_tuple[1][-1]}_to_{rot_goal[-1]}")
                    
        new_ypos = soft_drop_simulation_returning_ypos(PIECES_index[position_array[0]][position_array[1]], board_copy, position_array[2],position_array[1],position_array[0])
        
        #=== SOFTDROP ===#
        if new_ypos is not None and new_pos != goal_as_pos_array[3]:
            softdrop_pos = position_array.copy()
            softdrop_pos[3] = new_ypos
            softdrop_tuple = tuple(softdrop_pos)
            
            if softdrop_tuple not in visited_positions:
                queue_of_positions.append(softdrop_pos.copy())
                if softdrop_tuple not in came_from:
                    came_from[softdrop_tuple] = (position_array_tuple, f"softdrop_to_y{new_ypos}")
                if softdrop_pos == goal_as_pos_array:
                    print(f"goal found! {softdrop_pos}")
                    return reconstruct_path(came_from, softdrop_tuple)
        #=== SIDEWAYS ===#
        
        new_positions_from_sidewways_movement_arrays = sideways_movement_simulation(board_copy, piece, position_array[1], position_array[2], position_array[3], position_array)
        
        for new_position in new_positions_from_sidewways_movement_arrays:
                
            position_array_new_tuple = tuple(new_position)
            if position_array_new_tuple not in visited_positions:
                queue_of_positions.append(new_position.copy())
            
                if tuple(new_position) not in came_from:  # can replace with sets to remove tihngs liek taht
                    came_from[position_array_new_tuple] = (position_array_tuple, f"sideways_move_to_x{new_position[2]}_y{new_position[3]}")
                
                if new_position == goal_as_pos_array:
                    print(f"goal found! {new_position}")
                    return reconstruct_path(came_from, tuple(new_position))

    return None 

def reconstruct_path(came_from, goal_tuple):
    path = []
    current = goal_tuple
    while current is not None:
        parent,action  = came_from[current]
        path.append((action,list(current)))
        current = parent
    path.reverse()  
    print("here is the path:", path)
    return path