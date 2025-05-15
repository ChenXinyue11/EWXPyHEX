import Hex
import time
def negamx(s, ptm,start,timelimit = 1000): # assume neither player has won yet
  if time.time() - start > timelimit:
    return None, 0 , None
  optm = Hex.oppCH(ptm)
  if Hex.has_win(s, optm):
        return False, 0 , None
  calls = 1
  for k in Hex.CELLS:
    if s[k]==Hex.ECH:
      t = Hex.change_str(s, k, ptm)
      cw, prev_calls,_ = negamx(t, optm,start,timelimit)
      calls += prev_calls
      if cw == None:
        return None, calls , None
      if cw == False:
        return True, calls,k
  return False, calls, None

'''p = Hex.Position(4, 4)
print(negamx(p.brd, Hex.BCH, time.time(), 5))'''