import logging

logging.basicConfig(format='%(levelname)s: %(filename)s: %(lineno)d: %(message)s', level=logging.DEBUG)

def check_holes(board, check_covered=True):
    """
    this is merged fucntion of check holes and check cover,
    returns true when there is a hole which can hav ebigger height than one
    untested, better change that soon!
    """
    # explanation with example:
    # region
    # number of blocks that are covering x number of holes, eg.
    # x - full; o - empty
    # xxo
    # xxo
    # oxx
    # xxo
    # xxo
    # returns 2 for first column and 1 for second one, in a case like:
    # xxo
    # xxo
    # oxx
    # xxo
    # xxx
    # xxo
    # it would return 2 for first column, 1 for one hole in column 3 and 1 for another hole
    #endregion
    sum,count = 0,0
    test_mode = False  # Set to True to enable debug output
    for col in range(10):
        found_solid = False
        for row in range(20):
            if board[row][col] != ' ':
                found_solid = True
            if found_solid:
                if board[row][col] != ' ':
                    count += 1
                if board[row][col] == ' ' and board[row-1][col] != ' ': 
                    sum += count
                    if test_mode:
                        logging.debug(f"Found hole in column {col} at row {row}, sum: {sum} count: {count} \n" )
                if row == 19: 
                    count = 0
    return sum 

def height_difference(board):
    """
    Calculates the maximum height difference between columns and returns heights.
    """
    # idfk why it works,apparently its bad but i will make testcases after realising it
    # i really cannot be bothered to work on it now, im hungry
    height_array = []
    for col in range(10):  
        column_height = 0
        # checks from bottom up, looking for empty space
        for row in range(19,-1,-1):
            if board[row][col] == ' ':
                height_array.append(row+1) # Calculate height from the bottom  
                break
        if len(height_array) == col - 1:    
            height_array.append(0)  # If no blocks found, column is empty
    max_diff = max(height_array) - min(height_array)
    return max_diff, height_array

def uneven_stack_est(height_array):
    """
    Calculates the unevenness of a stack by summing absolute differences between adjacent heights.
    """
    if len(height_array) < 2:
        return 0.0  
    
    uneven_sum = sum(abs(height_array[j] - height_array[j+1]) for j in range(len(height_array) - 1))
    return uneven_sum / (len(height_array) - 1) 

def get_heights(board):
    heights = []
    for col in range(len(board[0])):  
        for row in range(len(board)):  
            if board[row][col] != ' ':
                heights.append(len(board) - row - 1) # 0 index  !!!
                break
        else:  
            heights.append(0)
    return heights
