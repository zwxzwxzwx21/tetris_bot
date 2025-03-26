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
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    ]
# keep track of dependencies like I,J,L
# keep track of when a next piece when appear, when you place o piece on empty board, next o piece wont appear in at least 7 pieces!
# ^ might be stupid, no point really
# place pieces with advance of one piece, so when you place one piece you want to know immediately when second one will go
# that lowers the efficiency because you cant change the piece placement if you find a better one, tho i dont think it would be the case as the piece that would have to change inputs is last
#make possibility to delay box patterns, if you have L piece which you just can really place, just move it to the left and wait for 2 pieces filling the box pattern, can do the same but with 2 T pieces

# creating i dependencies is good UNTIL you have i pieces to fill them with, in a run you wont have more than 16-17 I pieces so you need to limit your I piece usage (including dependencies)!

queues = [
            ['O','J','I','L','S','T'],  # First queue # SEED 1 
            ['Z','T','O','L','J','S'],  # Second queue
            ['T','Z','J','J','S','L'],   # Third queue
            ['I','T','Z','O','I','T'],   # Third queue
            ['L','O','Z','S','J','J'],   # Third queue
            ['O','Z','L','I','T','O']   # Third queue
        ]
    

queue = ['O','J','I','L','S','T','Z','T','O','L','J','S','I','Z','L','I','S','O','I','T','Z','O','I','T','L','O','Z','S','J','J','O','Z','L','I','T','O']
# wow it works nice, now what i need to do is to have counter of I pieces to not overshoot



import timeit
import time
from bruteforcing import bruteforce_placements
from utility.print_board import print_board

def measure_execution_time():
    start_time = time.perf_counter()
    
    if __name__ == "__main__":
        # Initialize with empty board
        current_board = copy.deepcopy(board)
       
        current_board = bruteforce_placements(current_board, queue, 0)
        print_board(current_board)
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    print("\nFinal board state:")
    print_board(current_board)
    print(f"\nTotal runtime: {execution_time:.6f} seconds")

# Run the modified function
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

