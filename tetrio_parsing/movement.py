# exact same as screen_reading, useless, thus commented out
'''import keyboard
import time
import pyautogui
 
hd = 'b'
ccw = 'c'
cw = 'v'
x = 'x'
l = 'i'
r = 'p'
stall = True
delay = 0.02
def move_piece(piece,pos,rotation):
    # have to do it in wanky way as sometimes you go rotation > movement and sometimes movement > rotation
    pos = pos + 1 # change from 0 index for clarity
    print(pos)
    if piece == 'O':
        if rotation == 'flat':
            # here we dont have any finesse, so we immediately call move function
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 4:
                press_button(l)
            if pos == 6:
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 9:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            press_button(hd)
    if piece == 'I':
            
            if rotation == 'flat':
                if pos == 1:
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                if pos == 2:
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                if pos == 3:
                    press_button(l)
                if pos == 5:
                    press_button(r)
                if pos == 6:
                    press_button(r)
                    if stall:
                        time.sleep(delay)
                    press_button(r)
                if pos == 7:
                    press_button(r)
                    if stall:
                        time.sleep(delay)
                    press_button(r)
                    if stall:
                        time.sleep(delay)
                    press_button(r)
            elif rotation == 'spin':
                if pos == 1:
                    rotate(cw)
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                if pos == 2:
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                    rotate(cw)
                if pos == 3:
                    press_button(l)
                    if stall:
                        time.sleep(delay)
                    press_button(l)
                    rotate(cw)
                if pos == 4:
                    rotate(ccw)
                    press_button(l)
                if pos == 5:
                    rotate(ccw)
                if pos == 6:
                    rotate(cw)
                if pos == 7:
                    rotate(cw)
                    press_button(r)
                if pos == 8:
                    press_button(r)
                    if stall:
                        time.sleep(delay)
                    press_button(r)
                    rotate(cw)
                if pos == 9:
                    press_button(r)
                    if stall:
                        time.sleep(delay)
                    press_button(r)
                    if stall:
                        time.sleep(delay)
                    press_button(r)
                    rotate(cw)
                if pos == 10:
                    rotate(cw)
                    simulate_das(r)
                    if stall:
                        time.sleep(delay)
                    press_button(r)
                    if stall:
                        time.sleep(delay)
                    press_button(r)
                    if stall:
                        time.sleep(delay)
                    press_button(r)
            press_button(hd)
                
            # i will work on more later as im not sure about pos of rotated pieces
    if piece == 'T':
        if rotation == 'flat':
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
        elif rotation == 'cw':
            press_button(cw)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 4:
                press_button(l)
            if pos == 6:
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 9:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
        elif rotation == 'ccw':
            press_button(ccw)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 9:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)  
                if stall:
                    time.sleep(delay)
                press_button(r)   
        elif rotation == '180':
            press_button(x)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
        press_button(hd)
    if piece == 'J':
        if rotation == 'flat':
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
        elif rotation == 'cw':
            press_button(cw)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 4:
                press_button(l)
            if pos == 6:
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 9:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
        elif rotation == 'ccw':
            press_button(ccw)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 9:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r) 
                if stall:
                    time.sleep(delay) 
                press_button(r)   
        elif rotation == '180':
            press_button(x)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:

                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)  
        press_button(hd)
    if piece == 'L':
        if rotation == 'flat':
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
        elif rotation == 'cw':
            press_button(cw)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 4:
                press_button(l)
            if pos == 6:
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 9:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
        elif rotation == 'ccw':
            press_button(ccw)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 9:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)  
                if stall:
                    time.sleep(delay)
                press_button(r)   
        elif rotation == '180':
            press_button(x)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
        press_button(hd)
    if piece == 'S':
        if rotation == 'flat':
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)        
        elif rotation == 'spin':
            press_button(ccw)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 9:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r) 
                if stall:
                    time.sleep(delay) 
                press_button(r)
        press_button(hd)
    if piece == 'Z':
        if rotation == 'flat':
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)        
        elif rotation == 'spin':
            press_button(ccw)
            if pos == 1:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 2:
                press_button(l)
                if stall:
                    time.sleep(delay)
                press_button(l)
            if pos == 3:
                press_button(l)
            if pos == 5:
                press_button(r)
            if pos == 6:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 7:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 8:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
            if pos == 9:
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)
                if stall:
                    time.sleep(delay)
                press_button(r)  
                if stall:
                    time.sleep(delay)
                press_button(r)
        press_button(hd)

def simulate_das(direction, duration=0.1): 
    keyboard.press(direction)
    time.sleep(duration)
    keyboard.release(direction)

def press_button(direction):
    print('simulate button',direction)
    a = ['left','right']
    if direction in a:
        
        pyautogui.press(direction)
        #pyautogui.keyUp(direction)  
    else:
        b = ['b']
        keyboard.press_and_release(direction)
        
def rotate(rot):
    print(rot)
    if rot == 'ccw' or rot == 'c':
        keyboard.press_and_release('c') 
    if rot == 'cw'or rot == 'v':
        keyboard.press_and_release('v')
    if rot == '180' or rot == 'x':
        keyboard.press_and_release('x')
'''