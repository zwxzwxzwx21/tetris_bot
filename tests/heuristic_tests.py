from gettext import find
import sys
import os
def a(board):
    colHeights = []
    for i in range(10):
        for j in range(20): #go down from the top and break when tile is detected
            if board[j][i] != " ":
                colHeights.append(20-j)
                break
            elif j == 19:
                if board[j][i] != " ":
                    colHeights.append(1)
                else:
                    colHeights.append(0)
    return colHeights
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from board_operations.checking_valid_placements import place_piece
from heuristic import check_holes2, clearedLines, bumpiness, blockade_test, tetrisSlot, aggregate, iDependency, analyze
from utility.pieces_index import PIECES_index

heuristic_test_board = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],  
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ]
a_ = a(heuristic_test_board)
#print(a_)
b =bumpiness(a_)
print("bumpiness: "+str(b))
c = blockade_test(heuristic_test_board)
print("blockade value: " +  str(c))
d = iDependency(a_)
print("i dependency value: " +  str(d))
e = check_holes2(heuristic_test_board)
print("holes value: " +  str(e))
f = tetrisSlot(heuristic_test_board, [row[0] for row in heuristic_test_board])
print("tetris slot value: " +  str(f))
g = aggregate(heuristic_test_board)
print("aggregate height value: " +  str(g))
print("==TESTCASE 2 ==")
heuristic_test_board2 = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ['x','x','x','x','x',' ','x','x','x','x'],
    ]
aa_ = a(heuristic_test_board2)
#print(aa_)
bb =bumpiness(aa_)
print("bumpiness: "+str(bb))
cc = blockade_test(heuristic_test_board2)
print("blockade value: " +  str(cc))
ee = check_holes2(heuristic_test_board2)
print("holes value: " +  str(ee))
ff = tetrisSlot(heuristic_test_board2, [row[0] for row in heuristic_test_board2])
print("tetris slot value: " +  str(ff))
gg = aggregate(heuristic_test_board2)
print("aggregate height value: " +  str(gg))
print("==TESTCASE 3 ==")
heuristic_test_board3 = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ','x',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ','x',' ','x',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ','x',' ','x',' ',' ',' ',' ',' ',' '],
    ['x',' ',' ','x',' ',' ',' ',' ',' ',' '],
    ['x','x','x','x',' ','x',' ','x',' ','x'],
    ]
aaa_ = a(heuristic_test_board3)
#print(aaa_)
bbb =bumpiness(aaa_)
print("bumpiness: "+str(bbb))
ccc = blockade_test(heuristic_test_board3)
print("blockade value: " +  str(ccc))
ddd = iDependency(aaa_)
print("i dependency value: " +  str(ddd))
eee = check_holes2(heuristic_test_board3)
fff = tetrisSlot(heuristic_test_board3, [row[0] for row in heuristic_test_board3])
print("tetris slot value: " +  str(fff))
print("holes value: " +  str(eee))
ggg = aggregate(heuristic_test_board3)
print("aggregate height value: " +  str(ggg))

print("==TESTCASE 4 ==")
heuristic_test_board4 = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    ['x',' ',' ','x',' ',' ',' ',' ',' ',' '],
    ['x','x','x','x','x',' ',' ',' ',' ',' '],
    ['x','x','x','x','x','x',' ','x','x',' '],
    ['x','x','x','x','x','x',' ','x','x','x'],
    ['x','x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x','x','x','x','x'],
    ]
heuristic_test_board5 = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    ['x',' ',' ','x',' ',' ',' ',' ',' ',' '],
    ['x','x','x','x','x','x',' ','x','x',' '],
    ['x','x','x','x','x','x',' ','x','x',' '],
    ['x','x','x','x','x','x',' ','x','x','x'],
    ['x','x','x','x','x','x',' ','x','x','x'],
    ['x','x','x','x','x','x','x','x','x','x'],
    ['x','x','x','x','x','x',' ','x','x','x'],
    ['x','x','x','x','x','x',' ','x','x','x'],
    ]
heuristic_test_board5 = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ','x',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ','x','x',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ','x',' ',' ',' ',' ',' ',' ',' '],
    ]
heuristic_test_board6 = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
    [' ','x','x',' ',' ',' ',' ',' ',' ',' '],
    ['x','x',' ',' ',' ',' ',' ',' ',' ',' '],
    ]
a_ = a(heuristic_test_board4)
#print(a_)
b =bumpiness(a_)
print("bumpiness: "+str(b))
c = blockade_test(heuristic_test_board4)
print("blockade value: " +  str(c))
d = iDependency(a_)
print("i dependency value: " +  str(d))
e = check_holes2(heuristic_test_board4)
print("holes value: " +  str(e))
f = tetrisSlot(heuristic_test_board4, [row[0] for row in heuristic_test_board4])
print("tetris slot value: " +  str(f))
g = aggregate(heuristic_test_board4)
print("aggregate height value: " +  str(g))
h = clearedLines(4)
print("cleared lines value (tetris): " +  str(h))
sum = analyze(heuristic_test_board4,4)
print("total heuristic value: " +  str(sum))
sum2 = analyze(heuristic_test_board3,0)
#print("total heuristic value testcase 3: " +  str(sum2))
sum3 = analyze(heuristic_test_board,0)
#print("total heuristic value testcase 1: " +  str(sum))
sum4 = analyze(heuristic_test_board2,0)
#print("total heuristic value testcase 2: " +  str(sum4))
sum5 = analyze(heuristic_test_board5,0)
print("total heuristic value testcase 5: " +  str(sum5))
sum6 = analyze(heuristic_test_board6,0)
#print("total heuristic value testcase 6: " +  str(sum6))
piece = "I"
rotation = "flat_0"
xpos = 5
ypos = 15
piece_info_array = PIECES_index[piece][rotation] # Example piece info array
#place_piece()
#aggregate_val = analyze_test(heuristic_test_board)
#print("Aggregate Height:", aggregate_val)
#aggregate_val2 = analyze_test(heuristic_test_board2)
#print("Aggregate Height:", aggregate_val2)