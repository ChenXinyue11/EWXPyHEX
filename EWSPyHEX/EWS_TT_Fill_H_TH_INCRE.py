
import random,time
import Hex
import TT
from copy import deepcopy
import Fill_in,Fill_in_Nega
import H_Nob_Single_ES_INCRE as nb
VERBOSE = False
PRINT_ITERATIONS = True
ITER_FREQ = 100
WR_WEIGHT = 1

class Node:
    def __init__(self, move,ptm):
        self.ptm = ptm
        self.children = []
        self.move = move
        self.expanded = False
        self.wins = 1
        self.visits = 2
        self.ewLoss = 0
        self.ewWin = 0
        self.pvcs = None
        self.psvcs = None
        self.Ovcs = None
        self.Osvcs = None
        self.Ohash = None
        self.Phash = None

    def RemoveChild(self, move):
        for i in range(len(self.children)):
            if self.children[i].move == move:
                del self.children[i]
                return

    def Value(self, pVisits):
        return (WR_WEIGHT / (WR_WEIGHT + pVisits)) * (self.ewLoss / (1 - self.wins / self.visits))\
            + (1 - (WR_WEIGHT / (WR_WEIGHT + pVisits))) * (1 / (1 - self.wins / self.visits))

    def SortChildren(self):
        if len(self.children) <= 1:
            return
        self.children.sort(key=lambda x: x.Value(self.visits))

    def UpdateWinRate(self, wins, visits):
        self.wins += wins
        self.visits += visits

    def UpdateEW(self):
        self.ewLoss = sum([child.ewWin for child in self.children])
        self.ewWin = 0
        p = 1
        for child in self.children:
            self.ewWin += p * child.ewLoss
            p *= child.wins / child.visits

    def PrintChildren(self):
        print("[", end="")
        for c in self.children:
            print(c.move, end=", ")
        print("]")

class EWS:
    def __init__(self, game):
        self.game = game

    def Evaluate(self, node):
        if VERBOSE:
            print("Evaluate")
            self.game.Print()
        toPlay = True
        numMoves = 0
        node.visits += 1
        #self.game.takeSnapshot()
        gamestr = self.game.brd
        ptm = node.ptm
        while True:
            gamestr = Fill_in_Nega.fillin(gamestr)
            captured = Fill_in_Nega.capture(gamestr,ptm)
            moves = list(set(Hex.get_moves(gamestr))-captured)

            '''if VERBOSE:
                print(moves)'''
            node.ewLoss += len(moves)
            node.ewWin += len(moves)
            move = moves[random.randint(0, len(moves) - 1)]
            #self.game.MakeMove(move, False)
            gamestr = Hex.change_str(gamestr, move, ptm)
            gamestr = Fill_in_Nega.fillin(gamestr)
            '''if VERBOSE:
                print(move)
                self.game.Print()'''
            numMoves += 1
            #isTerminal, isWinning = self.game.IsTerminal()
            winning= Hex.has_win(gamestr, ptm)
            if winning:
                if ptm == node.ptm:
                    node.wins += 1
                    '''if VERBOSE:
                        print("win")'''
                    return True
                else:
                    '''if VERBOSE:
                        print("loss")'''
                    return False
            ptm = Hex.oppCH(ptm)


    def Expand(self, node,tt,th,pstring = None,Ooldvcs = None,Ooldscvs = None,Poldvcs = None,Poldsvcs =None,Ooldhash = None,Poldhash = None):
        '''if VERBOSE:
            print("Expand")
            self.game.Print()'''
        node.expanded = True
        wins = 0
        visits = 0
        Fill_in.fillin(self.game)
        result = tt.lookup(self.game.brd)
        if result != None:
            if result == node.ptm:
                return True, True, 1, 1, None
            elif result == Hex.oppCH(node.ptm):
                return True, False, 0, 1, None
        if Hex.has_win(self.game.brd, Hex.oppCH(node.ptm)):
            tt.store(self.game.brd, Hex.oppCH(node.ptm))
            return True, False, 0, 1, None
        elif Hex.has_win(self.game.brd, node.ptm):
            tt.store(self.game.brd, node.ptm)
            return True, True, 1, 1, None
        reslt = th.lookup(self.game.brd)
        if reslt != None:
            node.pvcs,node.psvcs,node.Phash,node.Ovcs,node.Osvcs,node.Ohash,mustplay = reslt[0],reslt[1],reslt[2],reslt[3],reslt[4],reslt[5],reslt[6]
            '''if op_win:
                tt.store(self.game.brd, Hex.oppCH(node.ptm))
                return True, False, 0, 1
            elif player_win:
                tt.store(self.game.brd, node.ptm)
                return True, True, 1, 1
            else:'''
            moves = mustplay
        else:
            mustplay = []
            Ovcs, Osvcs,Ohash,Ovw,Osw = nb.hsearch(self.game.brd,Hex.oppCH(node.ptm),False,0,pstring,Poldvcs,Poldsvcs,Poldhash,True)
            if Ovw == True:
                tt.store(self.game.brd, Hex.oppCH(node.ptm))
                return True, False, 0, 1, None
            pvcs, psvcs,phash,pvw,psw = nb.hsearch(self.game.brd,node.ptm,True,0,pstring,Ooldvcs,Ooldscvs,Ooldhash,False)
            if psw == True:
                tt.store(self.game.brd, node.ptm)
                return True, True, 1, 1,None
            captured = Fill_in.capture(self.game,node.ptm)
            mustplay = nb.mustplay_zone(self.game.brd,Ovcs,Osvcs,Hex.oppCH(node.ptm))
            moves = []
            node.pvcs = pvcs
            node.psvcs = psvcs
            node.Ovcs = Ovcs
            node.Osvcs = Osvcs
            node.Ohash = Ohash
            node.Phash = phash
            if mustplay == "nowin":
                tt.store(self.game.brd, Hex.oppCH(node.ptm))
                return True, False, 0, 1, None
            elif len(mustplay) == 0:
                for k in Hex.CELLS:
                    if self.game.brd[k]==Hex.ECH and k not in captured:
                        moves.append(k)
            else:
                for k in mustplay:
                    if self.game.brd[k]==Hex.ECH and k not in captured:
                        moves.append(k)
            th.store(self.game.brd,[pvcs,psvcs,phash,Ovcs,Osvcs,Ohash,moves])
        #moves = list(set(Hex.get_moves(self.game.brd))-captured)
        #moves,slist = nb.mustplay_order(moves,self.game.brd,pvcs,psvcs,node.ptm)
        for m in moves:
            self.game.change_str(m, node.ptm)
            Fill_in.fillin(self.game)
            winning= Hex.has_win(self.game.brd, node.ptm) # isWinning is for the last player to move
            '''if VERBOSE:
                print("move", m, "terminal", isTerminal, "winning", isWinning)'''
            if winning:
                '''if VERBOSE:
                    print("Winning child:", m)
                    self.game.Print()
                    print()'''
                tt.store(self.game.brd, node.ptm)
                self.game.undo()
                return True, True, 1, 1,m
            else:
                child = Node(m,Hex.oppCH(node.ptm))
                node.children.append(child)
                childWon = self.Evaluate(child)
                if not childWon:
                    wins += 1
                visits += 1
            self.game.undo()

        '''if VERBOSE:
            node.PrintChildren()
            print()'''
        if len(node.children) == 0:
            tt.store(self.game.brd, Hex.oppCH(node.ptm))
        return len(node.children) == 0, False, wins, visits,None

    def SelectBackpropagate(self, node,tt,th):
        result = tt.lookup(self.game.brd)
        if result != None:
            if result == node.ptm:
                return True, True, 1, 1,None
            elif result == Hex.oppCH(node.ptm):
                return True, False, 0, 1,None
        child = node.children[0]
        childMove = child.move
        '''if VERBOSE:
            print("SB")
            self.game.Print()
            node.PrintChildren()
            print("MOVE", childMove)
            print()'''
        string = deepcopy(self.game.brd)
        self.game.change_str(childMove, node.ptm)
        if child.expanded:
            isSolved, isWinning, wins, visits,wm = self.SelectBackpropagate(child,tt,th)
        else:
            isSolved, isWinning, wins, visits,wm = self.Expand(child,tt,th,string,node.Ovcs,node.Osvcs,node.pvcs,node.psvcs,node.Ohash,node.Phash)
        self.game.undo()
        '''if VERBOSE:
            print("UNDO")
            self.game.Print()'''
        wins = visits - wins
        node.UpdateWinRate(wins, visits)

        if isSolved and isWinning:
            node.RemoveChild(childMove)
            '''if VERBOSE:
                print("Solved child")
                node.PrintChildren()'''
            if len(node.children) == 0:
                '''if VERBOSE:
                    print("Solved losing")'''
                tt.store(self.game.brd, Hex.oppCH(node.ptm))
                return True, False, wins, visits,None
        elif isSolved and not isWinning:
            '''if VERBOSE:
                print("Solved winning")'''
            tt.store(self.game.brd, node.ptm)
            return True, True, wins, visits,childMove

        node.SortChildren()
        node.UpdateEW()
        if VERBOSE:
            print("Unsolved")
            node.PrintChildren()
            print()
        return False, False, wins, visits,None


    def Solve(self,ptm, timelimit = 1000):
        random.seed(1)
        start = time.time()
        #self.game.Reset()
        #self.game.Print()
        tt = TT.TranspositionTable()
        th = TT.TranspositionConnection()
        root = Node(None,ptm)
        isSolved, isWinning, wins, visits,wm = self.Expand(root,tt,th)
        if isSolved:
            return isWinning,wm,1
        isSolved, isWinning, _, _,wm = self.SelectBackpropagate(root,tt,th)
        iteration = 0
        while not isSolved:
            if time.time() - start > timelimit:
                return None,None,iteration
            '''if VERBOSE:
                print("------------------------------------------")
            if PRINT_ITERATIONS and iteration % ITER_FREQ == 0:
                print("Iteration num:", iteration)
                print("Root child nodes:")
                print("Move coords, win rate, visits, ewLoss, ewWin")
                for child in root.children:
                    print(child.move, round(child.wins / child.visits, 3), child.visits, round(child.ewLoss), round(child.ewWin))
                print()
                c = root
                print("Branching factors of last line searched:")
                while len(c.children) > 0:
                    print(len(c.children), end=" ")
                    c = c.children[0]
                print()
                print()'''
                
            iteration += 1
            if VERBOSE:
                input("Press enter to continue...")
            isSolved, isWinning, _, _,wm = self.SelectBackpropagate(root,tt,th)
        print(iteration)
        return isWinning,wm,iteration
