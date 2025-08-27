import logging

logging.basicConfig(
    format="%(levelname)s: %(filename)s: %(lineno)d: %(message)s", level=logging.DEBUG
)


def hole_exists(board, x, y):
    assert 0 <= x <= 9
    assert 0 <= y <= 19

    return (y == 0 or board[y - 1][x] != " ") and board[y][x] == " "


def check_holes(board):
    total = 0

    for y in range(1, 20):
        total += sum(hole_exists(board, x, y) for x in range(10))
    return total


def height_difference(board):
    """
    Calculates the maximum height difference between columns and returns heights.
    """
    # idfk why it works,apparently its bad but i will make testcases after realising it
    # i really cannot be bothered to work on it now, im hungry
    height_array = []
    for col in range(10):
        # checks from bottom up, looking for empty space
        for row in range(19, -1, -1):
            if board[row][col] == " ":
                height_array.append(row + 1)  # Calculate height from the bottom
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

    uneven_sum = sum(
        abs(height_array[j] - height_array[j + 1]) for j in range(len(height_array) - 1)
    )
    return uneven_sum / (len(height_array) - 1)


def get_heights(board):
    heights = []
    for col in range(len(board[0])):
        for row in range(len(board)):
            if board[row][col] != " ":
                heights.append(len(board) - row)
                break
        else:
            heights.append(0)
    return heights
