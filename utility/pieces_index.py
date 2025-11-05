# important thing about this one, I and O pieces are basically made with hope that they work
# they should normally work just fine, however the issue i imagine can happen is for example, 
# first or last index of the board in x axis would be not checked, its really ahrd to tell because most of the things should work just fine, if anything will be off i will adjust any code that doesnt work
# O and I rotation index (or just the main index,) is (1,1) because every other piece rotates around that one too
import sys
import os
from time import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#[0,0][1,0]
#[0,1][1,1] <-- rotation index
#(x,y)
PIECES_index = {
    'O': {
        'flat_0' : [(0,0),(-1,0),(0,-1),(-1,-1)], 
        },

    'I': {
        'flat_0' : [(0,1),(-1,1),(1,1),(2,1)],
        'spin_L' : [(0,0),(0,-1),(0,1),(0,2)],
        'flat_180' : [(0,0),(-1,0),(1,0),(2,0)],
        'spin_R' : [(1,0),(1,-1),(1,1),(1,2)],
        }, 

    'T': {
        'flat_0': [(0,0),(-1,0),(1,0),(0,-1)],
        'flat_180': [(0,0),(-1,0),(1,0),(0,1)],
        'spin_R': [(0,0),(1,0),(0,-1),(0,1)],
        'spin_L': [(0,0),(-1,0),(0,1),(0,-1)]
        },

    'L': {
        'flat_0': [(0,0),(-1,0),(1,0),(1,-1)],
        'flat_180': [(0,0),(1,0),(-1,1),(-1,0)],
        'spin_R': [(0,0),(1,1),(0,1),(0,-1)],
        'spin_L': [(0,0),(-1,-1),(0,-1),(0,1)],  
        },

    'J': {
        'flat_0': [(0,0),(-1,0),(1,0),(-1,-1)],
        'flat_180': [(0,0),(-1,0),(1,0),(1,1)],
        'spin_R': [(0,0),(0,-1),(0,1),(1,-1)],
        'spin_L': [(0,0),(0,-1),(0,1),(-1,1)],  
        },

    'S': {
        'flat_0': [(0,0),(0,-1),(1,-1),(-1,0)],
        'spin_R': [(0,0),(0,-1),(1,0),(1,1)],
        'flat_180': [(0,0),(1,0),(-1,1),(0,1)],
        'spin_L': [(0,0),(-1,-1),(-1,0),(0,1)],
        },

    'Z': {
        'flat_0': [(0,0),(-1,-1),(0,-1),(1,0)],
        'flat_180': [(0,0),(-1,0),(0,1),(1,1)],
        'spin_L': [(0,0),(0,-1),(-1,0),(-1,1)],
        'spin_R': [(0,0),(1,0),(1,-1),(0,1)],
        }
}
PIECES_soft_drop_index = { # pieces without rotations, basically 0
    'O': {
        'flat_0' : [(0,0),(-1,0),(0,-1),(-1,-1)]
    },
    'I': {
        'flat_0' : [(0,1),(-1,1),(1,1),(2,1)],
    },    
    'T': {
        'flat_0': [(0,0),(-1,0),(1,0),(0,-1)],
    },
    'L': {
        'flat_0': [(0,0),(-1,0),(1,0),(1,-1)],
    },
    'J': {
        'flat_0': [(0,0),(-1,0),(1,0),(-1,-1)],
    },
    'S': {
        'flat_0': [(0,0),(0,-1),(1,-1),(-1,0)],
    },
    'Z': {
        'flat_0': [(0,0),(-1,-1),(0,-1),(1,0)],
    }
}

'''from utility.print_board import print_board
def testprint(piece,rotation):
    board = [[' ' for _ in range(6)] for _ in range(6)]
    for pos in PIECES_index[piece][rotation]:
        print(pos)
        board[pos[1]+2][2+pos[0]] = piece
    print_board(board)
testprint("T",'flat_0')
testprint("T",'flat_180')
testprint("T",'spin_R')
testprint("T",'spin_L')'''


# pieces - RGB : (amount of possible placementes)
# j - (25, 131, 191) poss moves: 8+8+9+9 (34)
# l - (239, 149, 53) 8+8+9+9 (34)
# z - (239, 98, 77) 8+9 (16)
# s - (102, 198, 92) 8+9 (16)
# o - (247, 211, 62) 9  
# t - (180, 81, 172) same as l/j (34)
# i - (65, 175, 222) 10+7 (17)