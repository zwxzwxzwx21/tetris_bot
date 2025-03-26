#called by breuteforcer 

# first bruteforcer calls drop piece which loops for entire board
# while looping it calls can_place which checks if piece can go "1 lower"
# if it can, loop again, if it cant, place the piece using place_piece
# now board is edited with placed piece as we were not working on a copy

def drop_piece(piece, board, col):
    row = 0
    while can_place(piece, board, row + 1, col):
        row += 1
    place_piece(piece, board, row, col) 

def can_place(piece, board, row, col, debug=False):
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                y, x = row + dy, col + dx
                
                if debug:
                    print(f"Checking: piece[{dy}][{dx}] -> board[{y}][{x}]")
                
                if y >= len(board):
                    if debug: print("Fail: out of board (bottom)")
                    return False
                if x < 0:
                    if debug: print("Fail: out of board (left)")
                    return False
                if x >= len(board[0]):
                    if debug: print("Fail: out of board (right)")
                    return False
                if board[y][x] != ' ':
                    if debug: print(f"Fail: collision with '{board[y][x]}'")
                    return False
    return True

def place_piece(piece, board, row, col):
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                board[row + dy][col + dx] = cell