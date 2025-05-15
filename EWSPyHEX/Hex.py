
import copy
from collections import deque
import time

PTS = '.xo'
EMPTY, BLACK, WHITE = 0, 1, 2
ECH, BCH, WCH = PTS[EMPTY], PTS[BLACK], PTS[WHITE]

def oppCH(ch): 
  if ch== BCH: return WCH
  elif ch== WCH: return BCH
  else: assert(False)

def coord_to_point(r, c, C): return c + r*C

def point_to_coord(p, C): return divmod(p, C)

def point_to_alphanum(p, C):
  r, c = point_to_coord(p, C)
  return 'abcdefghj'[c] + '1234566789'[r]

def change_str(s, where, what):
  return s[:where] + what + s[where+1:]

def char_to_color(c): 
  return PTS.index(c)

def undo(H, brd):  # pop last meta-move
  if len(H)==1:
    print('\n    original position,  nothing to undo\n')
    return brd
  else:
    H.pop()
    return copy.copy(H[len(H)-1])

def has_win(brd, who):
  set1, set2 = (TOP_ROW, BTM_ROW) if who == BCH else (LFT_COL, RGT_COL)
  #print('has_win', brd, who, set1, set2)
  Q, seen = deque([]), set()
  for c in set1:
    if brd[c] == who: 
      Q.append(c)
      seen.add(c)
  while len(Q) > 0:
    c = Q.popleft()
    if c in set2: 
      return True
    for d in NBRS[c]:
      if brd[d] == who and d not in seen:
        Q.append(d)
        seen.add(d)
  return False

def win_move(s, ptm): # assume neither player has won yet
  calls = 1
  optm = oppCH(ptm)
  for k in CELLS:
    if s[k]==ECH:
      t = change_str(s, k, ptm)
      if has_win(t, ptm):
        return point_to_alphanum(k, COLS), calls
      cw, prev_calls = win_move(t, optm)
      calls += prev_calls
      if not cw:
        return point_to_alphanum(k, COLS), calls
  return '', calls

def get_moves(s): # assume neither player has won yet
  moves = []
  for k in CELLS:
    if s[k]==ECH:
      moves.append(k)
  return moves
def negamx(s, ptm): # assume neither player has won yet
  optm = oppCH(ptm)
  if has_win(s, optm):
        return False, 0 , None
  calls = 1
  for k in CELLS:
    if s[k]==ECH:
      t = change_str(s, k, ptm)
      cw, prev_calls,_ = negamx(t, optm)
      calls += prev_calls
      if cw == False:
        return True, calls,k
  return False, calls, None

class Position: # hex board 
    def __init__(self, rows, cols):
        global CELLS,COLS,ROWS,N,NBRS,LFT_COL,RGT_COL,TOP_ROW,BTM_ROW,DIS_BTM,DIS_TOP,DIS_LFT,DIS_RGT
        self.R, self.C, self.n = rows, cols, rows*cols
        self.brd = PTS[EMPTY]*self.n
        self.history = []  # board positions
        self.history.append(self.brd)
        ROWS = rows
        COLS = cols
        N = rows * cols
        CELLS = range(N)
        NBRS = []
        for r in range(ROWS):
            for c in range(COLS):
                nbs = []
                if r > 0:                nbs.append(coord_to_point(r-1, c,   COLS))
                if r > 0 and c < COLS-1: nbs.append(coord_to_point(r-1, c+1, COLS))
                if c > 0:                nbs.append(coord_to_point(r,   c-1, COLS))
                if c < COLS-1:           nbs.append(coord_to_point(r,   c+1, COLS))
                if r < ROWS-1 and c > 0: nbs.append(coord_to_point(r+1, c-1, COLS))
                if r < ROWS-1:           nbs.append(coord_to_point(r+1, c, COLS))
                NBRS.append(nbs)
        
        LFT_COL, RGT_COL, TOP_ROW, BTM_ROW = set(), set(), set(), set()
        for r in range(ROWS):
            LFT_COL.add(coord_to_point(r, 0, COLS))
            RGT_COL.add(coord_to_point(r, COLS-1, COLS))
        for c in range(COLS):
            TOP_ROW.add(coord_to_point(0, c, COLS))
            BTM_ROW.add(coord_to_point(ROWS-1, c, COLS))
        
        DIS_TOP, DIS_BTM, DIS_LFT, DIS_RGT = [], [], [], []
        for cell in CELLS:
            r, c = point_to_coord(cell, COLS)
            DIS_TOP.append(abs(r))
            DIS_BTM.append(abs(ROWS-1-r))
            DIS_LFT.append(abs(c))
            DIS_RGT.append(abs(COLS-1-c))
    def undo(self):  # pop last meta-move
        if len(self.history)==1:
            print('\n    original position,  nothing to undo\n')
            return 
        else:
            self.brd = self.history.pop()
            return
    def change_str(self, where, what):
        self.history.append(self.brd)
        self.brd = self.brd[:where] + what + self.brd[where+1:]
        return
    def change_str_no_history(self, where, what):
        self.brd = self.brd[:where] + what + self.brd[where+1:]
        return
escape_ch           = '\033['
colorend, textcolor = escape_ch + '0m', escape_ch + '0;37m'
stonecolors         = (textcolor, escape_ch + '0;35m', escape_ch + '0;32m')
def showboard(brd, R, C):
  def paint(s):  # s   a string
    pt = ''
    for j in s:
      if j in PTS:      pt += stonecolors[PTS.find(j)] + j + colorend
      elif j.isalnum(): pt += textcolor + j + colorend
      else:             pt += j
    return pt

  pretty = '\n   ' 
  for c in range(C): # columns
    pretty += ' ' + paint(chr(ord('a')+c))
  pretty += '\n'
  for j in range(R): # rows
    pretty += ' ' + ' '*j + paint(str(1+j)) + ' '
    for k in range(C): # columns
      pretty += ' ' + paint([brd[coord_to_point(j,k,C)]])
    pretty += '\n'
  print(pretty)

def msg(s, ch):
  if has_win(s, 'x'): 
    return('x has won')
  elif has_win(s, 'o'): return('o has won')
  else: 
    start_time = time.time()
    wm, calls = win_move(s, ch)
    out = '\n' + ch + '-to-move: '
    out += (ch if wm else oppCH(ch)) + ' wins' 
    out += (' ... ' if wm else ' ') + wm + '\n'
    out += str(calls) + ' calls\n'
    out += format(time.time() - start_time, '.1f') + ' seconds\n'
    return out
  
def interact():
  p = Position(3, 3)
  history = []  # board positions
  new = copy.copy(p.brd); history.append(new)
  while True:
    showboard(p.brd, p.R, p.C)
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    elif cmd[0][0]=='u':
      p.brd = undo(history, p.brd)
      new = p.requestmove(cmd)
      if new != '':
        p.brd = new
        history.append(new)
    elif cmd[0][0]=='?':
      cmd = cmd.split()
      if len(cmd)>0:
        for ch in (BCH, WCH):
          if cmd[1][0]==ch: 
            print(msg(p.brd, ch))

#interact()
'''p = Position(3, 3)
showboard(p.brd, p.R, p.C)
print(DIS_BTM,DIS_TOP,DIS_LFT,DIS_RGT)'''