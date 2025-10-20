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
    
from spins import * 
def simulate_kicks(board,piece,rotation,x_pos,y_pos,piece_info_array):
    # if one position after softdrop unlocks every x pos (for example with a flat board)
    # you can use formula 10- width of block, and if in one for loop, 10-width entries were added
    # into piece_info_array, that means that we have a flat board and we DO NOT need to go through
    # every single x position, just that one on the same y level
    
    return None


