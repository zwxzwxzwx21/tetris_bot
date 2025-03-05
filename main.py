import pyautogui
import time
import copy
# board zoom at 95% 

#board = [[ '' for _ in range(10)] for _ in range(20)]
'''board = [
    
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
'''''' pieces '''
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
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    ]
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
sequences = [
    ["T", "T", "L"],  # TTL
    ["T", "T", "J"],  # TTJ
    ["L", "O", "J"],  # LOJ
    ["J", "O", "L"],  # JOL
    ["L", "S", "L"],  # LSL
    ["J", "Z", "J"],   # JZJ
    ["L", "T", "T"],
    ["J", "T", "T"],
    ["L", "S", "L"],
    ["J", "Z", "J"],
    ["O", "I", "O"],
    ["O", "O", "I"],
    ["I", "O", "O"],
    ["T", "S", "L"],
    ["L", "Z", "J"],
    ["L", "L", "O"],
    ["J", "J", "O"],
    ["O", "J", "J"],
    ["O", "L", "L"],
]  

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
                    #print('piece placement makes a hole',row,col)
                    return True
    return False

def check_cover(board):
    # this one doesnt check for holes but if anything is above a hole, goes upwards and if there is anything covering then prints it out
    for row in range(20):
        for col in range(10):
            if board[row][col] == ' ':
                for y in range(row-1,-1,-1):
                    if board[y][col] != ' ':
                        #print(f' cover at line {col}, y = {y}, row = {row}')
                        return True
    return False

def choose_piece():
    import random
    piece_variant =random.randint(0,6)
    #temp function because we dont wanna roll pieces, its just good for bruteforcing pieces, for now i wanna have 2 piece placements bruteforced, can do that rather nicely
    pieces = ['I','O','S','Z','L','J','T']
    return pieces[piece_variant]
    
def bruteforce_placements(board, pieces, current_piece_index=0):
    rotations = {
        'I': ['i_piece_f', 'i_piece_s'],
        'O': ['o_piece'],
        'S': ['s_piece_f', 's_piece_s'],
        'Z': ['z_piece_f', 'z_piece_s'],
        'L': ['l_piece_f', 'l_piece_ccw', 'l_piece_cw', 'l_piece_180'],
        'J': ['j_piece_f', 'j_piece_ccw', 'j_piece_cw', 'j_piece_180'],
        'T': ['t_piece_f', 't_piece_ccw', 't_piece_cw', 't_piece_180']
    }

    column_number = {
        'i_piece_f': 6 + 1 - 4,
        'i_piece_s': 9 + 1 - 4,
        'o_piece': 8 + 1 - 4,
        's_piece_f': 7 + 1 - 4,
        's_piece_s': 8 + 1 - 4,
        'z_piece_f': 7 + 1 - 4,
        'z_piece_s': 8 + 1 - 4,
        'l_piece_180': 7 + 1 - 4,
        'l_piece_ccw': 8 + 1 - 4,
        'l_piece_cw': 8 + 1 - 4,
        'l_piece_f': 7 + 1 - 4,
        'j_piece_180': 7 + 1 - 4,
        'j_piece_ccw': 8 + 1 - 4,
        'j_piece_cw': 8 + 1 - 4,
        'j_piece_f': 7 + 1 - 4,
        't_piece_180': 7 + 1 - 4,
        't_piece_ccw': 8 + 1 - 4,
        't_piece_cw': 8 + 1 - 4,
        't_piece_f': 7 + 1 - 4
    }

    str_to_piece = {
        'i_piece_f': i_piece_f,
        'i_piece_s': i_piece_s,
        'o_piece': o_piece,
        's_piece_f': s_piece_f,
        's_piece_s': s_piece_s,
        'z_piece_f': z_piece_f,
        'z_piece_s': z_piece_s,
        'l_piece_180': l_piece_180,
        'l_piece_ccw': l_piece_ccw,
        'l_piece_cw': l_piece_cw,
        'l_piece_f': l_piece_f,
        'j_piece_180': j_piece_180,
        'j_piece_ccw': j_piece_ccw,
        'j_piece_cw': j_piece_cw,
        'j_piece_f': j_piece_f,
        't_piece_180': t_piece_180,
        't_piece_ccw': t_piece_ccw,
        't_piece_cw': t_piece_cw,
        't_piece_f': t_piece_f,
    }

    if current_piece_index >= len(pieces):
        print(f"board after  {len(pieces)} pieces:")
        print_board(board)
        check_heights(board)
        return True  # Znaleziono planszę

    current_piece = pieces[current_piece_index]

    for rotation in rotations[current_piece]:
        for xpos in range(column_number[rotation]):
            board_copy = copy.deepcopy(board)

            drop_piece(str_to_piece[rotation], board_copy, xpos)

            if check_cover(board_copy) != True and check_holes(board_copy) != True:
                a, arr_fo_heights = height_difference(board_copy)
                if 'I' in pieces and a < 6 and uneven_stack_est(arr_fo_heights) < 15 and not (check_i_dep(arr_fo_heights)):
                    if bruteforce_placements(board_copy, pieces, current_piece_index + 1):
                        return True  
                elif 'I' not in pieces and a < 6 and uneven_stack_est(arr_fo_heights) < 15 and not (check_i_dep(arr_fo_heights)):
                    if bruteforce_placements(board_copy, pieces, current_piece_index + 1):
                        return True  

    return False  

def find_best_board(board, pieces):
    
    if bruteforce_placements(board, pieces):
        print("found 6 piece sol.")
        return

   
    if len(pieces) >= 5:
        print("no 6 piece  looking for 5 ...")
        if bruteforce_placements(board, pieces[:5]):
            print("found 5 piece sol.")
            return

    if len(pieces) >= 4:
        print("no 5 piece looking for 4...")
        if bruteforce_placements(board, pieces[:4]):
            print("found 4 piece sol.")
            return

    print("uhoh.")
def check_sequence_with_gaps(pieces, sequence):
    seq_index = 0

    for piece in pieces:
        
        if piece == sequence[seq_index]:
            seq_index += 1 
            if seq_index == len(sequence):
                return True
    return False
def uneven_stack_est(height_array):
    # this one checks how unever stack is in order to remove things with i dependencies, if there is stack like 2,6,2 in heights, we dont want that so we compare how much it varies
    # hwo it works, compare 1,2 2,3 3,4 4,5 5,6 and see the diff, sum it all up and if its quite big, fuck you ig
    uneven_sum = 0
    for j in range(5):
            a = height_array[j] - height_array[j+1]
            uneven_sum += abs(a)
    #print("uneven height by: ", uneven_sum)
    return uneven_sum

def check_i_dep(height_arr):
    # checks 1,2,3 2,3,4 3,4,5 4,5,6 for i dependencies, returns true if there is one and breaks to save time
    #print(height_arr," checking i depeidencies with this heights")
    if height_arr[1] - height_arr[0] > 2:
        return True
    if height_arr[4] - height_arr[5] > 2:
        return True
    for j in range(1, 5):  
        if height_arr[j] < height_arr[j-1] - 2 and height_arr[j] < height_arr[j+1] - 2:
            return True  
    return False

def check_sequences_with_gaps(pieces, sequences):

    found_sequences = []
    
    for sequence in sequences:
        if check_sequence_with_gaps(pieces, sequence):
            found_sequences.append(sequence)
    
    return found_sequences
        
def compare_to_avg(height_array,average):
    print(average, "avg height")
    offset = 0
    for height in height_array:
        offset_ = height - average
        if offset_ < 0:
            offset_ *= -1
        offset += offset_
    print('offset ', offset)

def check_heights(board):
    #this function checks how  flat the board is by taking average of every column and comparing it to each column, if its close 
    # to every single column then stack is clean, otherwise it wont be 
    
    minos_array = []
    for stack in range(6):
        minos_in_line = 0
        for y in range(20):
            
            if board[y][stack] != ' ':
                minos_in_line += 1
        #print(minos_in_line, 'minos on line', stack)
        minos_array.append(minos_in_line)
    sum_height = 0
    for height in minos_array:
        sum_height += height
    average_height = sum_height/6
    compare_to_avg(minos_array,average_height)

def height_difference(board):
    # this one just returns what is the height difference
    arr = [] # it just holds values from 1-6colums heights
    for stack in range(6):
        minos_in_line = 0
        for y in range(20):
            
            if board[y][stack] != ' ':
                minos_in_line += 1
        arr.append(minos_in_line)

    #print(f"height diff: {max(arr) - min(arr)}")
    return (max(arr) - min(arr)),arr

def remove_box_from_q(queue, box):

    #print(queue,box)
    for piece_b in box[0]:
        if piece_b in queue:
            queue.remove(piece_b)
    return queue

import timeit
import time

def measure_execution_time():
    start_time = time.perf_counter() 
    if __name__ == "__main__":
        board1 = copy.deepcopy(board)
        #piece = ['O','T','I','O','S','Z'] # random queue
        piece = ['O','T','J','L','T','O']
        found_sequences = check_sequences_with_gaps(piece, sequences)
        if found_sequences:
            print(found_sequences[-1])  # !! use that to access first sequence
            new_queue = remove_box_from_q(piece,found_sequences) # q without pieces in box as those would be used to make a box (wow)
            print(new_queue, "remaining pieces to build stack on the left")
            bruteforce_placements(board,new_queue,0)
        else:
            bruteforce_placements(board,piece,0)
    end_time = time.perf_counter()  
    execution_time = end_time - start_time  

    print(f"runtime: {execution_time:.6f} s")  
measure_execution_time()


#idea:
#mearuse up how high the stack is on both of the sides and try to match the left side with the side of the boxes on the right
# another important thing is to have a system that ill judge the flatness of a stack and immediately pic k one which is "good enough"

# todo:
# make functionality so you can parse q and play indefinitely 
# make line clears 
# scoring system to judge pieces instead of bruteforcing them to save time
# perfect clear mode/ solver
# make so it resets when early z/s piece

