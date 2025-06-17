def print_board(board):
    for row in board:
        print(' '.join(row))
    print()
    
board = [[' ' for _ in range(10)] for _ in range(20)]
# ye it just kinda prints the board