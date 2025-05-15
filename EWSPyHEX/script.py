import time,csv
import random
import TT
import Hex
import EWS,EWS_TT,EWS_TT,EWS_TT_Fill,EWS_TT_Fill_H,EWS_TT_Fill_H_TH,EWS_TT_Fill_H_TH_INCRE
import Nega,Nega_TT,Nega_TT_fill,Nega_TT_fill_H,Nega_TT_fill_H_TH,Nega_TT_fill_H_TH_INCRE
import Nega_TT_fill_H_TH_local,Nega_TT_fill_H_TH_local_limit
import EWS_Hvalue,EWS_VISIT,EWS_Hvalue_2
import Nega_TT_H_NoMO,EWS_TT_Fill_H_TH_INCRE_hvalue
LIS = [ [(0, 4), (3, 1), (0, 3)],[(1, 5), (1, 2), (5, 5)], [(3, 0), (4, 1), (5, 4)], [(4, 4), (4, 5), (2, 1)], [(4, 0), (1, 2), (3, 1)], [(0, 0), (2, 1), (3, 5)], [(3, 4), (2, 2), (3, 3)], [(4, 3), (3, 4), (2, 3)], [(5, 4), (1, 5), (0, 0)], [(2, 0), (5, 1), (5, 3)], [(1, 0), (5, 2), (4, 0)], [(4, 0), (0, 5), (1, 3)], [(2, 3), (1, 5), (5, 2)], [(2, 0), (2, 5), (0, 5)], [(5, 5), (0, 1), (3, 3)], [(3, 3), (5, 1), (2, 5)], [(1, 2), (3, 4), (2, 5)], [(2, 3), (0, 2), (2, 1)], [(3, 5), (0, 0), (3, 1)], [(3, 0), (5, 3), (4, 4)], [(0, 1), (3, 5), (4, 2)], [(5, 4), (2, 1), (1, 3)], [(5, 4), (0, 0), (2, 5)], [(2, 5), (2, 2), (2, 3)], [(2, 0), (5, 3), (4, 2)], [(0, 4), (0, 0), (1, 3)], [(3, 4), (3, 5), (0, 3)], [(5, 2), 
 (4, 5), (3, 4)], [(5, 4), (1, 1), (3, 0)], [(0, 5), (2, 3), (0, 3)], [(0, 0), (4, 5), (0, 1)], [(4, 5), (0, 3), (3, 4)], [(4, 0), (1, 2), (4, 3)], [(3, 4), (5, 0), (2, 5)], [(0, 0), (3, 4), (4, 5)], [(2, 0), (5, 5), (0, 0)], [(3, 4), (2, 1), (3, 
1)], [(0, 3), (5, 1), (0, 2)], [(5, 2), (5, 4), (3, 2)], [(4, 0), (4, 2), (1, 3)], [(3, 1), (5, 1), (1, 5)], [(0, 3), (1, 2), (4, 1)], [(4, 3), (1, 1), (5, 5)], [(4, 1), (1, 5), (4, 5)], [(0, 2), (3, 0), (2, 5)], [(5, 4), (2, 4), (5, 2)], [(5, 4), (5, 3), (0, 3)], [(3, 4), (2, 5), (5, 4)], [(1, 5), (2, 0), (4, 1)],[(2, 1), (2, 5), (0, 1)]]
LIS2 = [ [(0, 4), (3, 1), (0, 3)],[(3, 2),]]
def solve():
    for i in range(3,5):
        string = 'Nega_'+str(i)+'.csv'
        resultlists = []
        g = Hex.Position(i,i)
        start = time.time()
        r,m,iter = Nega.negamx(g.brd,Hex.BCH,start,1000)
        temp = [(i,i),time.time()-start,r,m,iter]
        resultlists.append(temp)
        for j in range(i*i):
            g = Hex.Position(i,i)
            g.change_str(j,Hex.BCH)
            start = time.time()
            r,m,iter = Nega.negamx(g.brd,Hex.WCH,start,1000)
            temp = [(j),time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)
    for i in range(3,5):
        string = 'Nega_TT_'+str(i)+'.csv'
        resultlists = []
        g = Hex.Position(i,i)
        start = time.time()
        tt = TT.TranspositionTable()
        r,m,iter = Nega_TT.negamx(g.brd,Hex.BCH,tt,start,1000)
        temp = [(i,i),time.time()-start,r,m,iter]
        resultlists.append(temp)
        for j in range(i*i):
            g = Hex.Position(i,i)
            g.change_str(j,Hex.BCH)
            tt = TT.TranspositionTable()
            start = time.time()
            r,m,iter = Nega_TT.negamx(g.brd,Hex.WCH,tt,start,1000)
            temp = [(j),time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)
    for i in range(3,5):
        string = 'Nega_TT_Fill_'+str(i)+'.csv'
        resultlists = []
        g = Hex.Position(i,i)
        start = time.time()
        tt = TT.TranspositionTable()
        r,m,iter = Nega_TT_fill.negamx_2(g,Hex.BCH,tt,start,1000)
        temp = [(i,i),time.time()-start,r,m,iter]
        resultlists.append(temp)
        for j in range(i*i):
            g = Hex.Position(i,i)
            g.change_str(j,Hex.BCH)
            tt = TT.TranspositionTable()
            start = time.time()
            r,m,iter = Nega_TT_fill.negamx_2(g,Hex.WCH,tt,start,1000)
            temp = [(j),time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)
    '''function = [Nega_TT_fill_H,Nega_TT_fill_H_TH]
    function_str = ['Nega_TT_fill_H','Nega_TT_fill_H_TH']
    for f in range(len(function)):
        sf = function[f]
        sfstring = function_str[f]'''
    for i in range(4,6):
        string = 'Nega_TT_fill_H_'+str(i)+'.csv'
        resultlists = []
        tt = TT.TranspositionTable()
        g = Hex.Position(i,i)
        start = time.time()
        r,m,iter = Nega_TT_fill_H.negamx_2(g,Hex.BCH,tt,start,1000)
        temp = [(i,i),time.time()-start,r,m,iter]
        resultlists.append(temp)
        for j in range(i*i):
            g = Hex.Position(i,i)
            g.change_str(j,Hex.BCH)
            tt = TT.TranspositionTable()
            start = time.time()
            r,m,iter = Nega_TT_fill_H.negamx_2(g,Hex.WCH,tt,start,1000)
            temp = [(j),time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)
    for i in range(4,6):
        string = 'Nega_TT_fill_H_TH_'+str(i)+'.csv'
        resultlists = []
        tt = TT.TranspositionTable()
        th = TT.TranspositionConnection()
        g = Hex.Position(i,i)
        start = time.time()
        r,m,iter = Nega_TT_fill_H_TH.negamx_2(g,Hex.BCH,tt,th,start,1000)
        temp = [(i,i),time.time()-start,r,m,iter]
        resultlists.append(temp)
        for j in range(i*i):
            g = Hex.Position(i,i)
            g.change_str(j,Hex.BCH)
            th = TT.TranspositionConnection()
            tt = TT.TranspositionTable()
            start = time.time()
            r,m,iter = Nega_TT_fill_H_TH.negamx_2(g,Hex.WCH,tt,th,start,1000)
            temp = [(j),time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)
    function = [EWS,EWS_TT,EWS_TT_Fill]
    function_str = ['EWS','EWS_TT','EWS_TT_Fill']
    for f in range(len(function)):
        sf = function[f]
        sfstring = function_str[f]
        for i in range(3,5):
            string = sfstring+'_'+str(i)+'.csv'
            resultlists = []
            g = Hex.Position(i,i)
            start = time.time()
            ews = sf.EWS(g)
            r,m,iter = ews.Solve(Hex.BCH,1000)
            temp = [(i,i),time.time()-start,r,m,iter]
            resultlists.append(temp)
            for j in range(i*i):
                g = Hex.Position(i,i)
                g.change_str(j,Hex.BCH)
                ews = sf.EWS(g)
                start = time.time()
                r,m,iter = ews.Solve(Hex.WCH,1000)
                temp = [(j),time.time()-start,r,m,iter]
                resultlists.append(temp)
            with open(string, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(resultlists)


    function = [EWS_TT_Fill_H,EWS_TT_Fill_H_TH]
    function_str = ['EWS_TT_Fill_H','EWS_TT_Fill_H_TH']
    for f in range(len(function)):
        sf = function[f]
        sfstring = function_str[f]
        for i in range(4,6):
            string = sfstring+'_'+str(i)+'.csv'
            resultlists = []
            g = Hex.Position(i,i)
            start = time.time()
            ews = sf.EWS(g)
            r,m,iter = ews.Solve(Hex.BCH,1000)
            temp = [(i,i),time.time()-start,r,m,iter]
            resultlists.append(temp)
            for j in range(i*i):
                g = Hex.Position(i,i)
                g.change_str(j,Hex.BCH)
                ews = sf.EWS(g)
                start = time.time()
                r,m,iter = ews.Solve(Hex.WCH,1000)
                temp = [(j),time.time()-start,r,m,iter]
                resultlists.append(temp)
            with open(string, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(resultlists)

def solve_2():
    resultlists = []
    for move in LIS:
        move = [Hex.coord_to_point(i[0],i[1],6) for i in move]
        g = Hex.Position(6,6)
        player = Hex.BCH
        for m in move:
            g.change_str(m,player)
            player = Hex.oppCH(player)
        tt = TT.TranspositionTable()
        th = TT.TranspositionConnection()
        start = time.time()
        r,m,iter = Nega_TT_fill_H_TH.negamx_2(g,player,tt,th,start,1000)
        temp = [move,time.time()-start,r,m,iter]
        resultlists.append(temp)
    with open('Nega_TT_fill_H_TH_63.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(resultlists)
    
    resultlists = []
    for move in LIS:
        move = [Hex.coord_to_point(i[0],i[1],6) for i in move]
        g = Hex.Position(6,6)
        player = Hex.BCH
        for m in move:
            g.change_str(m,player)
            player = Hex.oppCH(player)
        start = time.time()
        ews = EWS_TT_Fill_H_TH_INCRE.EWS(g)
        r,m,iter = ews.Solve(player,1000)
        temp = [move,time.time()-start,r,m,iter]
        resultlists.append(temp)
    with open('EWS_TT_fill_H_TH_incre_63.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(resultlists)
def solve_3():
    '''resultlists = []
    for move in LIS:
        move = [Hex.coord_to_point(i[0],i[1],6) for i in move]
        g = Hex.Position(6,6)
        player = Hex.BCH
        for m in move:
            g.change_str(m,player)
            player = Hex.oppCH(player)
        tt = TT.TranspositionTable()
        th = TT.TranspositionConnection()
        start = time.time()
        r,m,iter = Nega_TT_fill_H_TH_INCRE.negamx_2(g,player,tt,th,start,1000)
        temp = [move,time.time()-start,r,m,iter]
        resultlists.append(temp)
    with open('Nega_TT_fill_H_TH_incre_63.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(resultlists)'''
    
    resultlists = []
    for move in LIS:
        move = [Hex.coord_to_point(i[0],i[1],6) for i in move]
        g = Hex.Position(6,6)
        player = Hex.BCH
        for m in move:
            g.change_str(m,player)
            player = Hex.oppCH(player)
        start = time.time()
        ews = EWS_TT_Fill_H_TH.EWS(g)
        r,m,iter = ews.Solve(player,1000)
        temp = [move,time.time()-start,r,m,iter]
        resultlists.append(temp)
    with open('EWS_TT_fill_H_TH_incre_63.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(resultlists)

def solve_4():
    '''for i in range(6,7):
        string = 'Nega_all_6'+str(i)+'.csv'
        resultlists = []
        tt = TT.TranspositionTable()
        g = Hex.Position(i,i)
        start = time.time()
        r,m,iter = Nega_TT_fill_H.negamx_2(g,Hex.BCH,tt,start,2000)
        temp = [(i,i),time.time()-start,r,m,iter]
        resultlists.append(temp)
        for j in range(i*i):
            print(j)
            g = Hex.Position(i,i)
            g.change_str(j,Hex.BCH)
            tt = TT.TranspositionTable()
            start = time.time()
            r,m,iter = Nega_TT_fill_H.negamx_2(g,Hex.WCH,tt,start,2000)
            temp = [(j),time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)'''
    for i in range(6,7):
        string = 'EWS_hvaue_incre_single2'+str(i)+'.csv'
        resultlists = []
        g = Hex.Position(i,i)
        start = time.time()
        ews = EWS_TT_Fill_H_TH_INCRE_hvalue.EWS(g,5)
        r,m,iter = ews.Solve(Hex.BCH,20000)
        temp = [(i,i),time.time()-start,r,m,iter]
        resultlists.append(temp)
        for j in range(i*i):
            if j != 23:
                continue
            g = Hex.Position(i,i)
            g.change_str(j,Hex.BCH)
            ews = EWS_TT_Fill_H_TH_INCRE_hvalue.EWS(g,5)
            start = time.time()
            r,m,iter = ews.Solve(Hex.WCH,20000)
            temp = [(j),time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)
    print('done4')
def solve_5():
    '''for i in range(5,6):
        string = 'Nega_local'+str(i)+'.csv'
        resultlists = []
        tt = TT.TranspositionTable()
        th = TT.TranspositionConnection()
        g = Hex.Position(i,i)
        start = time.time()
        r,m,iter = Nega_TT_fill_H_TH_local.negamx_2(g,Hex.BCH,tt,th,start,1000)
        temp = [(i,i),time.time()-start,r,m,iter]
        resultlists.append(temp)
        for j in range(i*i):
            print(j)
            g = Hex.Position(i,i)
            g.change_str(j,Hex.BCH)
            tt = TT.TranspositionTable()
            th = TT.TranspositionConnection()
            start = time.time()
            r,m,iter = Nega_TT_fill_H_TH_local.negamx_2(g,Hex.WCH,tt,th,start,1000)
            temp = [(j),time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)'''
    for i in range(5,6):
        string = 'new_nega_mo_'+str(i)+'.csv'
        resultlists = []
        tt = TT.TranspositionTable()
        th = TT.TranspositionConnection()
        g = Hex.Position(i,i)
        start = time.time()
        r,m,iter = Nega_TT_H_NoMO.negamx_2(g,Hex.BCH,tt,start,1000)
        temp = [(i,i),time.time()-start,r,m,iter]
        resultlists.append(temp)
        for j in range(i*i):
            print(j)
            g = Hex.Position(i,i)
            g.change_str(j,Hex.BCH)
            tt = TT.TranspositionTable()
            th = TT.TranspositionConnection()
            start = time.time()
            r,m,iter = Nega_TT_H_NoMO.negamx_2(g,Hex.WCH,tt,start,1000)
            temp = [(j),time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)
def solve_6():

    Hlistt = [5,]#1,5,10]

    for v in Hlistt:
        resultlists = []
        string = 'EWS_HVALUE_incre_663'+str(v)+'.csv'
        for move in LIS:
            move = [Hex.coord_to_point(i[0],i[1],6) for i in move]
            g = Hex.Position(6,6)
            player = Hex.BCH
            for m in move:
                g.change_str(m,player)
                player = Hex.oppCH(player)
            start = time.time()
            ews = EWS_TT_Fill_H_TH_INCRE_hvalue.EWS(g,v)
            r,m,iter = ews.Solve(player,1000)
            temp = [move,time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)

    '''visitlistt = [0,5,10,100]

    for v in visitlistt:
        resultlists = []
        string = 'EWS_VISIT'+str(v)+'.csv'
        for move in LIS:
            move = [Hex.coord_to_point(i[0],i[1],6) for i in move]
            g = Hex.Position(6,6)
            player = Hex.BCH
            for m in move:
                g.change_str(m,player)
                player = Hex.oppCH(player)
            start = time.time()
            ews = EWS_VISIT.EWS(g,v)
            r,m,iter = ews.Solve(player,1000)
            temp = [move,time.time()-start,r,m,iter]
            resultlists.append(temp)
        with open(string, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(resultlists)'''
def solve_7():
    resultlists = []
    for move in LIS:
        move = [Hex.coord_to_point(i[0],i[1],6) for i in move]
        g = Hex.Position(6,6)
        player = Hex.BCH
        for m in move:
            g.change_str(m,player)
            player = Hex.oppCH(player)
        tt = TT.TranspositionTable()
        th = TT.TranspositionConnection()
        start = time.time()
        r,m,iter = Nega_TT_fill_H_TH_local_limit.negamx_2(g,player,tt,th,start,1000)
        temp = [move,time.time()-start,r,m,iter]
        resultlists.append(temp)
    with open('Nega_local_number_63.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(resultlists)    
#solve_4()
#solve_5()
#solve_6()
#solve_3()
solve_4()