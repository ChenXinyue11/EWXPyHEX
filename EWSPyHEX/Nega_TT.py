import Hex,TT,time
def negamx(s,ptm,tt,start,timelimit = 1000 ): # assume neither player has won yet
  if time.time() - start > timelimit:
    return None, 0 , None
  optm = Hex.oppCH(ptm)
  result = tt.lookup(s)
  if result != None:
    if result == optm:
      return False, 0 , None
    elif result == ptm:
      return True, 0 , None
  if Hex.has_win(s, optm):
        tt.store(s, optm)
        return False, 0 , None
  calls = 1
  for k in Hex.CELLS:
    if s[k]==Hex.ECH:
      t = Hex.change_str(s, k, ptm)
      cw, prev_calls,_ = negamx(t, optm,tt,start,timelimit)
      calls += prev_calls
      if cw == None:
        return None, calls , None
      if cw == False:
        tt.store(s, ptm)
        return True, calls,k
  tt.store(s, optm)
  return False, calls, None

'''t = time.time()
p = Hex.Position(4, 4)
tt = TT.TranspositionTable()
print(negamx(p.brd, Hex.BCH, tt,t, 1))
print('Time taken:', time.time()-t)'''