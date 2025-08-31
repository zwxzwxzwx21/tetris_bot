# called by bruteforcer

def find_drop_height(board, xpos):
    """
    Finds the height at which a piece would land if dropped in the given column.
    """
    for y in range(20):  ##### HARDCODED
        if board[xpos][y] != ' ':  
            return y - 1  
    return 20 - 1 # retuns last index of board, being 19 normally        ##### HARDCODED

def can_place(piece, board, row, col):
    """
    Checks if a piece can be placed at the given position on the board.
    """
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                x, y = col + dx, row + dy
                if y >= 20 or x < 0 or x >= 10 or board[x][y] != ' ':    ##### HARDCODED
                    return False
    return True

def drop_piece(piece, board, col):
    """
    Simulates dropping a piece in the given column and returns a new board.
    Does not modify the original board.
    """
    import copy
    board_copy = copy.deepcopy(board)  
    row = 0
    while can_place(piece, board_copy, row + 1, col):
        row += 1
    place_piece(piece, board_copy, row, col)
    return board_copy

def place_piece(piece, board, row, col):
    """
    Places a piece on the board at the specified position.
    Modifies the board in-place.
    """
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                board[col + dx][row + dy] = cell
