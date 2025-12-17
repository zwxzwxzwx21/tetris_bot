from gettext import find
import sys
import os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board_operations.board_operations import clear_lines
from board_operations.checking_valid_placements import place_piece
from search_for_best_move import search_for_best_move
from board_operations.stack_checking import find_highest_y
from bruteforcing import find_best_placement
from utility.pieces_index import PIECES_index
from utility.pieces import PIECES
from utility.print_board import print_board
tspin_double_testcase = [
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
    ['x','x','x','x','x','x','x',' ',' ','x'],
    ['x','x','x','x','x','x',' ',' ',' ','x'],
    ['x','x','x','x','x','x','x',' ','x','x'],
    ]

tspin_triple_testcase = [
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
    [' ',' ',' ','x',' ',' ',' ',' ',' ',' '], 
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    ['x','x','x',' ','x','x','x','x','x','x'],
    ['x','x','x',' ',' ','x','x','x','x','x'],
    ['x','x','x',' ','x','x','x','x','x','x'],
    ]
sspin_triple_testcase = [
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
    [' ',' ',' ',' ',' ','x',' ',' ',' ',' '],
    ['x','x','x',' ','x','x','x','x','x','x'],
    ['x','x','x',' ',' ','x','x','x','x','x'],
    ['x','x','x','x',' ','x','x','x','x','x'],
    ]
clean_lines_testcase = [
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
    ['x','x','x','x','x','x','x','x','x','x'],
    ['x','x','x',' ','x','x','x','x','x','x'],
    ['x','x','x',' ','x','x','x','x','x','x'],
    ['x','x','x',' ','x','x','x','x','x','x'],
    ]
o_testcase = [
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
    ['x',' ','x','x','x','x',' ','x','x','x'],
    [' ',' ','x',' ',' ','x',' ',' ',' ',' '],
    [' ',' ','x',' ',' ','x',' ',' ',' ','x'],
    ]
queue = ['S'] #  vro is alonje :sob: 
from spins import SRS_rest_pieces_kick_table, SRS_I_piece_kick_table
#find_best_placement(tspin_double_testcase,queue,0,{}) 
#test = search_for_best_move("S_x4_spin_L",sspin_triple_testcase,18)
from heuristic import clearedLines
a = clearedLines(clean_lines_testcase)
print(a)
b,c = clear_lines(clean_lines_testcase) 
print(c)
#test = search_for_best_move("T_x7_flat_2",tspin_double_testcase,18)
#test = search_for_best_move("T_x3_spin_R",tspin_triple_testcase,18)
from spins_funcions import try_place_piece_with_kick
#test,a = try_place_piece(tspin_triple_testcase,SRS_rest_pieces_kick_table, ['T','flat_0',4,16],'spin_R')
#place_piece_test = place_piece(PIECES_index["T"]['spin_R'],test[0],tspin_triple_testcase,test[2],test[3],test[1] )
#print_board(place_piece_test[0])
from board_operations.checking_valid_placements import can_place, find_lowest_y_for_piece, place_piece, sideways_movement_simulation, get_piece_height, get_piece_lowest_index_from_origin, get_piece_width, get_piece_leftmost_index_from_origin,get_piece_rightmost_index_from_origin
#place_piece_test = place_piece(PIECES_index["T"]['spin_R'],"T",tspin_triple_testcase,3,18,"spin_R" )
#print("place piece test result:\n",place_piece_test)
#test = sideways_movement_simulation(tspin_triple_testcase,'T','flat_0',6,16,[['T','flat_0',6,16]])
#print("sideways movement simulation test result:",test)
import time
time.sleep(2)
#arr = sideways_movement_simulation(tspin_triple_testcase,'I','spin_0',7,12,[['T','flat_0',4,15]]) # this seems to be off by one for some reason, id fix that later
#print(arr)

from spins import SRS_rest_pieces_kick_table, SRS_I_piece_kick_table
from spins_funcions import try_place_piece_with_kick
#print(PIECES["I"]['flat_0'])
#x,y = 2,2
#brd,a = place_piece(PIECES_index["I"]['flat_0'],"I",tspin_triple_testcase,x,y )
##print_board(brd)


a=  try_place_piece_with_kick(tspin_triple_testcase,SRS_rest_pieces_kick_table, ['T','flat_0',4,16],'spin_L')
print(a)
'''place_piece_test = place_piece(PIECES_index["T"]['flat_0'],"T",tspin_triple_testcase,4,16,"flat_0" )
print(place_piece_test)
print_board(place_piece_test[0])
place_piece_test2 = place_piece(PIECES_index["T"]['spin_R'],"T",tspin_triple_testcase,3,18,"spin_R" )
print(place_piece_test2)
print_board(place_piece_test2[0])
'''#from bruteforcing import find_best_placement
#find_best_placement(tspin_triple_testcase,queue,0,{})
def testprint(piece,rotation):
    board = [[' ' for _ in range(6)] for _ in range(6)]
    for pos in PIECES_index[piece][rotation]:
        print(pos)
        board[pos[1]+2][2+pos[0]] = piece
    print_board(board)
#z = find_lowest_y_for_piece(tspin_double_testcase)
#print(z)
#a = can_place(PIECES_index["T"]['flat_0'],tspin_double_testcase,11,1)
#print(a)
'''
b = place_piece(PIECES_index["T"]['flat_0'],tspin_double_testcase,5,5)
print(b)'''
rotation = 'spin_L'
piece = 'T'
width = get_piece_width(PIECES_index[piece][rotation])
height = get_piece_height(PIECES_index[piece][rotation])
lowest = get_piece_lowest_index_from_origin(PIECES_index[piece][rotation])
leftmost = get_piece_leftmost_index_from_origin(PIECES_index[piece][rotation])
rightmost = get_piece_rightmost_index_from_origin(PIECES_index[piece][rotation])
print(f"width:{width} height:{height} lowest:{lowest} leftmost:{leftmost} rightmost:{rightmost}")