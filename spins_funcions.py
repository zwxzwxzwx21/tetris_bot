def change_rotations(rotation):
    # to be fair im not really sure if we need that function or if it would be better to rename things from the get go
    # i dont wanna fuck around changing variables now so this is the only reason why i made that
    rotation_map_no_180 = {
        "0": "0",
        "cw": "R",
        "180": "2",
        "ccw": "L",
    }
    rotation_map_T_180 = {
        "0": "N",
        "cw": "E",
        "180": "S",
        "ccw": "W",
    }
    if rotation in rotation_map_no_180:
        return rotation_map_no_180[rotation]
    elif rotation in rotation_map_T_180:
        return rotation_map_T_180[rotation]
from board_operations.checking_valid_placements import place_piece    
from utility.pieces import PIECES
from spins import SRS_I_piece_kick_table,SRS_rest_pieces_kick_table,SRS_Tpiece_180_kick_table
from utility.print_board import print_board

def try_place_piece(board,kick_table,info_array,rotation_goal):
    """this function tries to place a piece by using a spin, if it fails, it tries puttinga  kick offset on it
    when fails completely,returns none"""
    # rotation goal is either left right or 180, determines what offset to set 
    # this one makes the data sets like work, because you need same data twice which is different for some reason lol, i should fix it at some point
    str_piece_rotation_goal = 'spin_'+rotation_goal if info_array[1] in ['flat_0','flat_180'] else 'flat_'+rotation_goal # change it to table
    rotated_piece = PIECES[info_array[0]][str_piece_rotation_goal]
    print(rotated_piece)
    print(str_piece_rotation_goal)
    for offset in kick_table[info_array[1][-1]+'-'+rotation_goal]:
        print(info_array[1][-1]+'-'+rotation_goal)
        print(kick_table[info_array[1][-1]+'-'+rotation_goal])
        print(offset,info_array[2] + int(offset[0]), info_array[3] + int(offset[1]))
        board_,result = place_piece(rotated_piece,board,info_array[3] + int(offset[1]),info_array[2] + int(offset[0]))
        print("result:",result)
        if result:
            # returning board makes no sense, ill return position array instead
            print_board(board_)
            print([info_array[0],str_piece_rotation_goal,info_array[2] + int(offset[0]), info_array[3] + int(offset[1])])

            return [info_array[0],str_piece_rotation_goal,info_array[2] + int(offset[0]), info_array[3] + int(offset[1])]
            #distinguishing spins would be easier than just making sure they work so spins dont do mpre than normal clears
            #print_board(board_)
            #return board_ # now continue on heuristic from this point

    return None 
def simulate_kicks(board,piece,rotation,x_pos,y_pos,piece_info_array):
    # piece info array example ("T",'flat_0',x(fore xample 4),y(for example 15))
    possible_positions_array = []
    # clockwise/counter clockwise
    if piece != "I":
        kick_table = SRS_rest_pieces_kick_table
    elif piece == "I":
        kick_table = SRS_I_piece_kick_table
    rotation_goal = None
    # here would we just cycle trhough rotation goals like R,2,L 
    # if they can be placed, go on, if no, try next one
    result = try_place_piece(board,kick_table,piece_info_array,rotation_goal)
    if result is not None:
        possible_positions_array.append(result)
        # add all possible potitions and put them through heuristic
    # IMPORTANT: there is a srs L/J kick i dont really have any data on as it seems to be tetrio thing, it uses 180 and can make a L/J piece be kicked using 180 spin  which is the only piece that can be kicked like that except T piece  
    # 180
    if piece == 'T':
        kick_table = SRS_Tpiece_180_kick_table 
        if piece_info_array[1] == "flat_0":
            rotation_goal = "flat_180"
        elif piece_info_array[1] == "flat_180":
            rotation_goal = "flat_0"
        elif piece_info_array[1] == "spin_R":
            rotation_goal = "spin_L"
        elif piece_info_array[1] == "spin_L":
            rotation_goal = "spin_R"
        result = try_place_piece(board,kick_table,piece_info_array,rotation_goal)
        if result is not None:
            possible_positions_array.append(result)
    # if one position after softdrop unlocks every x pos (for example with a flat board)
    # you can use formula 10- width of block, and if in one for loop, 10-width entries were added
    # into piece_info_array, that means that we have a flat board and we DO NOT need to go through
    # every single x position, just that one on the same y level
    
    return possible_positions_array

