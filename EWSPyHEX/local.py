import Hex
def local_area(board,ptm,type = 1):
    area = set()
    optm = Hex.oppCH(ptm)
    if ptm == Hex.BCH:
        for cell in Hex.CELLS:
            if board[cell] == ptm:
                toplist = [cell]
                bottomlist = [cell]
                cordcell = Hex.point_to_coord(cell,Hex.COLS)
                if type == 2:
                    if cordcell[1] > 0:    
                        bottomlist.append(Hex.coord_to_point(cordcell[0],   cordcell[1]-1, Hex.COLS))
                        toplist.append(Hex.coord_to_point(cordcell[0],   cordcell[1]-1, Hex.COLS))
                    if cordcell[1] < Hex.COLS-1: 
                        bottomlist.append(Hex.coord_to_point(cordcell[0],   cordcell[1]+1, Hex.COLS))
                        toplist.append(Hex.coord_to_point(cordcell[0],   cordcell[1]+1, Hex.COLS))
                
                while len(toplist) > 0:
                    current = toplist.pop()
                    area.add(current)
                    if current < Hex.COLS:
                        continue
                    cord = Hex.point_to_coord(current,Hex.COLS)
                    topcells = []
                    if cord[0] > 0:                topcells.append(Hex.coord_to_point(cord[0]-1, cord[1],   Hex.COLS))
                    if cord[0] > 0 and cord[1] < Hex.COLS-1: topcells.append(Hex.coord_to_point(cord[0]-1, cord[1]+1, Hex.COLS))
                    for neighbor in topcells:
                        if board[neighbor] != optm and neighbor not in area:
                            toplist.append(neighbor)
                while len(bottomlist) > 0:
                    current = bottomlist.pop()
                    area.add(current)
                    if current >= (Hex.COLS*Hex.ROWS - Hex.COLS):
                        continue
                    bottomcells = []
                    cord = Hex.point_to_coord(current,Hex.COLS)
                    if cord[0] < Hex.ROWS-1:
                        bottomcells.append(Hex.coord_to_point(cord[0]+1, cord[1],   Hex.COLS))
                    if cord[0] < Hex.ROWS-1 and cord[1] > 0:
                        bottomcells.append(Hex.coord_to_point(cord[0]+1, cord[1]-1, Hex.COLS))
                    for neighbor in bottomcells:
                        if board[neighbor] != optm and neighbor not in area:
                            bottomlist.append(neighbor)
        if area != set():
            area.add(-4)
            area.add(-2)
    elif ptm == Hex.WCH:
        for cell in Hex.CELLS:
            if board[cell] == ptm:
                leftlist = [cell]
                rightlist = [cell]  
                cordcell = Hex.point_to_coord(cell,Hex.COLS)
                if type == 2:
                    if cordcell[0] > 0:    
                        leftlist.append(Hex.coord_to_point(cordcell[0]-1,   cordcell[1], Hex.COLS))
                        rightlist.append(Hex.coord_to_point(cordcell[0]-1,   cordcell[1], Hex.COLS))
                    if cordcell[0] < Hex.ROWS-1: 
                        leftlist.append(Hex.coord_to_point(cordcell[0]+1,   cordcell[1], Hex.COLS))
                        rightlist.append(Hex.coord_to_point(cordcell[0]+1,   cordcell[1], Hex.COLS))
                while len(leftlist) > 0:
                    current = leftlist.pop()
                    area.add(current)
                    if current % Hex.COLS == 0:
                        continue
                    cord = Hex.point_to_coord(current,Hex.COLS)
                    leftcells = []
                    if cord[1] > 0:                
                        leftcells.append(Hex.coord_to_point(cord[0], cord[1]-1,   Hex.COLS))
                    if cord[0] < Hex.ROWS-1 and cord[1] > 0: 
                        leftcells.append(Hex.coord_to_point(cord[0]+1, cord[1]-1, Hex.COLS))
                    for neighbor in leftcells:
                        if board[neighbor] != optm and neighbor not in area:
                            leftlist.append(neighbor)
                while len(rightlist) > 0:
                    current = rightlist.pop()
                    area.add(current)
                    if current % Hex.COLS == (Hex.COLS - 1):
                        continue
                    rightcells = []
                    cord = Hex.point_to_coord(current,Hex.COLS)
                    if cord[1] < Hex.COLS-1:
                        rightcells.append(Hex.coord_to_point(cord[0], cord[1]+1,   Hex.COLS))
                    if cord[0] >0 and cord[1] < Hex.COLS-1:
                        rightcells.append(Hex.coord_to_point(cord[0]-1, cord[1]+1, Hex.COLS))
                    for neighbor in rightcells:
                        if board[neighbor] != optm and neighbor not in area:
                            rightlist.append(neighbor)  
        if area != set():
            area.add(-1)
            area.add(-3)
    return area

'''g = Hex.Position(6,6)
g.change_str(15,Hex.WCH)
g.change_str(22,Hex.WCH)
Hex.showboard(g.brd,Hex.ROWS,Hex.COLS)
print(local_area(g.brd,Hex.WCH,2))'''

            