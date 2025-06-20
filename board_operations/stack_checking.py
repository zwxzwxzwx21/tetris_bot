
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
    test_mode = True
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
                        print(f"Found hole in column {col} at row {row}, sum: {sum} count: {count}")
                        print()
                    
                if row == 19: 
                    count = 0
    return sum 

def compare_to_avg(height_array, average):
    """
    Calculates the total offset of column heights from the average height.
    
    Args:
        height_array (list): List of column heights (9 elements).
        average (float): Average height of all columns.
    """
    print(average, "avg height")
    offset = 0
    for height in height_array:
        offset += abs(height - average)  
    print('Total offset:', offset)

def height_difference(board):
    """
    Calculates the maximum height difference between columns and returns heights.
    
    Args:
        board (list): 2D list representing the game board (20 rows x 10 columns).
    
    Returns:
        tuple: (max_height_diff, height_array), where height_array contains heights of all 10 columns.
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

def check_i_dep(height_arr, threshold=2):
    """
    Checks for I-dependencies in a Tetris-like height array (9 columns).
    I-dependency occurs when a column is at least 'threshold' blocks lower than both neighbors,
    making it impossible to place an I-piece vertically without leaving holes.

    Args:
        height_arr (list): List of 9 integers representing column heights.
        threshold (int): Minimum height difference to trigger detection (default: 2).

    Returns:
        bool: True if an I-dependency is found (unsuitable for I-piece placement).
    """
    if len(height_arr) != 9:
        raise ValueError("Height array must have exactly 9 elements")

    # Check left edge (column 0 vs 1)
    if height_arr[1] - height_arr[0] > threshold:
        return True

    # Check right edge (column 8 vs 7)
    if height_arr[7] - height_arr[8] > threshold:
        return True

    # Check middle columns (1-7) for pits
    for col_idx in range(1, 8):
        if (height_arr[col_idx] < height_arr[col_idx - 1] - threshold and 
            height_arr[col_idx] < height_arr[col_idx + 1] - threshold):
            return True

    return False

def uneven_stack_est(height_array):
    """
    Calculates the unevenness of a stack by summing absolute differences between adjacent heights.
    
    Args:
        height_array (list): List of integers representing column heights. Should be from different function
    
    Returns:
        float: Average unevenness per adjacent pair.
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
