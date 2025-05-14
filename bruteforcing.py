import copy
from utility.print_board import print_board
from utility.pieces import * # importing piece lookuptable
from board_operations.stack_checking import compare_to_avg, check_heights, check_holes, check_i_dep, uneven_stack_est, height_difference,get_heights
from board_operations.checking_valid_placements import drop_piece,place_piece,can_place
from tetrio_parsing.movement import move_piece
import time 

# this bruteforcer makes no sense baah,
# here is how new one might work better, fuck efficiency, just hoow it will work
# first of all, combination like S/Z/O means unlucky = restart, cant have anything  clean with Z/S as first pieces, and second too when you have O/Z/S next

# create a function to be like, how clean is the stack for other pieces like: can you put O piece in there? can you put horizontal I piece in stack, would vertical i piece fuck the stack up
# same to rest pieces l,j,s,z,t  

# split bruteforcer and evaluations so bruteforcer returns  board piece and position (mby im missing sth) and it parses it to another function/file
#


debug = True
rotations = {
    'I': ['flat', 'spin'],
    'O': ['flat'],
    'S': ['flat', 'spin'],
    'Z': ['flat', 'spin'],
    'L': ['flat', '180', 'cw', 'ccw'],
    'J': ['flat', '180', 'cw', 'ccw'],
    'T': ['flat', '180', 'cw', 'ccw']
}

column_ranges  = {
        'i_flat': 6  ,
        'i_spin': 9  ,

        'o_flat': 8  ,

        's_flat': 7  ,
        's_spin': 8  ,

        'z_flat': 7  ,
        'z_spin': 8  ,

        'l_180': 7  ,
        'l_ccw': 8  ,
        'l_cw': 8  ,
        'l_flat': 7  ,

        'j_180': 7 ,
        'j_ccw': 8  ,
        'j_cw': 8  ,
        'j_flat': 7  ,

        't_180': 7  ,
        't_ccw': 8  ,
        't_cw': 8  ,
        't_flat': 7  
    }
import time

TIME_LIMIT = 0.1 
UNEVEN_THRESHOLD = 1.1
MAX_HEIGHT_DIFF = 11

def find_best_placement(board, queue):
   
    global start_time
    start_time = time.perf_counter()
    best_board = None
    best_score = float('inf')
    best_move = None
    perfect_clear_found = False

    def evaluate(board, is_potential_pc=False):
        height_diff, heights = height_difference(board)
        uneven = uneven_stack_est(heights)
        score = height_diff * uneven
        
        if is_potential_pc:
            score -= 10000
        return score

    def recursive_search(board, queue, current_piece_index, move_history):
        nonlocal best_board, best_score, best_move, perfect_clear_found

        if time.perf_counter() - start_time > TIME_LIMIT:
            return

        if current_piece_index >= len(queue):
          
            best_board = board    
            best_move = move_history[0]
            return
            

        current_piece = queue[current_piece_index]
        for rotation_name, piece_shape in PIECES[current_piece].items():
            max_x = 10 - len(piece_shape[0])
            for x in range(max_x + 1):
                new_board = drop_piece(piece_shape, copy.deepcopy(board), x)
                if new_board is None:
                    continue

                height_diff, heights = height_difference(new_board)
                uneven = uneven_stack_est(heights)
                if (uneven > UNEVEN_THRESHOLD or 
                    height_diff > MAX_HEIGHT_DIFF or 
                    check_holes(new_board)):
                    continue

                move = f"{current_piece}_x{x}_{rotation_name}"
                recursive_search(
                    new_board,
                    queue,
                    current_piece_index + 1,
                    [*move_history, move] if current_piece_index == 0 else move_history
                )

    recursive_search(board, queue, 0, [])
    return best_board, best_move


def clear_lines(board):
    
    lines_cleared = 0
    
    rows_to_clear = []
    for row in range(len(board)):
        if all(cell != ' ' for cell in board[row]):
            rows_to_clear.append(row)
            lines_cleared += 1
    
    for row in rows_to_clear:
        board[row] = [' ' for _ in range(10)]
    
    if lines_cleared > 0:
        apply_gravity(board)
    
    return board

def apply_gravity(board):
    
    for col in range(10):
        
        blocks = []
        for row in range(len(board)):
            if board[row][col] != ' ':
                blocks.append(board[row][col])
        
        for row in range(len(board)-1, -1, -1):
            if blocks:
                board[row][col] = blocks.pop()
            else:
                board[row][col] = ' '

board = [[' ' for _ in range(10)] for _ in range(20)]
from tetrio_parsing.screen_reading import get_next_piece, read_queue
from GenerateBag import create_bag, add_piece_from_bag
from BoardRealTimeView import TetrisBoardViewer
import time
import threading

# Initialize empty board
board = [[0 for _ in range(10)] for _ in range(20)]
queue = create_bag()
bag = create_bag()

# Create viewer window
viewer = TetrisBoardViewer(board)

def game_loop():
    while True:
        global board, queue, bag
        print("\n=== Current Queue ===")
        print(queue)
        
        best_board, best_move = find_best_placement(board, queue)
        
        if not best_board:
            print("No valid placement found")
            break
        
        piece_type, x, rotation = best_move.split('_')
        x = int(x[1:])
        piece_shape = PIECES[piece_type][rotation]
        new_board = drop_piece(piece_shape, board, x)
        
        new_board = clear_lines(new_board)
       
        board[:] = new_board  
        viewer.update_board(board)
        print(f"\nPlaced: {piece_type} at x={x}, rotation={rotation}")
       
        print_board(board)
        queue, bag = add_piece_from_bag(queue, bag)
        queue.pop(0)
        

game_thread = threading.Thread(target=game_loop, daemon=True)
game_thread.start()


viewer.mainloop()