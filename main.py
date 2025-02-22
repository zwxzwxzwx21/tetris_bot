import pyautogui
import time
# board zoom at 95% 

board = [[ '' for _ in range(10)] for _ in range(20)]

'''
# pieces:
# j - (25, 131, 191) poss moves: 8+8+9+9 (34)
# l - (239, 149, 53) 8+8+9+9 (34)
# z - (239, 98, 77) 8+9 (16)
# s - (102, 198, 92) 8+9 (16)
# o - (247, 211, 62) 9  
# t - (180, 81, 172) same as l/j (34)
# i - (65, 175, 222) 10+7 (17)'''

    
def read_queue():
    p1,p2,p3,p4,p5 = '','','','','' # pieces
    '''#used 1258 192
    # 1st 1654 382  + 130
    # 2nd 1654 512  + 136
    # 3rd 1654 648  + 137
    # 4th 1654 785  + 134
    # 5th 1654 919'''
    pieces = {
        (65, 175, 222) : "I",
        (247, 211, 62) : "O",
        (102, 198, 92) : "S",
        (239, 98, 77) : "Z",
        (239, 149, 53) : "L",
        (25, 131, 191) : "J",
        (180, 81, 172) : "T",
        #used piece is highlited so this list is for that piece only
        (63, 221, 255) : "I",
        (5, 158, 244) : "J",
        (255, 111, 80) : "Z",
        (255, 184, 46) : "L",
        (116, 255, 102) : "S",
        (229, 86, 217) : "T",
        (255, 255, 59) : "O"
    }
    '''for piece in range(5):
        print(pyautogui.pixel(1654,382+piece*134))
        if (pyautogui.pixel(1654,382+piece*134) in pieces):
            if piece == 0 :
                p1 = pieces[pyautogui.pixel(1654,382+piece*134)]
            if piece == 1 :
                p2 = pieces[pyautogui.pixel(1654,382+piece*134)]
            if piece == 2 :
                p3 = pieces[pyautogui.pixel(1654,382+piece*134)]
            if piece == 3 :
                p4 = pieces[pyautogui.pixel(1654,382+piece*134)]
            if piece == 4 :
                p5 = pieces[pyautogui.pixel(1654,382+piece*134)]
        print(p1,p2,p3,p4,p5)'''
    y_pos = [382, 512, 648, 785, 919]

    queue = [pieces.get(pyautogui.pixel(1654,y), '') for y in y_pos]

    p1, p2, p3, p4, p5 = queue

    for i, (y,piece), in enumerate(zip(y_pos,queue),start=1):
        print(f"{i}. Pos: (1654, {y}) -> {pyautogui.pixel(1654, y)} => '{piece}'")

    print("Queue:", p1, p2, p3, p4, p5)    
    p_use = pieces[pyautogui.pixel(1258, 192)]
    return p_use, queue

def move_pieves(queue):
    pass 
# this function will work like this that you pass q as argument and make p2 -> p1, p3 -> p2 etc, can do with p2,p3 = p1,p2
def check_pos():
    while True:
        x,y = pyautogui.position()
        print(x,y,pyautogui.pixel(x,y)) 
        time.sleep(0.2)
def make_placements(board,pieces):
    
if __name__ == "__main__":
    #check_pos()
    
    
    use_piece, queue = read_queue()
    
    print(use_piece)

    q_bruteforce = [use_piece] # queue which we will bruteforce on board, used as arg for function so its more flexible, can use 1 to  6 pieces
    
    make_placements(board,q_bruteforce)
    #print(board)
    