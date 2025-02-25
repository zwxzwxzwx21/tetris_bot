import pyautogui
import time
import copy
# board zoom at 95% 

#board = [[ '' for _ in range(10)] for _ in range(20)]
board = [
    
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ','x',' ',' ','x'],
    ['x',' ',' ','x',' ','x','x',' ',' ','x'],
    ['x','x','x','x','x','x','x','x','x','x'],
    ]
''' pieces '''
#region
# f - flat
# cw - clockwise
# ccw- counter clockwise
# 180 - yeha
# s - side (for pieces like i, s, z)

# O piece
o_piece = [
    ['O', 'O'],
    ['O', 'O']
]
# I piece
i_piece_s = [
    ['I'],
    ['I'],
    ['I'],
    ['I']
]

i_piece_f = [
    ['I', 'I', 'I', 'I']
]
# T piece
t_piece_f = [
    ['T', 'T', 'T'],
    [' ', 'T', ' ']
]

t_piece_180 = [
    [' ', 'T', ' '],
    ['T', 'T', 'T']
]

t_piece_cw = [
    ['T', ' '],
    ['T', 'T'],
    ['T', ' ']
]

t_piece_ccw = [
    [' ', 'T'],
    ['T', 'T'],
    [' ', 'T']
]
# L piece
l_piece_f = [
    [' ', ' ', 'L'],
    ['L', 'L', 'L']
]

l_piece_180 = [
    ['L', 'L', 'L'],
    ['L', ' ', ' ']
]

l_piece_cw = [
    ['L', ' '],
    ['L', ' '],
    ['L', 'L']
]

l_piece_ccw = [
    ['L', 'L'],
    [' ', 'L'],
    [' ', 'L']
]
# J piece
j_piece_f = [
    ['J', ' ', ' '],
    ['J', 'J', 'J']
]

j_piece_180 = [
    ['J', 'J', 'J'],
    [' ', ' ', 'J']
]

j_piece_cw = [
    ['J', 'J'],
    ['J', ' '],
    ['J', ' ']
]

j_piece_ccw = [
    [' ', 'J'],
    [' ', 'J'],
    ['J', 'J']
]
# S piece
s_piece_f = [
    [' ', 'S', 'S'],
    ['S', 'S', ' ']
]

s_piece_s = [
    ['S', ' '],
    ['S', 'S'],
    [' ', 'S']
]
# Z piece
z_piece_f = [
    ['Z', 'Z', ' '],
    [' ', 'Z', 'Z']
]

z_piece_s = [
    [' ', 'Z'],
    ['Z', 'Z'],
    ['Z', ' ']
]
#endregion
'''
# pieces:
# j - (25, 131, 191) poss moves: 8+8+9+9 (34)
# l - (239, 149, 53) 8+8+9+9 (34)
# z - (239, 98, 77) 8+9 (16)
# s - (102, 198, 92) 8+9 (16)
# o - (247, 211, 62) 9  
# t - (180, 81, 172) same as l/j (34)
# i - (65, 175, 222) 10+7 (17)'''

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()
    
def read_queue():
    p1,p2,p3,p4,p5 = '','','','','' # pieces
    '''#used 1258 192
    # 1st 1654 382  + 130
    # 2nd 1654 512  + 136
    # 3rd 1654 648  + 137
    # 4th 1654 785  + 134
    # 5th 1654 919'''
    pieces = {
        (65, 175, 222) : "I",
        (247, 211, 62) : "O",
        (102, 198, 92) : "S",
        (239, 98, 77) : "Z",
        (239, 149, 53) : "L",
        (25, 131, 191) : "J",
        (180, 81, 172) : "T",
        #used piece is highlited so this list is for that piece only
        (63, 221, 255) : "I",
        (5, 158, 244) : "J",
        (255, 111, 80) : "Z",
        (255, 184, 46) : "L",
        (116, 255, 102) : "S",
        (229, 86, 217) : "T",
        (255, 255, 59) : "O"
    }
    '''for piece in range(5):
        print(pyautogui.pixel(1654,382+piece*134))
        if (pyautogui.pixel(1654,382+piece*134) in pieces):
            if piece == 0 :
                p1 = pieces[pyautogui.pixel(1654,382+piece*134)]
            if piece == 1 :
                p2 = pieces[pyautogui.pixel(1654,382+piece*134)]
            if piece == 2 :
                p3 = pieces[pyautogui.pixel(1654,382+piece*134)]
            if piece == 3 :
                p4 = pieces[pyautogui.pixel(1654,382+piece*134)]
            if piece == 4 :
                p5 = pieces[pyautogui.pixel(1654,382+piece*134)]
        print(p1,p2,p3,p4,p5)'''
    y_pos = [382, 512, 648, 785, 919]

    queue = [pieces.get(pyautogui.pixel(1654,y), '') for y in y_pos]

    p1, p2, p3, p4, p5 = queue

    for i, (y,piece), in enumerate(zip(y_pos,queue),start=1):
        print(f"{i}. Pos: (1654, {y}) -> {pyautogui.pixel(1654, y)} => '{piece}'")

    print("Queue:", p1, p2, p3, p4, p5)    
    p_use = pieces[pyautogui.pixel(1258, 192)]
    return p_use, queue

def move_pieces(queue):
    pass 
# this function will work like this that you pass q as argument and make p2 -> p1, p3 -> p2 etc, can do with p2,p3 = p1,p2
def check_pos():
    while True:
        x,y = pyautogui.position()
        print(x,y,pyautogui.pixel(x,y)) 
        time.sleep(0.2)
def make_placements(board,pieces):
    pass

def can_place(piece,board,row,col):
    for dy,piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                y, x = row + dy, col + dx
                if y >= len(board) or x < 0 or x >= len(board[0]) or board[y][x] != ' ':
                    return False
    return True


def place_piece(piece, board, row, col):
    for dy, piece_row in enumerate(piece):
        for dx, cell in enumerate(piece_row):
            if cell != ' ':
                board[row + dy][col + dx] = cell

def drop_piece(piece, board, col):
    row = 0
    while can_place(piece, board, row + 1, col):
        row += 1
    place_piece(piece, board, row, col)  

def check_holes(board):
    #pass
    #todo, somehow figure out a way to check for holes on sides, because it wont be chceking with current loop and ifs
    for row in range(20):
        for col in range(10):
            if board[row][col] == ' ':  
                pieces_around = 0
                available_neighbors = 0

                for x_row in range(-1, 2):
                    for y_col in range(-1, 2):
                        if not (x_row == 0 and y_col == 0): 
                            new_row, new_col = row + x_row, col + y_col

                            # Sprawdzanie granic planszy
                            if 0 <= new_row < 20 and 0 <= new_col < 10:
                                available_neighbors += 1
                                if board[new_row][new_col] != ' ':
                                    pieces_around += 1
                if pieces_around == available_neighbors:
                    print('piece placement makes a hole',row,col)
                    return True
    return False



def check_cover(board):
    # this one doesnt check for holes but if anything is above a hole, goes upwards and if there is anything covering then prints it out
    for row in range(20):
        for col in range(10):
            if board[row][col] == ' ':
                for y in range(row-1,-1,-1):
                    if board[y][col] != ' ':
                        print(f' cover at line {col}, y = {y}, row = {row}')
                        return True
    return False

def choose_piece():
    import random
    piece_variant =random.randint(0,6)
    #temp function because we dont wanna roll pieces, its just good for bruteforcing pieces, for now i wanna have 2 piece placements bruteforced, can do that rather nicely
    pieces = ['I','O','S','Z','L','J','T']
    return pieces[piece_variant]
    
def bruteforce_placements(board,piece):
    rotations = {
        'I': ['i_piece_f','i_piece_s'],
        'O': ['o_piece'],
        'S': ['s_piece_f','s_piece_s'],
        'Z': ['z_piece_f','z_piece_s'],
        'L': ['l_piece_180','l_piece_ccw','l_piece_cw','l_piece_f'],
        'J': ['j_piece_180','j_piece_ccw','j_piece_cw','j_piece_f'],
        'T': ['t_piece_180','t_piece_ccw','t_piece_cw','t_piece_f']
    }
    # this one is keeping track of colums you move from  0 to X, where x needs to change because some pieces are longer than others
    column_number = {
        'i_piece_f': 6,
        'i_piece_s': 9,
        'o_piece': 8,
        's_piece_f' : 7,
        's_piece_s' : 8,
        'z_piece_f' : 7,
        'z_piece_s' : 8,
        'l_piece_180' : 7,
        'l_piece_ccw' : 8,
        'l_piece_cw' : 8,
        'l_piece_f' : 7,
        'j_piece_180' : 7,
        'j_piece_ccw' : 8,
        'j_piece_cw' : 8,
        'j_piece_f' : 7,
        't_piece_180' : 7,
        't_piece_ccw' : 8,
        't_piece_cw' : 8,
        't_piece_f' : 7
    }
    str_to_piece =  {
        'i_piece_f' : i_piece_f,
        'i_piece_s' : i_piece_s,
        'o_piece' : o_piece,
        's_piece_f': s_piece_f,
        's_piece_s' :s_piece_s,
        'z_piece_f' :z_piece_f,
        'z_piece_s' :z_piece_s,
        'l_piece_180': l_piece_180,
        'l_piece_ccw' :l_piece_ccw,
        'l_piece_cw' :l_piece_cw,
        'l_piece_f':l_piece_f,
        'j_piece_180': j_piece_180,
        'j_piece_ccw' :j_piece_ccw,
        'j_piece_cw' :j_piece_cw,
        'j_piece_f' :j_piece_f,
        't_piece_180': t_piece_180,
        't_piece_ccw': t_piece_ccw,
        't_piece_cw' :t_piece_cw,
        't_piece_f': t_piece_f,
    }
    for rotation in rotations[piece]:
        for xpos in range(column_number[rotation]):
            board_copy = copy.deepcopy(board)
            drop_piece(str_to_piece[rotation],board_copy,xpos)
            if check_cover(board_copy) != True and check_holes(board_copy) != True:
                print_board(board_copy)


if __name__ == "__main__":
    #check_pos()
    for i in range(1):
        board1 = copy.deepcopy(board)
        #drop_piece(s_piece_s,board1,col=i)
        #print_board(board1)
        #check_holes(board1)
        #check_cover(board)
        piece = choose_piece()
        print(f"chosen piece is {piece}")
        bruteforce_placements(board1,piece)
        
        
        
    #use_piece, queue = read_queue()
    
    #print(use_piece)

    #q_bruteforce = [use_piece] # queue which we will bruteforce on board, used as arg for function so its more flexible, can use 1 to  6 pieces
    
    #make_placements(board,q_bruteforce)
    #print(board)
    