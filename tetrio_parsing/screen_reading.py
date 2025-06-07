# this function is entirely for tetrio screen reading which will become
# complretely redundant once i got the access to API
# hence why i am commenting it out 
'''import pyautogui
from math import sqrt

PIECE_COLORS = {
    "I": [(65, 175, 222), (63, 221, 255)],
    "O": [(247, 211, 62), (255, 255, 59)],
    "S": [(102, 198, 92), (116, 255, 102)],
    "Z": [(239, 98, 77), (255, 111, 80)],
    "L": [(239, 149, 53), (255, 184, 46)],
    "J": [(25, 131, 191), (5, 158, 244)],
    "T": [(180, 81, 172), (229, 86, 217)],
    "A": [(0, 0, 0), (0, 0, 0)]
    
}
failed_atts = 0
def color_distance(c1, c2):
    """Oblicza odległość między kolorami w przestrzeni RGB"""
    return sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)

def find_closest_piece(pixel, xpos, ypos, failed_atts):
    print('finding for color pixel: ', pixel, " xpos: ", xpos, " ypos: ", ypos)
    
    if not pixel:  
        return "?"
    
    closest_piece = "?"
    min_distance = float('inf')
    
    for piece, colors in PIECE_COLORS.items():
        for color in colors:
            dist = color_distance(pixel, color)
            if dist < min_distance:
                min_distance = dist
                closest_piece = piece
    
    print("closest piece now: ", closest_piece)
    
    if closest_piece == 'A':
        failed_atts += 1
        if failed_atts >= 10:  
            print("Too many failed attempts, returning '?'")
            return "?"
        import time
        time.sleep(0.2)
        new_pixel = pyautogui.pixel(xpos, ypos + failed_atts)
        return find_closest_piece(new_pixel, xpos, ypos + failed_atts, failed_atts)  # Zwróć wynik rekurencji!
    
    return closest_piece

def read_queue():
    y_positions = [384, 517, 645, 778, 906]
    queue = []
    
    for y in y_positions:
        
            pixel = pyautogui.pixel(1654, y)
            queue.append(find_closest_piece(pixel,1654,y,failed_atts))
        
    
    
            current_piece = find_closest_piece(pyautogui.pixel(1258, 192),1258,192,failed_atts)
    
    
    return [current_piece] + queue[:4]  # current + 4 następne

def get_next_piece():
    """Pobiera dodatkowy klocek z kolejki"""
    
    return find_closest_piece(pyautogui.pixel(1654, 906),1654,906,failed_atts)
    

# Przykład użycia
if __name__ == "__main__":
    queue = read_queue()
    queue.append(get_next_piece())
    print("Aktualna kolejka:", queue)'''