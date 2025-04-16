#called by breuteforcer 

# first bruteforcer calls drop piece which loops for entire board
# while looping it calls can_place which checks if piece can go "1 lower"
# if it can, loop again, if it cant, place the piece using place_piece
# now board is edited with placed piece as we were not working on a copy
def find_drop_height(board, xpos):
    """Znajduje wysokość, na której klocek został umieszczony"""
    for y in range(len(board)-1, -1, -1):
        if board[y][xpos] != ' ':
            return y + 1  # Zwraca pierwsze wolne miejsce nad najwyższym blokiem
    return 0

def can_place(piece, board, row, col):
    """Sprawdza, czy klocek może być umieszczony na danej pozycji."""
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                y, x = row + dy, col + dx
                if y >= len(board) or x < 0 or x >= len(board[0]) or board[y][x] != ' ':
                    return False
    return True

def drop_piece(piece, board, col):
    """Symuluje opadanie klocka i zwraca nową planszę (nie modyfikuje oryginalnej)."""
    board_copy = [row.copy() for row in board]  # Głęboka kopia
    row = 0
    while can_place(piece, board_copy, row + 1, col):
        row += 1
    place_piece(piece, board_copy, row, col)
    return board_copy

def place_piece(piece, board, row, col):
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                board[row + dy][col + dx] = cell
    # print("place piece x pos",col + dx)