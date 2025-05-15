import Hex
from itertools import combinations
import time
import cProfile
import pstats
SEMI = 0
NON_SEMI = 1
B,W,EMP = 0,1,2
b,w,emp = 0,1,2
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


'''def find_block(board, stone, blocks):
    # if colored stones, return its block
    # if empty, the block only contains the empty stone
    if Pt.point_color(board.stones, stone) == EMP:
        return [stone]
    for block in blocks:
        if stone in block:
            b = list(block)
            b.sort()
            return b
    return [stone]'''


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
    blocks = board.get_blocks(color)
    stones = find_stones(board, color)
    #print(stones)
    #print(color)
    for stone1 in stones:
        for stone2 in stones:
            if stone1 != stone2:
                #[end1, end2] = listsort([stone1, stone2])
                end1, end2 = str(stone1), str(stone2)
                vcs[end1 + end2] = set()
                svcs[end1 + end2] = set()
    # every nbrs of an empty or colored block, there is a vc
    for k, v in board.nbrs.items():
        k_block = find_block(board, k, blocks)
        # if k is empty in the board, go through its nbrs
        if Pt.point_color(board.stones, k) == EMP:
            for stone in v:
                if Pt.point_color(board.stones, stone) != (1 - color):
                    # add vc if the nbr is not the opposite color
                    stone_block = find_block(board, stone, blocks)
                    #[end1, end2] = listsort([k_block, stone_block])
                    end1, end2 = str(k_block), str(stone_block)
                    if not is_subset(vcs[end1 + end2], set()):
                        vc = VC(k_block, stone_block, set(), "s")
                        vcs[end1 + end2].add(vc)
                        hashstring = vc_hash(False, end1, end2, '')
                        hashtable.add(hashstring)
        # if k is colored stone, go through its nbrs
        elif Pt.point_color(board.stones, k) == color:
            for stone in v:
                if Pt.point_color(board.stones, stone) == EMP :
                    # same color nbr are in the same block
                    # blocks are treated as a single stone so no need to put into vc
                    # only cares about empty stone
                    stone_block = find_block(board, stone, blocks)
                    #[end1, end2] = listsort([k_block, stone_block])
                    end1, end2 = str(k_block), str(stone_block)
                    hashstring = vc_hash(False, end1, end2, '')
                    # check if other stone in blocks already formed a vc with the empty stone
                    if hashstring not in hashtable:
                        vc = VC(k_block, stone_block, set(), "s")
                        vcs[end1 + end2].add(vc)
                        hashtable.add(hashstring)
    return vcs, svcs


def find_stones(board, color):
    # find all empty stones and colored blocks
    moves = []
    optm = Hex.oppCH(color)
    for k in Hex.CELLS:
        if board[k]!=optm:
            moves.append(k)
    return moves



def all_new_empty(stones):
    vcs = {}
    svcs = {}
    for stone1 in stones:
        for stone2 in stones:
            if stone1 != stone2:
                #[end1, end2] = listsort([stone1, stone2])
                end1, end2 = str(stone1), str(stone2)
                vcs[end1 + end2] = set()
                svcs[end1 + end2] = set()
    return vcs, svcs


def hsearch(board, color,turn,opt = 0):
    opt = 0
    hashtable = set()
    vcs, svcs = start(board, hashtable, color)
    changes = True
    # stones and blocks we need to go through
    stones = find_stones(board, color)
    while changes:
        new_vcs, new_svcs = all_new_empty(stones)
        changes = False
        #find if there are any vcs/svcs from g1 to g2 though midstone
        for midstone in stones:
            for g1 in stones:
                for g2 in stones:
                    if g1 == midstone or g2 == midstone or g1 == g2 or list(midstone)[0] in BRD[color]:
                        continue
                    #[midkey, end1, end2] = listsort([midstone, g1, g2])
                    midkey, end1, end2 = str(midstone), str(g1), str(g2)
                    if Pt.point_color(board.stones, list(midstone)[0]) != EMP:
                        # If stone is black then, additionally, g1 and g2 should be both empty
                        if Pt.point_color(board.stones, list(g1)[0]) == Cell.opponent(color) or Pt.point_color(board.stones,list(g2)[0]) == Cell.opponent(color):
                            continue
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
                    else:
                        # if empty stone forms a semi-vc instead of vc
                        C1s = vcs[end1 + midkey]
                        C2s = vcs[end2 + midkey]




                        update = False
                        for c1 in C1s:
                            for c2 in C2s:
                                # if the intersection of two vc carriers is 0, and the ends of the vc do not
                                # intersect each other's carrier
                                # then it forms a new svc from end1 to end2 through midstone
                                if len(set(c1.end1).intersection(c2.carrier)) != 0 or len(set(c2.end1).intersection(c1.carrier)) != 0 or len(c1.carrier.intersection(c2.carrier)) != 0:
                                    continue
                                new_semin_carrier = c1.carrier.union(c2.carrier.union(set(midstone)))
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
                                if update:
                                    new_sc_set = svcs[end1 + end2]
                                    OR_RULE_three(new_vcs[end1 + end2], new_vcs[end2 + end1], new_sc_set, new_semin_carrier, new_semin_carrier, hashtable, vcs[end1 + end2])
        for k, v in new_vcs.items():
            if len(v) != 0:
                for vc in v:
                    vcs[k].add(vc)
        for k, v in new_svcs.items():
            if len(v) != 0:
                for vc in v:
                    svcs[k].add(vc)
        vcs = remove_subset(vcs)
        svcs = remove_subset(svcs)
        if opt != 0:
            optmzation(opt,vcs,svcs)
    vcs = remove_subset(vcs)
    svcs = remove_subset(svcs)
    return vcs, svcs, hashtable


def OR_RULE(vcs, vcs2, sc_set, uni, inters, hashtable, current_vcs):
    # from the current svcs set, remove one svc at a time, to two, three ...
    # loop over all possible combination
    for semi in sc_set:
        u1 = uni.union(semi.carrier)
        i1 = inters.intersection(semi.carrier)
        # if the intersection is 0, then it means there is a vc formed
        if len(i1) == 0:
            if not is_subset(current_vcs, u1):
                hashstring = vc_hash(False, semi.end1, semi.end2, u1)
                hashstring2 = vc_hash(False, semi.end2, semi.end1, u1)
                if hashstring not in hashtable:
                    vc = VC(semi.end1, semi.end2, u1, "o")
                    vc2 = VC(semi.end2, semi.end1, u1, "o")
                    vcs.add(vc)
                    vcs2.add(vc2)
                    hashtable.add(hashstring)
                    hashtable.add(hashstring2)
        else:
            new_sc_set = sc_set - {semi}
            OR_RULE(vcs, vcs2, new_sc_set, u1, i1, hashtable, current_vcs)


def OR_RULE_two(vcs, vcs2, sc_set, uni, inters, hashtable, current_vcs):
    #loop over all pairs of svcs, see if there is a vc formed
    for semi in sc_set:
        for semi2 in sc_set:
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

def OR_RULE_three(vcs, vcs2, sc_set, uni, inters, hashtable, current_vcs):
    #loop over all pairs of svcs, see if there is a vc formed
    for semi in sc_set:
        for semi2 in sc_set:
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
                    u1 = semi3.carrier.union(u1)
                    if len(i2) != 0:
                        continue
                    if is_subset(current_vcs, u1):
                        continue
                    hashstring = vc_hash(False, semi.end1, semi.end2, u1)
                    hashstring2 = vc_hash(False, semi.end2, semi.end1, u1)
                    if hashstring not in hashtable:
                        vc = VC(semi.end1, semi.end2, u1, "o")
                        vc.c1 = semi.carrier
                        vc.c2 = semi2.carrier
                        vc.c3 = semi3.carrier
                        vc2 = VC(semi.end2, semi.end1, u1, "o")
                        vc2.c1 = semi.carrier
                        vc2.c2 = semi2.carrier
                        vc2.c3 = semi3.carrier
                        vcs.add(vc)
                        vcs2.add(vc2)
                        hashtable.add(hashstring)
                        hashtable.add(hashstring2)


def distanceB(board,stones,dirc):
    if dirc == 0:
        score = max(stones[0]//board.c+1,stones[-1]//board.c+1)
    elif dirc == 1:
        score = max(board.r - stones[0]//board.c,board.r - stones[-1]//board.c)
    return score

def distanceW(board,stones,dirc):
    if dirc == 0:
        score = max(stones[0]%board.c+1,stones[-1]%board.c+1)
    elif dirc == 1:
        score = max(board.c - stones[0]%board.c,board.c - stones[-1]%board.c)
    return score
SCORE = [distanceB,distanceW]

def mustplay_zone(board,vcs,svcs,color):
    u = set()
    init = 0
    for k,v in svcs.items():
        #print(k,v)
        if side[color][0] in k and side[color][1] in k and len(svcs[k])>0:
            
            for i in v:
                if init == 0 :
                    u = i.carrier
                    init = 1
                else:
                    u = u.intersection(i.carrier)
                #i.print()
            break
    blocks = board.get_blocks_list(color)
    block1 = None
    block2 = None
    for block in blocks:
        if S[color][0] in block:
            block1 = block
        if S[color][1] in block:
            block2 = block
    blocks.remove(block1)
    blocks.remove(block2)
    vcs_point = set()
    for block in blocks:
        #[end1, end2] = listsort([block, block1])
        end1, end2 = str(block), str(block1)
        key1 = end1+end2
        #[end1, end2] = listsort([block, block2])
        end1, end2 = str(block), str(block2)
        key2 = end1+end2
        if len(vcs[key1])>0 and len(svcs[key2])>0:
            for e in vcs[key1]:
                for j in svcs[key2]:
                    if len(e.carrier.intersection(j.carrier)) == 0:
                        vcs_point = vcs_point.union(e.carrier)
        if len(vcs[key2])>0 and len(svcs[key1])>0:
            for e in vcs[key2]:
                for j in svcs[key1]:
                    if len(e.carrier.intersection(j.carrier)) == 0:
                        vcs_point = vcs_point.union(e.carrier)
    mustplay = u - vcs_point
    #print("must",mustplay)
    return mustplay
def mustplay_zone_2(board,vcs,svcs,color):
    u = set()
    init = 0
    for k,v in svcs.items():
        #print(k,v)
        if side[color][0] in k and side[color][1] in k and len(svcs[k])>0:
            
            for i in v:
                if init == 0 :
                    u = i.carrier
                    init = 1
                else:
                    u = u.intersection(i.carrier)
                #i.print()
            if len(u) == 0:
                return "nowin"
            break
    return u
    blocks = board.get_blocks_list(color)
    block1 = None
    block2 = None
    for block in blocks:
        if S[color][0] in block:
            block1 = block
        if S[color][1] in block:
            block2 = block
    blocks.remove(block1)
    blocks.remove(block2)
    vcs_point = set()
    for block in blocks:
        #[end1, end2] = listsort([block, block1])
        end1, end2 = str(block), str(block1)
        key1 = end1+end2
        #[end1, end2] = listsort([block, block2])
        end1, end2 = str(block), str(block2)
        key2 = end1+end2
        if len(vcs[key1])>0 and len(svcs[key2])>0:
            for e in vcs[key1]:
                for j in svcs[key2]:
                    if len(e.carrier.intersection(j.carrier)) == 0:
                        vcs_point = vcs_point.union(e.carrier)
        if len(vcs[key2])>0 and len(svcs[key1])>0:
            for e in vcs[key2]:
                for j in svcs[key1]:
                    if len(e.carrier.intersection(j.carrier)) == 0:
                        vcs_point = vcs_point.union(e.carrier)
    mustplay2 = u - vcs_point
    if len(mustplay2) == 0:
        return u
    else:
        return mustplay2

    #print("must",mustplay)
    return mustplay
def move_scoring(board,svcs,vcs,color):
    lis = []
    for k,v in vcs.items():
        l1 = 200
        l2 = 200
        cells = None
        if side[color][0] in k and len(vcs[k])>0:
            lv = list(v) 
            if Pt.point_color(board.stones, list(lv[0].end1)[0]) != EMP and  Pt.point_color(board.stones, list(lv[0].end2)[0]) != EMP:
                continue
            #print(k,v)
            if S[color][0] not in lv[0].end1:
                stones = list(lv[0].end1)
                stones.sort()
                l1 = SCORE[color](board,stones,0)
                cells = lv[0].end1
                s = score_svcs(board,svcs,lv[0].end1,color,0)
                l1+=s
            else:
                stones = list(lv[0].end2)
                stones.sort()
                l1 = SCORE[color](board,stones,0)
                cells = lv[0].end2
                s = score_svcs(board,svcs,lv[0].end2,color,0)
                l1+=s
        if side[color][1] in k and len(vcs[k])>0:
            lv = list(v)
            if Pt.point_color(board.stones, list(lv[0].end1)[0]) != EMP and  Pt.point_color(board.stones, list(lv[0].end2)[0]) != EMP:
                continue
            #print(k,v)
            #print(v[0].end1) 
            if S[color][1] not in lv[0].end1:
                stones = list(lv[0].end1)
                stones.sort()
                l2 = SCORE[color](board,stones,1)
                cells = lv[0].end1
                s = score_svcs(board,svcs,lv[0].end1,color,1)
                l2+=s
            else:
                stones = list(lv[0].end2)
                stones.sort()
                l2 = SCORE[color](board,stones,1)
                cells = lv[0].end2
                s =score_svcs(board,svcs,lv[0].end2,color,1)
                l2+=s
        l = min(l2,l1)
        #print(l)
        if cells != None:
            lis.append((cells,l))
    #print(lis)
    lis = fillin.center_weight(lis,board.r,board.c)
    lis.sort(key=lambda a:a[-1],reverse=True)
    newlist = []
    for e in lis:
        m = list(e[0])[0]
        move = (m//board.c,m%board.c)
        if move not in newlist:
            newlist.append(move)
    for move in board.moves:
        if move not in newlist:
            newlist.append(move)
    return newlist
def score_svcs(board,svcs,end,color,s):
    #print("start svcs")
    score=0
    for k, v in svcs.items():
        lv = list(v)
        if side[color][1-s] in k  and len(svcs[k])>0:
            if list(end)[0] not in lv[0].end1 and list(end)[0] not in lv[0].end2:
                continue
            #print(str(list(end)))
            #board.print2(v[0],False)
            if S[color][1-s] not in lv[0].end1:
                stones = list(lv[0].end1)
                stones.sort()
                #score = max(stones[0]//board.c+1,stones[-1]//board.c+1)
                score = 3
                cells = lv[0].end1
                break
            else:
                stones = list(lv[0].end2)
                stones.sort()
                #score = max(stones[0]//board.c+1,stones[-1]//board.c+1)
                score = 3
                cells = lv[0].end2
                break
    return score

def mustplay_order(cellist,board,vcs,svcs,color):
    newlist = []
    blocks = board.get_blocks_list(color)
    block1 = None
    block2 = None
    for block in blocks:
        if S[color][0] in block:
            block1 = block
        if S[color][1] in block:
            block2 = block
    for cell in cellist:
        score1 = 0
        score2 = 0
        #[end1, end2] = listsort([[cell], block1])
        end1, end2 = str([cell]), str(block1)
        key1 = end1+end2
        #[end1, end2] = listsort([[cell], block2])
        end1, end2 = str([cell]), str(block2)
        key2 = end1+end2
        if len(vcs[key1]) >0:
            score1 = SCORE[color](board,[cell],0)
            if len(svcs[key2]) >0:
                score1+=2
        if len(vcs[key2]) >0:
            score2 = SCORE[color](board,[cell],1)
            if len(svcs[key1]) >0:
                score2+=2
        score = max(score1,score2)
        newlist.append(({cell},score))
    newlist.sort(key=lambda a:a[-1],reverse=True)
    movelist =[]
    #print(newlist)
    for e in newlist:
        m = list(e[0])[0]
        move = (m//board.c,m%board.c)
        if move not in movelist:
            movelist.append(move)
    return movelist

def countvcs(vcs,svcs):
    count = 0
    for k,v in vcs.items():
        count += len(v)
    for k,v in svcs.items():
        count += len(v)
    return count
def countsinglekeys(vcs,svcs):
    vc1 = {}
    svc1 = {}
    for k,v in vcs.items():
        vc1[k] = len(v)
    for k,v in svcs.items():
        svc1[k] = len(v)
    return vc1,svc1
def remove_svcs(vcs,svcs):
    for k, v in vcs.items():
        if len(v)>0:
            svcs[k] = set()
def remove_svcs_2(vcs,svcs):
    for k, v in vcs.items():
        area = set()
        for vc in v:
            area = vc.carrier.union(area)
        remove = set()
        for svc in svcs[k]:
            if svc.carrier.issubset(area):
                remove.add(svc)
        for r in remove:
            svcs[k].remove(r)

def optmzation(typ,vcs,svcs):
    if typ == 1:
        remove_svcs(vcs,svcs)
    elif typ == 2:
        remove_svcs_2(vcs,svcs)
def endend_check(vcs1,vcs2,file = None):
    diff1 = set(vcs1) - set(vcs2)
    diff2= set(vcs2) - set(vcs1)
    print("different in vcs1",diff1)
    print("different in vcs2",diff2)
    for k,v in vcs1.items():
        if k in diff1:
            print("this key only in vcs1",k)
            continue
        for vc in v:
            different = True
            for vc2 in vcs2[k]:
                if vc.carrier == vc2.carrier:
                    different = False
            if different == True:
                print("this vc is only in vcs1")
                vc.print()
                file.write("this vc is only in vcs1"+"\n")
                file.write(str(vc.end1)+str(vc.end2)+str(vc.carrier)+"\n")
    for k,v in vcs2.items():
        if k in diff2:
            print("this key only in vcs2",k)
            continue
        for vc in v:
            different = True
            for vc2 in vcs1[k]:
                if vc.carrier == vc2.carrier:
                    different = False
            if different == True:
                print("this vc is only in vcs2")
                vc.print()
                file.write("this vc is only in vcs2"+"\n")
                file.write(str(vc.end1)+str(vc.end2)+str(vc.carrier)+"\n")
    print("different in vcs1",diff1)
    print("different in vcs2",diff2)
    file.write("different in vcs1"+"\n")
    file.write(str(diff1)+"\n")
    file.write("different in vcs2"+"\n")
    file.write(str(diff2)+"\n")
#def print
'''b,w,emp = 0,1,2
hw1 = ((b,3,2),(w,2,2))
#hw1 = ((b,2,3),(b,3,2),(b,4,1),(b,5,1),(b,5,0),(w,0,4),(w,2,2))

hb = Stone_board(Game.hex_game, 6,6)
for move in hw1:
  hb.make_move(move)
hb.print()
vcs, svcs = hsearch(hb,B)
vcs2, svcs2 = hsearch(hb,W)
mustplay = mustplay_zone(hb,vcs,svcs,B)
mp = mustplay_order(mustplay,hb,vcs2,svcs2,W)
print("mm ",mp)


order = move_scoring(hb,svcs,vcs,B)   
print(order,len(order)) '''


    #e[1][0].print()
#print(svcs["[-2][-4]"])
'''for k, v in svcs.items():
    #print(k,v)
    #if side[b][0] in k and side[b][1] in k and len(vcs[k])>0:
    if side[b][0] in k:
        for e in v:
            e.print()
            if e.v1 != None:
                e.v1.print()
                e.v2.print()
            hb.print2(e,False)'''

'''print(hb.stones)
print(hb.get_blocks(B))
hb.print()
Pt.show_point_names(hb.game_type, hb.r, hb.c)'''
# strr = time.time()
# b,w,emp = 0,1,2
# hw1 = ((b,3,2),(B,2,3))
# #hw1 = ((b,2,3),(b,3,2),(b,4,1),(b,5,1),(b,5,0),(w,0,4),(w,2,2))

# hb = Stone_board(Game.hex_game, 6,6)
# for move in hw1:
#   hb.make_move(move)
# hb.print()
# vcs, svcs,_ = hsearch(hb,B,False)
# for k, v in svcs.items():
#     print(k,v)
#     for e in v:
#         e.print()
#vcs2, svcs2 = hsearch(hb,W)
#mustplay = mustplay_zone(hb,vcs,svcs,B)
#mp = mustplay_order(mustplay,hb,vcs2,svcs2,W)
#print("mm ",mp)


#order = move_scoring(hb,svcs,vcs,B)   
#print(order,len(order))


    #e[1][0].print()
#print(svcs["[-2][-4]"])
'''for k, v in svcs.items():
    #print(k,v)
    #if side[b][0] in k and side[b][1] in k and len(vcs[k])>0:
    if side[b][0] in k:
        for e in v:
            e.print()
            if e.v1 != None:
                e.v1.print()
                e.v2.print()
            hb.print2(e,False)'''

# print(hb.stones)
# print(hb.get_blocks(B))
# hb.print()
# Pt.show_point_names(hb.game_type, hb.r, hb.c)
# print(time.time()- strr)

'''lis= [ [(0, 4), (3, 1), (0, 3)], [(1, 5), (1, 2), (5, 5)], [(3, 0), (4, 1), (5, 4)], [(4, 4), (4, 5), (2, 1)], [(4, 0), (1, 2), (3, 1)], [(0, 0), (2, 1), (3, 5)], [(3, 4), (2, 2), (3, 3)], [(4, 3), (3, 4), (2, 3)], [(5, 4), (1, 5), (0, 0)], [(2, 0), (5, 1), (5, 3)], [(1, 0), (5, 2), (4, 0)], [(4, 0), (0, 5), (1, 3)], [(2, 3), (1, 5), (5, 2)], [(2, 0), (2, 5), (0, 5)], [(5, 5), (0, 1), (3, 3)], [(3, 3), (5, 1), (2, 5)], [(1, 2), (3, 4), (2, 5)], [(2, 3), (0, 2), (2, 1)], [(3, 5), (0, 0), (3, 1)], [(3, 0), (5, 3), (4, 4)], [(0, 1), (3, 5), (4, 2)], [(5, 4), (2, 1), (1, 3)], [(5, 4), (0, 0), (2, 5)], [(2, 5), (2, 2), (2, 3)], [(2, 0), (5, 3), (4, 2)], [(0, 4), (0, 0), (1, 3)], [(3, 4), (3, 5), (0, 3)], [(5, 2), 
(4, 5), (3, 4)], [(5, 4), (1, 1), (3, 0)], [(0, 5), (2, 3), (0, 3)], [(0, 0), (4, 5), (0, 1)], [(4, 5), (0, 3), (3, 4)], [(4, 0), (1, 2), (4, 3)], [(3, 4), (5, 0), (2, 5)], [(0, 0), (3, 4), (4, 5)], [(2, 0), (5, 5), (0, 0)], [(3, 4), (2, 1), (3, 
1)], [(0, 3), (5, 1), (0, 2)], [(5, 2), (5, 4), (3, 2)], [(4, 0), (4, 2), (1, 3)], [(3, 1), (5, 1), (1, 5)], [(0, 3), (1, 2), (4, 1)], [(4, 3), (1, 1), (5, 5)], [(4, 1), (1, 5), (4, 5)], [(0, 2), (3, 0), (2, 5)], [(5, 4), (2, 4), (5, 2)], [(5, 4), (5, 3), (0, 3)], [(3, 4), (2, 5), (5, 4)], [(1, 5), (2, 0), (4, 1)],[(2, 1), (2, 5), (0, 1)]]
stream = open('output.txt', 'w')
for m in lis:
    hb = Stone_board(Game.hex_game, 6,6)
    color = BLACK
    for j in m:
        hb.play((int(j[0]),int(j[1])))
    prof = cProfile.Profile()
    prof.run('hsearch(hb,B,False)')
    prof.dump_stats('output.prof')

    
    stats = pstats.Stats('output.prof', stream=stream)
    stats.sort_stats('cumtime')
    stats.print_stats()
stream.close()'''
# stt = time.time()
# b,w,emp = 0,1,2
# #hw1 = ((b,1,5),(w,1,4),(w,2,2),(w,4,4),(w,5,0),(w,5,1),(w,5,2),(w,5,3),(w,5,5),(b,2,1),(b,2,4),(b,3,5),(b,4,0),(b,4,1),(b,4,3),(b,4,5),(b,5,4),)
# #hw1 = ((b,2,3),(b,3,2),(b,4,1),(b,5,1),(b,5,0),(w,0,4),(w,2,2))
# hw1 = ((b,2,3),)
# hb = Stone_board(Game.hex_game, 6,6)
# for move in hw1:
#   hb.make_move(move)
# hb.print()
# #star = time.time()

# vcs, svcs,ht = hsearch(hb,B,True)
# print(time.time()-stt)
# for k, v in svcs.items():
#     print(k,v)
#     for e in v:
#         e.print()
