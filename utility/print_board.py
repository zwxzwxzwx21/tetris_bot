def print_board(board,compressed_mode=False):
    # todo when bored, can use rich library and change function to print_board(color= T/F)to have colored output
    print("===PRINTING BOARD===") # no logging cuz i think it sobv for now that its from this file 
    for row in board:
        if any(cell != ' ' for cell in row) or not compressed_mode:
            print(' '.join(row))
    print()
    
board = [[' ' for _ in range(10)] for _ in range(20)]
# ye it just kinda prints the board