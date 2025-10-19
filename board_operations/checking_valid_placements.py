# called by bruteforcer

def find_drop_height(board, xpos):
    """
    Finds the height at which a piece would land if dropped in the given column.
    """
    for y in range(len(board)):  
        if board[y][xpos] != ' ':  
            return y - 1  
    return len(board) - 1 # retuns last index of board, being 19 normally 

def can_place(piece, board, row, col):
    """
    Checks if a piece can be placed at the given position on the board.
    """
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                y, x = row + dy, col + dx
                if y >= len(board) or x < 0 or x >= len(board[0]) or board[y][x] != ' ':
                    return False
    return True

def soft_drop_simulation(piece, board, col):
    """
    Simulates dropping a piece in the given column and returns a new board.
    Does not modify the original board.
    """
    board_copy = [row.copy() for row in board]  # deep copy
    row = 0
    while can_place(piece, board_copy, row + 1, col):
        row += 1
    if row == 0: 
        return None
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
                board[row + dy][col + dx] = cell
