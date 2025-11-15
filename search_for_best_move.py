from board_operations.checking_valid_placements import find_lowest_y_for_piece, sideways_movement_simulation, soft_drop_simulation, place_piece, soft_drop_simulation_returning_ypos
from spins import SRS_rest_pieces_kick_table, SRS_I_piece_kick_table
from utility.print_board import print_board
from utility.pieces_index import PIECES_index, PIECES_startpos_indexing_value, PIECES_xpos_indexing_value
from spins_funcions import simulate_kicks, try_place_piece
import time
from collections import deque
PRINT_MODE = False
def search_for_best_move(goal, board, best_move_y_pos):
    import time
    # i tihnk the best way to approach it, is to work on a board and do: board  == goal_board
    '''this function would search for the best move to reach goal on board, goal is string like 'T_x4_flat_0'
    would return move history to reach that goal'''
    
    goal_parts = goal.split('_')  # ['T','x4','flat','0']
    piece = goal_parts[0]
    x_pos = int(goal_parts[1][1:])
    rotation = goal_parts[2] + '_' + goal_parts[3]  # flat_0
    y_pos = best_move_y_pos
    came_from = {}
    goal_as_pos_array = [piece, rotation, x_pos, y_pos]
    #print(f"piece : {piece}, x_pos: {x_pos}, rotation: {rotation}, y_pos: {y_pos}")

    rotations = ["flat_0", "spin_R", "flat_2", "spin_L"]
    queue_of_positions = deque()  # this array is like: if we have an X position and we rotate it, if the new position is already in the array, we skip it, otherwise we could have infinite loops
    
    # piece info array example ("T",'flat_0',x(fore xample 4),y(for example 15))
    # idea for 180 spins: just replace indexes of X spin into the 180 variant of that one for exaple if you have spin_l s_piece with some indexes, just take indexes from spin_r s_piece, that should work just fine
    for rot in rotations:
        #print(f"checking rotation: {rot}")
        
        for dx in range(PIECES_startpos_indexing_value[piece][rot], 11 - PIECES_xpos_indexing_value[piece][rot]):
            lowest_Y = find_lowest_y_for_piece(PIECES_index[piece][rot], board, dx, rot, piece=piece)
            # print("lowest y ",lowest_Y)
            start_pos = [piece, rot, dx, lowest_Y]
            queue_of_positions.append(start_pos )  # apprends all the places available without tucking or spins/kicks
            came_from[tuple(start_pos)] = (None, "harddrop")  # lub inny etykietujący tekst
    visited_positions = set()  # to avoid processing the same position multiple times
    
    #print("already cheked possition array: ", "len:", len(queue_of_positions), queue_of_positions)
    
    while queue_of_positions:  # for every harddropped position, rotate it and see if we can reach new positions
        #came_from[tuple([piece, rot, dx, lowest_Y])] = (None, "harddrop")
        position_array = queue_of_positions.popleft()
        position_array_tuple = tuple(position_array.copy())
        new_pos = position_array.copy()
        if position_array_tuple in visited_positions:
            continue
        visited_positions.add(position_array_tuple)
        #a = set(queue_of_positions[0])
        #b = set(visited_positions)
        #c = a.difference(b)
        #print(c)
        applied_kicks_counter = 3
        board_copy = [row.copy() for row in board]
        #print(position_array,  goal_as_pos_array)
        #print("checking position array:", visited_positions)
        if position_array == goal_as_pos_array:
            print(f"goal found!! {position_array}")
            return reconstruct_path(came_from, position_array_tuple)
        if new_pos == goal_as_pos_array:
            print(f"goal found!! {position_array}")
            return reconstruct_path(came_from, position_array_tuple)
        #print("copying board for position array:", position_array)
        # print_board(board_copy)
        # time.sleep(0.5)
        #print("selecting kick table")
        # time.sleep(0.5)
        if piece == "I":
            kick_table = SRS_I_piece_kick_table
        else:
            kick_table = SRS_rest_pieces_kick_table

        while applied_kicks_counter > 0:
            for rot_goal in rotations:  # trying to rotate to every possible rotation
               
                # time.sleep(0.5)
                new_ypos = None

                if rot_goal != position_array[1]:  # rotation isnt the same as current one
                    if position_array[1] == 'flat_0' and rot_goal == 'flat_2':
                        continue  # skipping 180 spins for now
                    if position_array[1] == 'flat_2' and rot_goal == 'flat_0':
                        continue  # skipping 180 spins for now
                    if position_array[1] == 'spin_R' and rot_goal == 'spin_L':
                        continue  # skipping 180 spins for now
                    if position_array[1] == 'spin_L' and rot_goal == 'spin_R':
                        continue  # skipping 180 spins for now
                    #print(f"trying to rotate piece {piece} from {position_array[1]} to {rot_goal} at x:{position_array[2]} y:{position_array[3]}")
                else:
                    continue  # rotation is the same as current one, no need to try it

                #arg_position_array = position_array.copy()
                #print("position before rotation attempt:", position_array)
                if position_array == ['T', 'flat_0', 4, 16]:   
                    print("a")     
                    time.sleep(21)

                print("rot goal" ,rot_goal)
                position_array, spin = try_place_piece(board_copy, kick_table, position_array.copy(), rot_goal)
                print("result after try place piece:", position_array, spin)

                print(goal_as_pos_array)
                #print("position after rotation attempt:", position_array)

                if position_array is not None and tuple(position_array) not in visited_positions:
                    if position_array == ['T', 'spin_R', 3, 18]:
                        print("test")
                    queue_of_positions.append(position_array.copy())
                    came_from[tuple(position_array.copy())] = (position_array_tuple, f"rotate_{position_array_tuple[1][-1]}_to_{rot_goal[-1]}")
                    '''if position_array == goal_as_pos_array:
                        print(f"goal found! {position_array}")
                        
                        return reconstruct_path(came_from, tuple(position_array))'''
                #if position_array is None:  # failed to place with kicks/ checking for softdrops
                    new_ypos = soft_drop_simulation_returning_ypos(PIECES_index[position_array[0]][position_array[1]], board_copy, position_array[2],position_array[1],position_array[0])
                '''if new_ypos is None: # piece is completely stuck
                    continue''' 
                position_index_softdrop_copy = position_array.copy()
                if new_ypos is not None:
                    position_index_softdrop_copy[3] = new_ypos
                position_index_softdrop_tuple = tuple(position_index_softdrop_copy)
                if position_index_softdrop_tuple not in visited_positions:
                    queue_of_positions.append(position_index_softdrop_copy)
                    came_from[position_index_softdrop_tuple] = (position_array_tuple, f"softdrop_to_y{new_ypos}")
                if new_ypos != position_array[3] and new_ypos is not None:  # softdrop is possible
                    #arg_position_array_softdrop = position_array.copy()
                    softdrop_copy = position_array.copy()
                    softdrop_copy[3] = new_ypos
                    softdrop_tuple = tuple(softdrop_copy)
                    if softdrop_tuple not in visited_positions:
                        queue_of_positions.append(softdrop_copy)
                        if softdrop_tuple not in came_from:
                            came_from[softdrop_tuple] = (position_array_tuple, f"softdrop_to_y{new_ypos}")
                    
                        if softdrop_copy == goal_as_pos_array:
                            print(f"goal found! {softdrop_copy}")
                            return reconstruct_path(came_from, softdrop_tuple)
                    '''if position_array == goal_as_pos_array:
                        print(position_array)
                        time.sleep(1)
                        print(f"goal found! {position_array}")
                        return reconstruct_path(came_from, tuple(position_array))'''
                    #print(f"after soft drop new ypos is {new_ypos}")
                print(position_array)
                new_positions_from_sidewways_movement_arrays = sideways_movement_simulation(board_copy, piece, position_array[1], position_array[2], position_array[3], position_array)
                for new_position in new_positions_from_sidewways_movement_arrays:
                    #if len(new_positions_from_sidewways_movement_arrays) > 0:
                        
                    position_array_new_tuple = tuple(new_position)
                    if position_array_new_tuple not in visited_positions:
                        queue_of_positions.append(new_position.copy())
                    
                    if tuple(new_position) not in visited_positions:  # can replace with sets to remove tihngs liek taht
                        came_from[position_array_new_tuple] = (position_array_tuple, f"sideways_move_to_x{new_position[2]}_y{new_position[3]}")
                        
                    if new_position == goal_as_pos_array:
                        print(f"goal found! {new_position}")
                        return reconstruct_path(came_from, tuple(new_position))
                        '''if new_position == goal_as_pos_array:
                            print(f"goal found! {position_array}")
                            
                            return reconstruct_path(came_from, tuple(position_array))'''
                        #print(new_position, " is not in ", sequence_of_moves, " adding it now")

                # can fail in abscard cases when the piece is moved 3 times without kicking (soft drop and X movements only)
                #print(f"was spin successful: {spin}")
                '''if spin == False:
                    applied_kicks_counter -= 1
                    if applied_kicks_counter < 0:
                        break
                elif spin == True:
                    applied_kicks_counter = 3'''

                applied_kicks_counter -= 1
                # print(applied_kicks_counter," kicks left| ",len(sequence_of_moves)," positions found so far, sequence of moves ", sequence_of_moves)

        

    # checking new positions using kicks
    # im feeling like omitting tucking pieces for now to save on calculations, can add it later

    return None #reconstruct_path(came_from, tuple(position_array))


# try to compare new positions with already discovered ones because you can achieve infinite loops with certain setups, so if you add them to soem sort of array and cmapre, it should stop after one loop


def reconstruct_path(came_from, goal_tuple):
    print("paus")
    time.sleep(1.5)
    path = []
    current = goal_tuple
    while current is not None:
        parent,action  = came_from[current]
        path.append((action,list(current)))
        current = parent
    path.reverse()  
    print("here is the path:", path)
    time.sleep(989)
    return path