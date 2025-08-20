# all the functions that directly manipulate the board 
# this file deserve a namechange

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
