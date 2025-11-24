def print_board(board, compressed_mode=False, pro_mode=True):
    print("===PRINTING BOARD===")
    if not pro_mode:
        for row in board:
            if any(cell != ' ' for cell in row) or not compressed_mode:
                print(' '.join(row))
    elif pro_mode:
        color_dict = {
            ' ': '\033[0m.',
            '.': '\033[0m.',
            'I': '\033[96m█',
            'O': '\033[93m█',
            'T': '\033[95m█',
            'S': '\033[92m█',
            'Z': '\033[91m█',
            'J': '\033[94m█',
            'L': '\033[38;5;208m█',
        }
        print("   ", end='')
        for x in range(1,11):
            print(f" {x}", end='')
        print()   
        print("   ", end='')
        print("█" * 21)
        y = 0
        
        for row in board:
            y += 1
            if any(cell != ' ' for cell in row) or not compressed_mode:
                print(f"{y:2d} \033[0m█\033[0m", end='')
                print('\033[0m█'.join(color_dict[cell] for cell in row) + '█\033[0m')
                print("   " + "█" * 21)
    print()

board = [[' ' for _ in range(10)] for _ in range(20)]