# all the functions that directly manipulate the board 
# this file deserve a namechange

from utility.pieces_index import PIECES_index


def clear_lines(board):
    """
    Removes all full lines from the board and adds empty lines at the top.
    """
    new_board = []
    lines_cleared = 0

    for row in board:
        if all(cell != ' ' for cell in row):
            lines_cleared += 1
        else:
            new_board.append(row)

    # adds empty rows at the top for cleared lines
    for _ in range(lines_cleared):
        new_board.insert(0, [' ' for _ in range(10)])
    # doesn't have to return lines_cleared, it does so to count quads and other clears
    return new_board, lines_cleared

def solidify_piece(board, piece,piece_pos_array):
    """
    Places a piece on the board at the specified position.
    """
    new_board = [row.copy() for row in board]
    print(piece_pos_array)
    for (dx, dy) in PIECES_index[piece][piece_pos_array[1]]:
        
        if 0 <= dx+piece_pos_array[2] < 10 and 0 <= dy+piece_pos_array[3] < 20:
            new_board[dy+piece_pos_array[3]][dx+piece_pos_array[2]] = piece
    return new_board