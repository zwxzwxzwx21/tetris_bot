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
    
