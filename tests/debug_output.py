import numpy as np
board = np.full((10, 20), "o")
#print(board)


import copy
board_copy = copy.deepcopy(board)  
print(board_copy)
'''row = 0
while can_place(piece, board_copy, row + 1, col):
    row += 1
place_piece(piece, board_copy, row, col)'''
   