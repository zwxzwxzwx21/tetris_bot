def aggregate(board):
    aggregateHeight = 0
    for i in range(10):
        for j in range(20):
            if board[j][i] != " ":
                #find first non empty tile in the board and apply non-linear scaling
                aggregateHeight += (20 - j) ** 2.5
                break
                
    return aggregateHeight/10

def clearedLines(board):
    clearedLines = 0
    for line in board: #cleared line until detects empty tile
        cleared = True
        for tile in line:
            if tile == " ":
                cleared = False
                break
        if cleared:
            clearedLines += 1
            
    match clearedLines:
        case 4:
            clearedLines *= 10 #tetris gucci af
        case 3:
            clearedLines *= 0.75 #triple are horrible value
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
        
    return bumpiness * 4

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

def tetrisSlot(board, well):
    blocking = 0
    for i in range(20):
        lineCleared = " " not in board[i]
        if (well[i] != "I" and well[i] != " ") or well[i] == "I" and not lineCleared:
            blocking += 1

    return blocking

def iDependency(colHeights):
    iDep = 0

    for i in range(0, 9):
        c, l, r = colHeights[i], colHeights[i-1], colHeights[i+1] #heights of current and adjacent columns
        if l - c >= 3 and r - c >= 3:
            iDep += 1
            
    if colHeights[-2] - colHeights[-1] >= 3:
        iDep += 1
    if colHeights[2] - colHeights[1] >= 3:
        iDep += 1

    return iDep


def analyze(board):
    weights = [
    -1.030,   # aggregate
     0.760,   # increase tetris score after mvp
    -0.420,   # bumpiness
    -6.474,  # blockade
    -1.942,   # tetris well
    -2.420    # i piece dependencies
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
    varB = clearedLines(board) 
    varC = bumpiness(colHeights)
    varD = blockade(columns)
    varE = tetrisSlot(board, columns[0])
    varF = iDependency(colHeights)
    print(f"aggregate: {varA}, clearedLines: {varB}, bumpiness: {varC}, blockade: {varD}, tetrisSlot: {varE}, iDependency: {varF}")
    print(a*varA + b*varB + c*varC + d*varD + e*varE + f*varF)
    return a*varA + b*varB + c*varC + d*varD + e*varE + f*varF

def analyze_main(board):
    # this one is for the board view printing
    weights = [
    -1.030,   # aggregate
     0.760,   # increase tetris score after mvp
    -0.420,   # bumpiness
    -6.474,  # blockade
    -1.942,   # tetris well
    -2.420    # i piece dependencies
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
    varB = clearedLines(board) 
    varC = bumpiness(colHeights)
    varD = blockade(columns)
    varE = tetrisSlot(board, columns[0])
    varF = iDependency(colHeights)
    return a*varA, b*varB, c*varC, d*varD, e*varE, f*varF