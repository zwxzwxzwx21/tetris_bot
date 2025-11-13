from board_operations.checking_valid_placements import find_lowest_y_for_piece, sideways_movement_simulation, soft_drop_simulation, place_piece, soft_drop_simulation_returning_ypos
from spins import SRS_rest_pieces_kick_table,SRS_I_piece_kick_table
from utility.print_board import print_board
from utility.pieces_index import PIECES_index, PIECES_startpos_indexing_value, PIECES_xpos_indexing_value
from spins_funcions import simulate_kicks, try_place_piece
import time
def search_for_best_move(goal,board,best_move_y_pos):
    import time
    # i tihnk the best way to approach it, is to work on a board and do: board  == goal_board
    '''this function would search for the best move to reach goal on board, goal is string like 'T_x4_flat_0'
    would return move history to reach that goal'''
    
    move_array = [] 
    goal_parts = goal.split('_') # ['T','x4','flat','0']
    
    piece = goal_parts[0]
    x_pos = int(goal_parts[1][1:]) 
    rotation = goal_parts[2] + '_' + goal_parts[3] # flat_0
    y_pos = best_move_y_pos
    goal_as_pos_array = [piece, rotation, x_pos, y_pos]
    print(f"piece : {piece}, x_pos: {x_pos}, rotation: {rotation}, y_pos: {y_pos}")
    sequence_of_moves = []  # array that contains moves that would reach the goal
    rotations = ["flat_0","spin_R","flat_2","spin_L"]
    already_checked_positions = [] # this array is like: if we have an X position and we rotate it, if the new position is already in the array, we skip it, otherwise we could have infinite loops
    # piece info array example ("T",'flat_0',x(fore xample 4),y(for example 15))
    # idea for 180 spins: just replace indexes of X spin into the 180 variant of that one for exaple if you have spin_l s_piece with some indexes, just take indexes from spin_r s_piece, that should work just fine 
    for rot in rotations:
        
        print(f"checking rotation: {rot}")
        #time.sleep(0.5)
        for dx in range(PIECES_startpos_indexing_value[piece][rot],11-PIECES_xpos_indexing_value[piece][rot]):
            lowest_Y = find_lowest_y_for_piece(PIECES_index[piece][rot], board, dx,rot,piece=piece)
            #print("lowest y ",lowest_Y) 
            already_checked_positions.append([piece,rot,dx,lowest_Y]) # apprends all the places available without tucking or spins/kicks
    print("already cheked possition array: ","len:" , len(already_checked_positions), already_checked_positions)        
    for position_array in already_checked_positions: # for every harddropped position, rotate it and see if we can reach new positions
        
        applied_kicks_counter = 3 
        board_copy = [row.copy() for row in board]
        print("copying board for position array:",position_array)
        #print_board(board_copy)
        #time.sleep(0.5)
        print("selecting kick table")
        #time.sleep(0.5)
        if piece == "I":
            kick_table = SRS_I_piece_kick_table
        else:
            kick_table = SRS_rest_pieces_kick_table
        
            
        while applied_kicks_counter > 0:   
                    for rot_goal in rotations: # trying to rotate to every possible rotation
                        print("entering while loop for kicks, kicks left:",applied_kicks_counter)     
                        
                        print(f"kicks left to apply: {applied_kicks_counter}")
                        print("try piece place vals: ", rot_goal, position_array)
                        #time.sleep(0.5)
                        new_ypos = None

                        if rot_goal != position_array[1]: # rotation isnt the same as current one
                            
                            if position_array[1] == 'flat_0' and rot_goal == 'flat_2':
                                print("skipping 180 spin from flat_0 to flat_2")
                                continue # skipping 180 spins for now
                            if position_array[1] == 'flat_2' and rot_goal == 'flat_0':
                                print("skipping 180 spin from flat_2 to flat_0")
                                continue # skipping 180 spins for now
                            if position_array[1] == 'spin_R' and rot_goal == 'spin_L':
                                print("skipping 180 spin from spin_R to spin_L")
                                continue # skipping 180 spins for now
                            if position_array[1] == 'spin_L' and rot_goal == 'spin_R':
                                print("skipping 180 spin from spin_L to spin_R")
                                continue # skipping 180 spins for now
                            print(f"trying to rotate piece {piece} from {position_array[1]} to {rot_goal} at x:{position_array[2]} y:{position_array[3]}")
                        else: continue # rotation is the same as current one, no need to try it
                        position_array, spin = try_place_piece(board_copy,kick_table,position_array,rot_goal) 
                        print("position after rotation attempt:",position_array)   
                        if position_array is not None and position_array not in sequence_of_moves:
                            sequence_of_moves.append(position_array)
                            if position_array == goal_as_pos_array:
                                print(f"goal found! {position_array}")
                                return sequence_of_moves
                        elif position_array is None: # failed to place with kicks/ checking for softdrops
                            new_ypos = soft_drop_simulation_returning_ypos(piece,board_copy,position_array[2],)
                        '''if new_ypos is None: # piece is completely stuck
                            continue'''
                        if new_ypos is not None: # softdrop is possible
                            position_array[3] = new_ypos
                            sequence_of_moves.append(position_array)
                            if position_array == goal_as_pos_array:
                                print(f"goal found! {position_array}")
                                return sequence_of_moves
                            print(f"after soft drop new ypos is {new_ypos}")
                            new_positions_from_y_change_arrays = sideways_movement_simulation(board_copy,piece,position_array[1],position_array[2],new_ypos,position_array)
                            for new_position in new_positions_from_y_change_arrays and new_position not in sequence_of_moves:
                                if new_position not in sequence_of_moves: # can replace with sets to remove tihngs liek taht 
                                    sequence_of_moves.append(new_position)
                                    if position_array == goal_as_pos_array:
                                        print(f"goal found! {position_array}")
                                        return sequence_of_moves
                                    print(new_position, " is not in ", sequence_of_moves," adding it now")
                        # can fail in abscard cases when the piece is moved 3 times without kicking (soft drop and X movements only) 
                        print(f"was spin successful: {spin}")
                        if spin == False: 
                            applied_kicks_counter -= 1 
                            if applied_kicks_counter < 0:
                                break
                        elif spin == True:
                            applied_kicks_counter = 3
                        print(applied_kicks_counter," kicks left| ",len(sequence_of_moves)," positions found so far, sequence of moves ", sequence_of_moves)
                    
    # checking new positions using kicks
    # im feeling like omitting tucking pieces for now to save on calculations, can add it later

    return sequence_of_moves

# try to compare new positions with already discovered ones because you can achieve infinite loops with certain setups, so if you add them to soem sort of array and cmapre, it should stop after one loop