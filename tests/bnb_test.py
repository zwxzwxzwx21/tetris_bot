import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BnB import run_reference_comparison, all_valid_positions

board = [[" " for _ in range(10)] for _ in range(20)]
#queue = ["I", "O", "T", "S", "Z", "J", "L"]
queue = ["J", "L"]


def main():
    held_piece = "L"
    depth = 3

    result = run_reference_comparison(board, queue, held_piece=held_piece, depth=depth)
    print("[bnb_test] depth:", result["depth"])
    print("[bnb_test] visited_nodes:", result["bruteforce"]["visited_nodes"])
    print("[bnb_test] best_score:", result["bruteforce"]["score"])
    print("[bnb_test] first_move:", result["bruteforce"]["first_move"])
    print("[bnb_test] sequence:", result["bruteforce"]["sequence"])


if __name__ == "__main__":    
    all_valid_positions_result = all_valid_positions(queue[0], board, held_piece=None, queue=queue)
    for position in all_valid_positions_result:
        print(position)