
import Hex
from itertools import combinations
FIXORDER = [(3,2),(2,3),(4,1),(1,4),(5,0),(0,5),(2,2),(3,3),
            (3,1),(2,5),(1,3),(4,2),(4,0),(1,5),(0,4),(5,1),
            (1,2),(4,3),(2,1),(3,4),(0,3),(5,2),(3,0),(2,5),
            (1,1),(4,4),(0,2),(5,3),(2,0),(3,5),(0,1),(5,4),(1,0),(4,5),(0,0),(5,5)]

def fixorder(moves):
    new = []
    for move in FIXORDER:
        if move in moves:
            new.append(move)
    fullsore = len(new)
    scorelist = []
    for i in range(len(new)):
        scorelist.append((new[i],fullsore-i))
    return new,scorelist
def fillin(board):
    stones = board.stones
    blacks = stones[Hex.BLACK].copy()
    whites = stones[Hex.WHITE].copy()
    for stone in blacks:
        if stone[0] ==1:
            if stone[1] ==(board.ySize -1):
                continue
                # addstone = stone-board.c
                # board.add_stone(BLACK, addstone, (addstone//board.c,addstone%board.c))
            else:
                addstone = (stone[0]-1,stone[1])
                addstone2 = (stone[0]-1,stone[1]+1)
                if  addstone in stones[0] and addstone2 in stones[0]:
                    board.MakeColorMove(addstone,Hex.BLACK)
                    board.MakeColorMove(addstone2,Hex.BLACK)
                elif addstone in stones[Hex.BLACK] and addstone2 in stones[0]:
                    board.MakeColorMove(addstone2,Hex.BLACK)
                elif addstone in stones[0] and addstone2 in stones[Hex.BLACK]:
                    board.MakeColorMove(addstone,Hex.BLACK)
        if stone[0] == board.xSize -2:
            if stone[1] ==0:
                continue
                # addstone = stone+board.c
                # board.add_stone(BLACK, addstone, (addstone//board.c,addstone%board.c))
            else:
                addstone = (stone[0]+1,stone[1]-1)
                addstone2 = (stone[0]+1,stone[1])
                if  addstone in stones[0] and addstone2 in stones[0]:
                    board.MakeColorMove(addstone,Hex.BLACK)
                    board.MakeColorMove(addstone2,Hex.BLACK)
                elif addstone in stones[Hex.BLACK] and addstone2 in stones[0]:
                    board.MakeColorMove(addstone2,Hex.BLACK)
                elif addstone in stones[0] and addstone2 in stones[Hex.BLACK]:
                    board.MakeColorMove(addstone,Hex.BLACK)
    for stone in whites:
        if stone[1] ==1:
            if stone[0] ==(board.xSize -1):
                continue
                # addstone = stone-board.c
                # board.add_stone(BLACK, addstone, (addstone//board.c,addstone%board.c))
            else:
                addstone = (stone[0],stone[1]-1)
                addstone2 = (stone[0]+1,stone[1]-1)
                if  addstone in stones[0] and addstone2 in stones[0]:
                    board.MakeColorMove(addstone,Hex.WHITE)
                    board.MakeColorMove(addstone2,Hex.WHITE)
                elif addstone in stones[Hex.WHITE] and addstone2 in stones[0]:
                    board.MakeColorMove(addstone2,Hex.WHITE)
                elif addstone in stones[0] and addstone2 in stones[Hex.WHITE]:
                    board.MakeColorMove(addstone,Hex.WHITE)
        if stone[1] == (board.xSize -2):
            if stone[0] ==0:
                continue
                # addstone = stone+board.c
                # board.add_stone(BLACK, addstone, (addstone//board.c,addstone%board.c))
            else:
                addstone = (stone[0]-1,stone[1]+1)
                addstone2 =(stone[0],stone[1]+1)
                if  addstone in stones[0] and addstone2 in stones[0]:
                    board.MakeColorMove(addstone,Hex.WHITE)
                    board.MakeColorMove(addstone2,Hex.WHITE)
                elif addstone in stones[Hex.WHITE] and addstone2 in stones[0]:
                    board.MakeColorMove(addstone2,Hex.WHITE)
                elif addstone in stones[0] and addstone2 in stones[Hex.WHITE]:
                    board.MakeColorMove(addstone,Hex.WHITE)
    return board

def capture(board,color):
    stones = board.stones
    empty = stones[Hex.EMPTY].copy()
    captured = set()
    for stone in empty:
        if color  == Hex.BLACK:
            if stone[0] ==1:
                if stone[1] ==(board.ySize -1):
                    continue
                    # addstone = stone-board.c
                    # board.add_stone(BLACK, addstone, (addstone//board.c,addstone%board.c))
                else:
                    addstone = (stone[0]-1,stone[1])
                    addstone2 = (stone[0]-1,stone[1]+1)
                    if  addstone in stones[0] and addstone2 in stones[0]:
                        captured.add(addstone)
                        captured.add(addstone2)
            if stone[0] == board.xSize -2:
                if stone[1] ==0:
                    continue
                    # addstone = stone+board.c
                    # board.add_stone(BLACK, addstone, (addstone//board.c,addstone%board.c))
                else:
                    addstone = (stone[0]+1,stone[1]-1)
                    addstone2 = (stone[0]+1,stone[1])
                    if  addstone in stones[0] and addstone2 in stones[0]:
                        captured.add(addstone)
                        captured.add(addstone2)
        if color == Hex.WHITE:
            if stone[1] ==1:
                if stone[0] ==(board.xSize -1):
                    continue
                    # addstone = stone-board.c
                    # board.add_stone(BLACK, addstone, (addstone//board.c,addstone%board.c))
                else:
                    addstone = (stone[0],stone[1]-1)
                    addstone2 = (stone[0]+1,stone[1]-1)
                    if  addstone in stones[0] and addstone2 in stones[0]:
                        captured.add(addstone)
                        captured.add(addstone2)
            if stone[1] == (board.xSize -2):
                if stone[0] ==0:
                    continue
                    # addstone = stone+board.c
                    # board.add_stone(BLACK, addstone, (addstone//board.c,addstone%board.c))
                else:
                    addstone = (stone[0]-1,stone[1]+1)
                    addstone2 =(stone[0],stone[1]+1)
                    if  addstone in stones[0] and addstone2 in stones[0]:
                        captured.add(addstone)
                        captured.add(addstone2)
    return captured

def center_weight(score_list,r,c):
    dl = dline(r,c)
    for i in range(0,len(score_list)):
        move_score = score_list[i]
        move = list(move_score[0])[0]
        score = move_score[1]
        weightv = min(move[0]+1, r-move[0])
        weighth = min(move[1]+1, c-move[1])
        #check for for
        weight = (weighth/10+weightv/10)
        if move in dl:
            weight +=0.2
        score_list[i] = (move_score[0],score+weight)
    if 1 == 0:
       pass 
    return score_list
def dline(r,c):
    lis = []
    k = 0
    for m in range(r):
        move = (m,c-m-1)
        lis.append(move)
    return lis
#print(dline(6,6))
# hw1 = ((BLACK,3,2),(WHITE,4,3),)
# hb = Stone_board(Game.hex_game, 6,6)
# for move in hw1:
#   hb.make_move(move)
# hb.print()
# new = fillin(hb)
# new.print()

'''g = Hex.HexGame(5, 5, 0.5)
g.MakeMove((1,3))
g.MakeColorMove((0,3),1)
g.MakeColorMove((0,4),1)
g.Print()
fillin(g)
g.Print()
print(g.board)
print(g.blocks)
'''
'''g = Hex.HexGame(5, 5, 0.5)
g.MakeMove((1,3))
g.MakeColorMove((3,2),1)
g = fillin(g)
g.Print()
print(capture(g,Hex.BLACK))'''