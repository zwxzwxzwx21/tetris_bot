import logging

logging.basicConfig(
    format="%(levelname)s: %(filename)s: %(lineno)d: %(message)s", level=logging.DEBUG
)


def hole_exists(board, x, y):
    assert 0 <= x <= 9
    assert 0 <= y <= 19

    return (y == 0 or board[x][y - 1] != " ") and board[x][y] == " "


def check_holes(board):
    total = 0

    for y in range(1, 20):
        total += sum(hole_exists(board, x, y) for x in range(10))
    return total


def check_holes2(board):
    total = 0
    for x in range(10):
        y = 1
        while y < 20 and board[x][y] == " ":
            y += 1
        y += 1
        while y < 20:
            if board[x][y] == " ":
                total += 1
            y += 1
    return total


def height_difference(board):
    """
    Calculates the maximum height difference between columns and returns heights.
    """
    height_array = []
    for col in range(10):
        for row in range(19, -1, -1):
            if board[col][row] == " ":
                height_array.append(19 - row)
                break
        if len(height_array) == col - 1:
            height_array.append(0)
    max_diff = max(height_array) - min(height_array)
    return max_diff, height_array


def uneven_stack_est(height_array):
    """
    Calculates the unevenness of a stack by summing absolute differences between adjacent heights.
    """
    if len(height_array) < 2:
        return 0.0

    uneven_sum = sum(
        abs(height_array[j] - height_array[j + 1]) for j in range(len(height_array) - 1)
    )
    return uneven_sum / (len(height_array) - 1)


def get_heights(board):
    print('eh oh')
    print(board)
    heights = []
    for col in range(10):                      ##### HARDCODED 
        for row in range(20):                  ##### HARDCODED
            if board[col][row] != " ":
                heights.append(20 - row)
                break
        else:
            heights.append(0)
    return heights
