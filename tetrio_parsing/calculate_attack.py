'''def check_lines_clear(board):
    for row in board:
        if all(cell != ' ' for cell in row):
            return True
    return False'''

ATTACK_TABLE = {
    "single": [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3],
    "double": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
    "triple": [2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11],
    "tetris": [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
}

ATTACK_TABLE_MAX_COMBO = { # for combo above 19
    "single": 3,
    "double": 6,
    "triple": 12,
    "tetris": 24
}

PERFECT_CLEAR_BONUS = 10

def attack_simplified(clear, combo):
    
    atk = 0
    
    if clear == "perfect clear":
        # that wont work really, make sth like, check if board is empty, if it is, add 10 attack
        return PERFECT_CLEAR_BONUS

    if combo >= len(ATTACK_TABLE["single"]): 
        atk = ATTACK_TABLE_MAX_COMBO.get(clear, 0)
    else:
        attack_list = ATTACK_TABLE.get(clear, [])
        if attack_list: 
            atk = attack_list[combo]

    return atk


def count_lines_clear(lines_cleared_count,combo,board):
    
    
    attack = 0
    perfect_clear = True
    for row in board:
        if all(cell == ' ' for cell in row):
            perfect_clear = False
            break

    if perfect_clear:
        print("Perfect clear!")
        attack += PERFECT_CLEAR_BONUS
        
    if combo < 20:
        if lines_cleared_count == 1:
            attack += ATTACK_TABLE["single"][combo]
            print("Single cleared") 
        elif lines_cleared_count == 2:    
            attack += ATTACK_TABLE["double"][combo]
            print("Double cleared")
        elif lines_cleared_count == 3:    
            attack += ATTACK_TABLE["triple"][combo]
            print("Triple cleared")
        elif lines_cleared_count == 4:
            attack += ATTACK_TABLE["tetris"][combo]
            print("Tetris cleared") 
    else:
        if lines_cleared_count == 1:
            attack += ATTACK_TABLE_MAX_COMBO["single"]
            print("Single cleared") 
        elif lines_cleared_count == 2:    
            attack += ATTACK_TABLE_MAX_COMBO["double"]
            print("Double cleared")
        elif lines_cleared_count == 3:    
            attack += ATTACK_TABLE_MAX_COMBO["triple"]
            print("Triple cleared")
        elif lines_cleared_count == 4:
            attack += ATTACK_TABLE_MAX_COMBO["tetris"]
            print("Tetris cleared") 
    if lines_cleared_count > 0:
        combo += 1
    else:
        combo = 0        
    print(f"Attack: {attack}, Combo: {combo}")
    
    return attack, combo
