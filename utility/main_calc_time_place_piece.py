def time_to_place_piece(piece, array_of_piece_times, time_to_calc_piece, time_to_calc_piece_piecenumber):
    if piece == "O":
        array_of_piece_times[0] += time_to_calc_piece
        time_to_calc_piece_piecenumber[0] += 1
        return array_of_piece_times, time_to_calc_piece_piecenumber
    elif piece == "I":
        array_of_piece_times[1] += time_to_calc_piece
        time_to_calc_piece_piecenumber[1] += 1
        return array_of_piece_times, time_to_calc_piece_piecenumber
    elif piece == "J":
        array_of_piece_times[2] += time_to_calc_piece
        time_to_calc_piece_piecenumber[2] += 1
        return array_of_piece_times, time_to_calc_piece_piecenumber
    elif piece == "L":
        array_of_piece_times[3] += time_to_calc_piece
        time_to_calc_piece_piecenumber[3] += 1
        return array_of_piece_times, time_to_calc_piece_piecenumber
    elif piece == "S":
        array_of_piece_times[4] += time_to_calc_piece
        time_to_calc_piece_piecenumber[4] += 1
        return array_of_piece_times, time_to_calc_piece_piecenumber
    elif piece == "Z":
        array_of_piece_times[5] += time_to_calc_piece
        time_to_calc_piece_piecenumber[5] += 1
        return array_of_piece_times, time_to_calc_piece_piecenumber
    elif piece == "T":
        array_of_piece_times[6] += time_to_calc_piece
        time_to_calc_piece_piecenumber[6] += 1
        return array_of_piece_times, time_to_calc_piece_piecenumber

