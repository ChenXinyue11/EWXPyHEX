import Hex_Block as Hex
from itertools import combinations
FIXORDER = [(3,2),(2,3),(4,1),(1,4),(5,0),(0,5),(2,2),(3,3),
            (3,1),(2,5),(1,3),(4,2),(4,0),(1,5),(0,4),(5,1),
            (1,2),(4,3),(2,1),(3,4),(0,3),(5,2),(3,0),(2,5),
            (1,1),(4,4),(0,2),(5,3),(2,0),(3,5),(0,1),(5,4),(1,0),(4,5),(0,0),(5,5)]

def fixorder(moves):
    new = []
    for move in FIXORDER:
        if move in moves:
            move = Hex.coord_to_point(move[0],move[1],6)
            new.append(move)
    fullsore = len(new)
    scorelist = []
    for i in range(len(new)):
        scorelist.append((new[i],fullsore-i))
    return new,scorelist

def fillin(board):
    top = list(Hex.TOP_ROW)
    btm = list(Hex.BTM_ROW)
    lft = list(Hex.LFT_COL)
    rgt = list(Hex.RGT_COL)
    top.sort()
    btm.sort() 
    lft.sort()
    rgt.sort()
    for i in range(len(top)-1):
        if board.brd[top[i] + Hex.COLS] != Hex.BCH:
            continue
        if board.brd[top[i]] == Hex.WCH or board.brd[top[i+1]] == Hex.WCH:
            continue
        if board.brd[top[i]] == Hex.ECH:
            board.change_str_no_history(top[i],Hex.BCH)
        if board.brd[top[i+1]] == Hex.ECH:
            board.change_str_no_history(top[i+1],Hex.BCH)
    for i in range(1,len(btm)):
        if board.brd[btm[i] - Hex.COLS] != Hex.BCH:
            continue
        if board.brd[btm[i]] == Hex.WCH or board.brd[btm[i-1]] == Hex.WCH:
            continue
        if board.brd[btm[i]] == Hex.ECH:
            board.change_str_no_history(btm[i],Hex.BCH)
        if board.brd[btm[i-1]] == Hex.ECH:
            board.change_str_no_history(btm[i-1],Hex.BCH)
    for i in range(len(lft)-1):
        if board.brd[lft[i] + 1] != Hex.WCH:
            continue
        if board.brd[lft[i]] == Hex.BCH or board.brd[lft[i+1]] == Hex.BCH:
            continue
        if board.brd[lft[i]] == Hex.ECH:
            board.change_str_no_history(lft[i],Hex.WCH)
        if board.brd[lft[i+1]] == Hex.ECH:
            board.change_str_no_history(lft[i+1],Hex.WCH)
    for i in range(1,len(rgt)):
        if board.brd[rgt[i] - 1] != Hex.WCH:
            continue
        if board.brd[rgt[i]] == Hex.BCH or board.brd[rgt[i-1]] == Hex.BCH:
            continue
        if board.brd[rgt[i]] == Hex.ECH:
            board.change_str_no_history(rgt[i],Hex.WCH)
        if board.brd[rgt[i-1]] == Hex.ECH:
            board.change_str_no_history(rgt[i-1],Hex.WCH)

def capture(board,color):
    captured = set()
    top = list(Hex.TOP_ROW)
    btm = list(Hex.BTM_ROW)
    lft = list(Hex.LFT_COL)
    rgt = list(Hex.RGT_COL)
    top.sort()
    btm.sort() 
    lft.sort()
    rgt.sort()
    if color == Hex.BCH:
        for i in range(len(top)-1):
            if board.brd[top[i] + Hex.COLS] == Hex.ECH and board.brd[top[i]] == Hex.ECH and board.brd[top[i+1]] == Hex.ECH:
                captured.add(top[i])
                captured.add(top[i+1])
        for i in range(1,len(btm)):
            if board.brd[btm[i] - Hex.COLS] == Hex.ECH and board.brd[btm[i]] == Hex.ECH and board.brd[btm[i-1]] == Hex.ECH:
                captured.add(btm[i])
                captured.add(btm[i-1])
    elif color == Hex.WCH:
        for i in range(len(lft)-1):
            if board.brd[lft[i] + 1] == Hex.ECH and board.brd[lft[i]] == Hex.ECH and board.brd[lft[i+1]] == Hex.ECH:
                captured.add(lft[i])
                captured.add(lft[i+1])
        for i in range(1,len(rgt)):
            if board.brd[rgt[i] - 1] == Hex.ECH and board.brd[rgt[i]] == Hex.ECH and board.brd[rgt[i-1]] == Hex.ECH:
                captured.add(rgt[i])
                captured.add(rgt[i-1])
    return captured

def center_weight(score_list,r,c):
    dl = dline(r,c)
    for i in range(0,len(score_list)):
        move_score = score_list[i]
        point = move_score[0]
        move = Hex.point_to_coord(point,Hex.COLS)
        score = move_score[1]
        weightv = min(move[0]+1, r-move[0])
        weighth = min(move[1]+1, c-move[1])
        weight = round((weighth/10+weightv/10),2)
        if point in dl:
            weight +=1
        score_list[i] = (point,score+weight)
    return score_list  
def dline(r,c):
    lis = []
    for m in range(r):
        move = (m,c-m-1)
        move = Hex.coord_to_point(move[0],move[1],Hex.COLS)
        lis.append(move)
    return lis 

a = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0]] 
p = Hex.Position(3, 3)


cap = capture(p,Hex.BCH)
print(cap)
score = center_weight(a,3,3)
print(score)
Hex.showboard(p.brd, 3, 3)
