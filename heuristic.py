import random
from matplotlib.pylab import rand


def aggregate(board):
    #value to minimize
    aggregateHeight = 0
    for i in range(10):
        for j in range(20):
            if board[j][i] != " ":
                #find first non empty tile in the board and apply non-linear scaling
                aggregateHeight += (20 - j)
                break
                
    return aggregateHeight/10

def clearedLines(clearedLines):
     
    match clearedLines:
        case 4:
            clearedLines *= 10 #tetris gucci af
        case 3:
            clearedLines *= -0.75 #triple are horrible value
        case 2:
            clearedLines *= 1.5 #doubles are ok
        case 1:
            clearedLines *= 1 #singles are ok cause im fast
            
    return clearedLines

def bumpiness(colHeights):
    bumpiness = 0

    prevH = colHeights[1]
    for h in range(0, len(colHeights)): #get difference between adjacent columns
        bumpiness += abs(prevH - colHeights[h])
        prevH = colHeights[h]
        
    return bumpiness
    
def blockade(columns):
    blockade = 0

    for i in range(10):
        firstEmpty = 0
        for j in range(19, -1, -1):
            if columns[i][j] == " ":
                firstEmpty = j
                break
        
        for j in range(20):
            if columns[i][j] != " ":
                blockade += firstEmpty - j
                break

    return blockade * 1.2
def blockade_test(columns):
    blockade = 0
    # often at - values, we want to minimize this val, so dont *-1 it
    for i in range(10):
        firstEmpty = 0
        for j in range(19, -1, -1):
            if columns[j][i] == " ":
                firstEmpty = j
                break
        
        for j in range(20):
            if columns[j][i] != " ":
                blockade += firstEmpty - j
                break

    return blockade * 1.2
def tetrisSlot(board, well):
    blocking = 0
    for i in range(20):
        lineCleared = " " not in board[i]
        if (well[i] != "I" and well[i] != " ") or well[i] == "I" and not lineCleared:
            blocking += 1

    return blocking

def check_holes2(board):
    holes = 0
    for x in range(10):
        y = 1
        while y < 20 and board[y][x] == " ":
            y += 1
        y += 1
        while y < 20:
            if board[y][x] == " ":
                holes += 1
            y += 1
    return holes

def iDependency(colHeights):
    iDep = 0

    for i in range(2, 8):
        c, l, r = colHeights[i], colHeights[i-1], colHeights[i+1] #heights of current and adjacent columns
        if l - c >= 3 and r - c >= 3:
            iDep += 1
            
    if colHeights[-2] - colHeights[-1] >= 3:
        iDep += 1
    if colHeights[2] - colHeights[1] >= 3:
        iDep += 1

    return iDep 
weights = [
-2.030 ,   # aggregate
-0.760 ,   # increase tetris score after mvp
-0.420 ,   # bumpiness
-6.474 ,  # blockade
1.942 ,   # tetris well
2.420 ,# i piece dependencies
-5  # holes
]
print("Weights used in this run:",weights)
def analyze(board,cleared_lines):


    #weights = [-0.8452081857581533, -2.166070991373233, -0.9969115616865911, -5.828298433516476, -7.643093990636554, -0.2550496908381308]

    a, b, c, d, e, f,g = weights

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

    columns = []
    for i in range(10):
        columns.append([row[i] for row in board])

    varA = aggregate(board)
    #this is literally -> high stack = bad, no matter how bad it really is 
    # i think its okay to not put much weight into it, so low numbers are good because we will have more space for pieces, 
    varB = clearedLines(cleared_lines) 
    # DOESNT WORK AS INTENDED, VALUE DOENST RESET TO 0
    
    # this one returns from 0.75 to 10
    # often just doesnt do anything because the board has to have cleared lines for this to work
    # i dont see this one as being usefull, but it basically can replace attack, so having this high may work,we wanna max it out, but maybe punish triples?
    # (could stop punishing triples when we have deeper search and we can have multiple outcomes at once)
    
    varC = bumpiness(colHeights)
    # positive = worse, problem is that it overshadows everythign else, and it considers bad stacks good, as long as they are low
    # my idea is to treat it more as weight limit and not as something that should have high value, idk tho
    # so maybe /10 it?
    
    varD = blockade(columns)
    # often at negative values, we want to minimize this val, so dont *-1 it
    # because bad stacks give lets say +5, good vals give -X 
    
    varE = tetrisSlot(board, columns[0])
    # very similar to idependency, tho usually higher, so like not all idep are tetrisslots, plus it sums up the same well plenty of times
    
    
    varF = iDependency(colHeights)  # works good 
    # problem: returns val of I dependencies, so it gives like 1,2 at best, so  it hold no weight
    
    varG = check_holes2(board)
    # returns every hole as positive value, so we wanna minimize it, each EMPTY SPACE is counter as DIFFERENT HOLE
    # without any additional algorithms or addition, just one " " = 1 hole, so this number also yeals rather low values
    
    # === summary ===
    # - aggregate: we want this low
    # - clearedLines: we want this high
    # - bumpiness: we want this low, goes into negatives
    # - blockade: we want this low, goes into negatives
    # - tetrisSlot: we want this high ?
    # - iDependency: we want this low
    # - holes: we want this low
    
    #print(f"aggregate: {varA}, clearedLines: {varB}, bumpiness: {varC}, blockade: {varD}, tetrisSlot: {varE}, iDependency: {varF}")
    varB = 0
    #print(a*varA + b*varB + c*varC + d*varD + e*varE + f*varF)
    return -varA*1.7 + varB - varC*2.5 - varD*2.5 + varE - varF - varG*10

def analyze_main(board,cleared_lines):
    # this one is for the board view printing


    #weights = [-0.8452081857581533, -2.166070991373233, -0.9969115616865911, -5.828298433516476, -7.643093990636554, -0.2550496908381308]

    a, b, c, d, e, f, g = weights

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

    columns = []
    for i in range(10):
        columns.append([row[i] for row in board])

    varA = aggregate(board)
    varB = cleared_lines
    varC = bumpiness(colHeights)
    varD = blockade(columns)
    varE = tetrisSlot(board, columns[0])
    varF = iDependency(colHeights)
    varG = check_holes2(board)
    return a*varA, b*varB, c*varC, d*varD, e*varE, f*varF,g*varG

def analyze_test(board):
    # this one is for the board view printing
    weights = [
    -2.030,   # aggregate
    -0.760,   # increase tetris score after mvp
    0.420,   # bumpiness
    -6.474,  # blockade
    1.942,   # tetris well
    2.420    # i piece dependencies
    ]

    #weights = [-0.8452081857581533, -2.166070991373233, -0.9969115616865911, -5.828298433516476, -7.643093990636554, -0.2550496908381308]

    a, b, c, d, e, f = weights

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

    columns = []
    for i in range(10):
        columns.append([row[i] for row in board])

    varA = aggregate(board)
    varB = check_holes2(board)
    varC = bumpiness(colHeights)
    varD = blockade(columns)
    varE = tetrisSlot(board, columns[0])
    varF = iDependency(colHeights)
    print(f"aggregate: {varA*a}, bumpiness: {varC*c}, blockade: {varD*d}, tetrisSlot: {varE*e}, iDependency: {varF*f}")
    