# SO FAR NOT USED AS MY FILE SPLITTING BAD HEHE

import pyautogui
import time
import copy
# board zoom at 95% 
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
    [' ',' ',' ',' ','x','x','x',' ','x','x'],
    ['x','x','x','x','x','x','x','x','x','x'],
    ]
# keep track of dependencies like I,J,L
# keep track of when a next piece when appear, when you place o piece on empty board, next o piece wont appear in at least 7 pieces!
# ^ might be stupid, no point really
# place pieces with advance of one piece, so when you place one piece you want to know immediately when second one will go
# that lowers the efficiency because you cant change the piece placement if you find a better one, tho i dont think it would be the case as the piece that would have to change inputs is last
#make possibility to delay box patterns, if you have L piece which you just can really place, just move it to the left and wait for 2 pieces filling the box pattern, can do the same but with 2 T pieces

# creating i dependencies is good UNTIL you have i pieces to fill them with, in a run you wont have more than 16-17 I pieces so you need to limit your I piece usage (including dependencies)!

# yeah fuck efficiency for now, i think the best idea, tho extremely inefficient (IT DOESNT MATTER!!):
# take a piece and before making placement think about other pieces, so if you have a q
# think how other pieces would behave when you place one piece, if that piece placement would lead to uneven stack, then you need to  abbandon it
# another good thing would be to keep track of flatness of the board for pieces, if your board is completely flat, you cant place Z/S,
# if its spikey, you cant place O piece, idk how to do that to, fuck my life.

# ig what you can do is run function that checks if stack is viable to place o piece and z,s piece, instead of checking if its even  or not.
# height diff checks seems to be good idea as having stack being uneven just makes shit ton of dependencies which clearing up is nightmare


queue = ['O','J','I','L','S','T'] # ['O','J','I','L','S','T']  First queue # SEED 1 

    #['O','J','I','L','S','T','Z','T','O','L','J','S','I','Z','L','I','S','O','I','T','Z','O','I','T','L','O','Z','S','J','J','O','Z','L','I','T','O']

#queue = ['O','J','I','L','S','T']

# wow it works nice, now what i need to do is to have counter of I pieces to not overshoot



import timeit
import time
from bruteforcing import find_best_placement
from utility.print_board import print_board

def measure_execution_time():
    start_time = time.perf_counter()
    
    # Przekazujemy CAŁĄ kolejkę, nie pojedyncze klocki
    final_board = find_best_placement(board, queue)  # Start od indeksu 0
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    print("\nfinal board state ")
    if final_board is not None:
        pass
        print_board(final_board)
    else:
        print("bruteforced failed to find good placement (rn nothing is good tho as there are no rules)")
    
    print(f"\ntotal runtime {execution_time:.6f} seconds")


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

