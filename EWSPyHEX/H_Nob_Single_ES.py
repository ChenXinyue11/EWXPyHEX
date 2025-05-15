import Hex,Fill_in
from itertools import combinations
import time

SEMI = 0
NON_SEMI = 1
side = [["-4","-2"],["-1","-3"]]
S = [[-4,-2],[-1,-3]]

class VC:
    def __init__(self, end1, end2, carrier, when):
        self.end1 = end1  # end 1 could be (1) or [(many)
        self.end2 = end2  # end 2
        self.carrier = carrier  # carrier list
        self.when = when  # when is the VC formed. s: start, o: or rule, a: add rule
        #todo use a list to keep c1 c2..., and attend svc object istead just a set of cells
        self.c1 = None
        self.c2 = None
        self.c3 = None
    def print(self):
        print("VC: " + " END 1: " + str(self.end1) + " END 2: " + str(self.end2) + " Carrier: " + str(self.carrier),
              "when", self.when, self.c1, self.c2, self.c3 )

class SVC:
    def __init__(self, end1, end2, carrier,key = None):
        self.end1 = end1  # end 1
        self.end2 = end2  # end 2
        self.carrier = carrier  # carrier
        self.key = key
        self.v1 = None
        self.v2 = None

    def print(self):
        print("SEMI-VC: " + " END 1: " + str(self.end1) + " END 2: " + str(self.end2) + " Carrier: " + str(self.carrier)+ " key: " + str(self.key))

def vc_hash(semi, end1, end2, carrier):
    # return a hashable string
    return str(semi) + str(end1) + str(end2) + str(carrier)
def is_subset(vcs, new_carrier):
    # find if there is an existing vcs that has a carrier which is a subset of the new carrier
    for c in vcs:
        if c.carrier.issubset(new_carrier) or len(c.carrier) == 0:
            return True
    return False
def remove_subset(vcs):
    # loop over vcs/svcs, remove the vc/svc that the carrier is a superset of an existing vc/svc
    for k, v in vcs.items():
        removeset = set()
        for v1, v2 in combinations(v, 2):
            if v1.carrier.issubset(v2.carrier):
                removeset.add(v2)
            elif v2.carrier.issubset(v1.carrier):
                removeset.add(v1)
        vcs[k] = vcs[k] - removeset
    return vcs

def start(board, hashtable, color, vcs=None, svcs=None):
    # initial vcs and semi-vcs as two empty dictionaries
    vcs = {}
    svcs = {}
    # we only care about the given color, so we only go through empty and same color stones
    # use find_stones to find all empty and colored blocks
    stones = find_stones(board, color)
    optm = Hex.oppCH(color)
    for stone1, stone2 in combinations(stones, 2):
        end1, end2 = str([stone1]), str([stone2])
        vcs[end1 + end2] = set()
        svcs[end1 + end2] = set()
        vcs[end2 + end1] = set()
        svcs[end2 + end1] = set()
    stones.pop()
    stones.pop()
    # every nbrs of an empty or colored block, there is a vc
    for i in stones:
        # if k is empty in the board, go through its nbrs
        for k in Hex.NBRS[i]:
            if board[k] != optm:
                end1, end2 = str([i]), str([k])
                vc = VC([i], [k], set(), "s")
                vcs[end1 + end2].add(vc)
                hashstring = vc_hash(False, end1, end2, '')
                hashtable.add(hashstring)
    if color == Hex.BCH:
        for i in Hex.TOP_ROW:
            if board[i] != optm:
                end1, end2 = str([i]), str([-4])
                vc = VC([i], [-4], set(), "s")
                vcs[end1 + end2].add(vc)
                hashstring = vc_hash(False, end1, end2, '')
                hashtable.add(hashstring)
                vc = VC([-4], [i], set(), "s")
                vcs[end2 + end1].add(vc)
                hashstring = vc_hash(False, end2, end1, '')
                hashtable.add(hashstring)
        for i in Hex.BTM_ROW:
            if board[i] != optm:
                end1, end2 = str([i]), str([-2])
                vc = VC([i], [-2], set(), "s")
                vcs[end1 + end2].add(vc)
                hashstring = vc_hash(False, end1, end2, '')
                hashtable.add(hashstring)
                vc = VC([-2], [i], set(), "s")
                vcs[end2 + end1].add(vc)
                hashstring = vc_hash(False, end2, end1, '')
                hashtable.add(hashstring)
    elif color == Hex.WCH:
        for i in Hex.LFT_COL:
            if board[i] != optm:
                end1, end2 = str([i]), str([-1])
                vc = VC([i], [-1], set(), "s")
                vcs[end1 + end2].add(vc)
                hashstring = vc_hash(False, end1, end2, '')
                hashtable.add(hashstring)
                vc = VC([-1], [i], set(), "s")
                vcs[end2 + end1].add(vc)
                hashstring = vc_hash(False, end2, end1, '')
                hashtable.add(hashstring)
        for i in Hex.RGT_COL:
            if board[i] != optm:
                end1, end2 = str([i]), str([-3])
                vc = VC([i], [-3], set(), "s")
                vcs[end1 + end2].add(vc)
                hashstring = vc_hash(False, end1, end2, '')
                hashtable.add(hashstring)
                vc = VC([-3], [i], set(), "s")
                vcs[end2 + end1].add(vc)
                hashstring = vc_hash(False, end2, end1, '')
                hashtable.add(hashstring)
    return vcs, svcs,hashtable

def hsearch(board, color,turn,opt = 0):
    hashtable = set()
    vcs, svcs,hashtable = start(board, hashtable, color)
    changes = True
    optm = Hex.oppCH(color)
    colornumber = Hex.PTS.index(color)
    # stones and blocks we need to go through
    stones = find_stones(board, color)
    colornumber = Hex.PTS.index(color)
    top1 = [S[colornumber-1][0]]
    bot1 = [S[colornumber-1][1]]
    #[k1, k2] = listsort([top1, bot1])
    k1, k2 = str(top1), str(bot1)
    keylist = [k1+k2,k2+k1]
    while changes:
        new_vcs, new_svcs = all_new_empty(stones)
        changes = False
        #find if there are any vcs/svcs from g1 to g2 though midstone
        for midstone in stones:
            for g1, g2 in combinations(stones, 2):
                if g1 == midstone or g2 == midstone or midstone in S[colornumber-1]:
                    continue
                #[midkey, end1, end2] = listsort([midstone, g1, g2])
                midkey, end1, end2 = str([midstone]), str([g1]), str([g2])
                if board[midstone] != Hex.ECH:
                    # If stone is black then, additionally, g1 and g2 should be both empty
                    '''if board[g1] == optm or board[g2] == optm:
                        continue'''
                        # find the vcs that from g1 to midstone and vcs from g2 to midstone
                    C1s = vcs[end1 + midkey]
                    C2s = vcs[end2 + midkey]
                    # loop over every pair of vc in two vcs
                    for c1 in C1s:
                        for c2 in C2s:
                            # if the intersection of two vc carriers is 0, and the ends of the vc do not
                            # intersect each other's carrier
                            # then it forms a new vc from end1 to end2 through midstone
                            if len(set(c1.end1).intersection(c2.carrier)) != 0 or len(set(c2.end1).intersection(c1.carrier)) != 0 or len(c1.carrier.intersection(c2.carrier)) != 0:
                                continue
                            new_carrier = c1.carrier.union(c2.carrier)
                            # if the new carrier is not the superset of any existing carrier
                            if is_subset(vcs[end1 + end2], new_carrier) or is_subset(vcs[end2 + end1], new_carrier):
                                continue
                            hashstring = vc_hash(False, end1, end2, new_carrier)
                            hashstring2 = vc_hash(False, end2, end1, new_carrier)
                            # if not already seen, add to the new_vcs
                            if hashstring not in hashtable:
                                vc = VC(c1.end1, c2.end1, new_carrier, "a")
                                vc2 = VC(c2.end1, c1.end1, new_carrier, "a")
                                new_vcs[end1 + end2].add(vc)
                                new_vcs[end2 + end1].add(vc2)
                                hashtable.add(hashstring)
                                hashtable.add(hashstring2)
                                changes = True
                                if end1 + end2 in keylist:
                                    vcs[end1 + end2].add(vc)
                                    vcs[end2 + end1].add(vc2)
                                    return vcs, svcs,hashtable,True,True
                else:
                    # if empty stone forms a semi-vc instead of vc
                    C1s = vcs[end1 + midkey]
                    C2s = vcs[end2 + midkey]
                    update = False
                    if len(vcs[end1 + end2]) != 0:
                            continue
                    for c1 in C1s:
                        for c2 in C2s:
                            # if the intersection of two vc carriers is 0, and the ends of the vc do not
                            # intersect each other's carrier
                            # then it forms a new svc from end1 to end2 through midstone
                            if len(set(c1.end1).intersection(c2.carrier)) != 0 or len(set(c2.end1).intersection(c1.carrier)) != 0 or len(c1.carrier.intersection(c2.carrier)) != 0:
                                continue
                            new_semin_carrier = c1.carrier.union(c2.carrier.union({midstone}))
                            # if the new carrier is not the superset of any existing carrier
                            if is_subset(svcs[end1 + end2], new_semin_carrier) or is_subset(svcs[end2 + end1], new_semin_carrier):
                                continue
                            hashstring = vc_hash(True, end1, end2, new_semin_carrier)
                            hashstring2 = vc_hash(True, end2, end1, new_semin_carrier)
                            if hashstring not in hashtable:
                                svc = SVC(c1.end1, c2.end1, new_semin_carrier,midstone)
                                svc.v1,svc.v2 = c1,c2
                                svc2 = SVC(c2.end1, c1.end1, new_semin_carrier,midstone)
                                svc.v1,svc.v2 = c1,c2
                                svcs[end1 + end2].add(svc)
                                svcs[end2 + end1].add(svc2)
                                hashtable.add(hashstring)
                                hashtable.add(hashstring2)
                                changes = True
                                update = True
                                if end1 + end2 in keylist and turn:
                                    return vcs, svcs,hashtable,False,True
                            if update:
                                new_sc_set = svcs[end1 + end2]
                                OR_RULE_three(new_vcs[end1 + end2], new_vcs[end2 + end1], new_sc_set, hashtable, vcs[end1 + end2])
                                if len(new_vcs[keylist[0]])>0 or len(new_vcs[keylist[1]])>0:
                                    for k, v in new_vcs.items():
                                        if len(v) != 0:
                                            for vc in v:
                                                vcs[k].add(vc)
                                    return vcs, svcs,hashtable,True,True
        for k, v in new_vcs.items():
            if len(v) != 0:
                for vc in v:
                    vcs[k].add(vc)
        for k, v in new_svcs.items():
            if len(v) != 0:
                for vc in v:
                    svcs[k].add(vc)
        if turn:
            if len(svcs[keylist[0]])>0 or len(svcs[keylist[1]])>0 or len(vcs[keylist[0]])>0 or len(vcs[keylist[1]])>0:
                #print(2)
                return vcs, svcs,hashtable,False,True
        else:
            if len(vcs[keylist[0]])>0 or len(vcs[keylist[1]])>0:
                #print(1)
                return vcs, svcs,hashtable,True,True
        vcs = remove_subset(vcs)
        svcs = remove_subset(svcs)
        if opt != 0:
            optmzation(opt,vcs,svcs)
    vcs = remove_subset(vcs)
    svcs = remove_subset(svcs)
    return vcs, svcs, hashtable,False,False

def OR_RULE_two(vcs, vcs2, sc_set, hashtable, current_vcs):
    #loop over all pairs of svcs, see if there is a vc formed
    for semi,semi2 in combinations(sc_set, 2):
        i1 = semi2.carrier.intersection(semi.carrier)
        u1 = semi2.carrier.union(semi.carrier)
        # if the intersection is 0, then it means there is a vc formed
        if len(i1) != 0:
            continue
        if is_subset(current_vcs, u1):
            continue
        hashstring = vc_hash(False, semi.end1, semi.end2, u1)
        hashstring2 = vc_hash(False, semi.end2, semi.end1, u1)
        if hashstring not in hashtable:
            vc = VC(semi.end1, semi.end2, u1, "o")
            vc.c1 = semi.carrier
            vc.c2 = semi2.carrier
            vc2 = VC(semi.end2, semi.end1, u1, "o")
            vc2.c1 = semi.carrier
            vc2.c2 = semi2.carrier
            vcs.add(vc)
            vcs2.add(vc2)
            hashtable.add(hashstring)
            hashtable.add(hashstring2)

def OR_RULE_three(vcs, vcs2, sc_set, hashtable, current_vcs):
    #loop over all pairs of svcs, see if there is a vc formed
    for semi,semi2 in combinations(sc_set, 2):
        if semi.carrier == semi2.carrier:
            continue
        i1 = semi2.carrier.intersection(semi.carrier)
        u1 = semi2.carrier.union(semi.carrier)
        # if the intersection is 0, then it means there is a vc formed
        if len(i1) == 0:
            if is_subset(current_vcs, u1):
                continue
            hashstring = vc_hash(False, semi.end1, semi.end2, u1)
            hashstring2 = vc_hash(False, semi.end2, semi.end1, u1)
            if hashstring not in hashtable:
                vc = VC(semi.end1, semi.end2, u1, "o")
                vc.c1 = semi.carrier
                vc.c2 = semi2.carrier
                vc2 = VC(semi.end2, semi.end1, u1, "o")
                vc2.c1 = semi.carrier
                vc2.c2 = semi2.carrier
                vcs.add(vc)
                vcs2.add(vc2)
                hashtable.add(hashstring)
                hashtable.add(hashstring2)
        else:
            for semi3 in sc_set:
                if semi3.carrier == semi2.carrier or semi3.carrier == semi.carrier:
                    continue
                i2 = semi3.carrier.intersection(i1)
                if len(i2) != 0:
                    continue
                u2 = semi3.carrier.union(u1)
                if is_subset(current_vcs, u1):
                    continue
                hashstring = vc_hash(False, semi.end1, semi.end2, u2)
                hashstring2 = vc_hash(False, semi.end2, semi.end1, u2)
                if hashstring not in hashtable:
                    vc = VC(semi.end1, semi.end2, u2, "o")
                    vc.c1 = semi.carrier
                    vc.c2 = semi2.carrier
                    vc.c3 = semi3.carrier
                    vc2 = VC(semi.end2, semi.end1, u2, "o")
                    vc2.c1 = semi.carrier
                    vc2.c2 = semi2.carrier
                    vc2.c3 = semi3.carrier
                    vcs.add(vc)
                    vcs2.add(vc2)
                    hashtable.add(hashstring)
                    hashtable.add(hashstring2)

def all_new_empty(stones):
    vcs = {}
    svcs = {}
    for stone1 in stones:
        for stone2 in stones:
            if stone1 != stone2:
                #[end1, end2] = listsort([stone1, stone2])
                end1, end2 = str([stone1]), str([stone2])
                vcs[end1 + end2] = set()
                svcs[end1 + end2] = set()
    return vcs, svcs


def find_stones(board, color):
    # find all empty stones and colored blocks
    moves = []
    optm = Hex.oppCH(color)
    for k in Hex.CELLS:
        if board[k]!=optm:
            moves.append(k)
    if color == Hex.BCH:
        moves.append(-4)
        moves.append(-2)
    elif color == Hex.WCH:
        moves.append(-1)
        moves.append(-3)
    return moves

def optmzation(typ,vcs,svcs):
    if typ == 1:
        remove_svcs(vcs,svcs)

def remove_svcs(vcs,svcs):
    for k, v in vcs.items():
        if len(v)>0:
            svcs[k] = set()

def mustplay_zone(board,vcs,svcs,color):
    u = set()
    init = 0
    colornumber = Hex.PTS.index(color)
    top1 = [S[colornumber-1][0]]
    bot1 = [S[colornumber-1][1]]
    #[k1, k2] = listsort([top1, bot1])
    k1, k2 = str(top1), str(bot1)
    keylist = [k1+k2,k2+k1]
    for key in keylist:
        if len(svcs[key])>0:
            for i in svcs[key]:
                if init == 0:
                    u = i.carrier
                    init = 1
                else:
                    u = u.intersection(i.carrier)
            if len(u) == 0:
                return "nowin"
        break
    return u

def distanceB(board,stone,dirc):
    if dirc == 0:
        score = Hex.DIS_TOP[stone]
    elif dirc == 1:
        score = Hex.DIS_BTM[stone]
    return score

def distanceW(board,stone,dirc):
    if dirc == 0:
        score = Hex.DIS_LFT[stone]
    elif dirc == 1:
        score = Hex.DIS_RGT[stone]
    return score
SCORE = [distanceB,distanceW]

def mustplay_order(cellist,board,vcs,svcs,color):
    newlist = []
    colornumber = Hex.PTS.index(color)
    top1 = [S[colornumber-1][0]]
    bot1 = [S[colornumber-1][1]]
    #[k1, k2] = listsort([top1, bot1])
    k1, k2 = str(top1), str(bot1)
    #print(cellist,"cellist")
    for cell in cellist:
        if board[cell] != Hex.ECH:
            continue
        score1 = 0
        score2 = 0
        #[end1, end2] = listsort([[cell], block1])
        end1, end2 = str([cell]), k1
        key1 = end1+end2
        #[end1, end2] = listsort([[cell], block2])
        end1, end2 = str([cell]), k2
        key2 = end1+end2
        if len(vcs[key1]) >0:
            score1 = SCORE[colornumber-1](board,cell,0)
            if len(svcs[key2]) >0:
                score1+= len(svcs[key2])*0.5
        if len(vcs[key2]) >0:
            score2 = SCORE[colornumber-1](board,cell,1)
            if len(svcs[key1]) >0:
                score2+= len(svcs[key1])*0.5
        score = max(score1,score2)
        newlist.append((cell,score))
    newlist = Fill_in.center_weight(newlist,Hex.ROWS,Hex.COLS)
    newlist.sort(key=lambda a:a[-1],reverse=True)
    movelist =[]
    slist  = []
    #print(newlist)
    for e in newlist:
        if e[0] not in movelist:
            movelist.append(e[0])
            slist.append(e[-1])
    return movelist,slist

'''p = Hex.Position(6, 6)
#p.change_str(20, Hex.BCH)
t = time.time()
vcs, svcs,hash = hsearch(p.brd, Hex.BCH, 1, 1)'''
'''print("VCS:")
for k, v in svcs.items():
    if "-4" in k or "-2" in k:
        print(k)
        for i in v:
            i.print()'''
'''Hex.showboard(p.brd, 6, 6)
mustplay = mustplay_zone(p.brd,vcs,svcs,Hex.BCH)
mustplay = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35}
s1,s2 = mustplay_order(mustplay,p.brd,vcs,svcs,Hex.BCH)
print("mustplay:", mustplay)
print("mustplay order:", s1)
print("mustplay order:", s2)
print("time taken:", time.time()-t)'''