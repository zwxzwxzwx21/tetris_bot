def print_board(board):
    # todo when bored, can use rich library and change function to print_board(color= T/F)to have colored output
    print(
        "===PRINTING BOARD==="
    )  # no logging cuz i think it sobv for now that its from this file
    print(*("".join(s for s in row) for row in board.T), sep="\n")


# ye it just kinda prints the board
