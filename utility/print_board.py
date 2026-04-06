def print_board(board, compressed_mode=False, color=False, coords=True):
    print("===PRINTING BOARD===")
    if not color and not coords:
        for row in board:
            if any(cell != ' ' for cell in row) or not compressed_mode:
                print(' '.join(row))
    elif color:
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
    elif coords:
        print(" ", end='')
        for x in range(1,11):
            print(f" {x}", end='')
        print()
        y = 0
        for row in board:
            y += 1
            if any(cell != ' ' for cell in row) or not compressed_mode:
                print(f"{y:2d} " + ' '.join(row))
    print()   

board = [[' ' for _ in range(10)] for _ in range(20)]


def printred(s):
    print("\033[91m" + s + "\033[0m")

def printgreen(s):
    print("\033[92m" + s + "\033[0m")

def printyellow(s):
    print("\033[93m" + s + "\033[0m")
    
import config    
def debug_print(*args, print_mode=config.PRINT_MODE, color=None, filename_line: str = "", **kwargs):
    if print_mode:
        if color == 'red':
            printred(*args, filename_line=filename_line, **kwargs)
        elif color == 'green':
            printgreen(*args, filename_line=filename_line, **kwargs)
        elif color == 'yellow':
            printyellow(*args, filename_line=filename_line, **kwargs)
        else:
            print(*args, filename_line=filename_line,**kwargs)