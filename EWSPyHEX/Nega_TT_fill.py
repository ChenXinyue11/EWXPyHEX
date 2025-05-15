import Hex,TT,time
import Fill_in,Fill_in_Nega
def negamx(s,ptm,tt,start, timelimit = 1000): # assume neither player has won yet
  if time.time() - start > timelimit:
    return None, 0 , None
  optm = Hex.oppCH(ptm)
  s = Fill_in_Nega.fillin(s)
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

def negamx_2(board,ptm,tt,start, timelimit = 1000): # assume neither player has won yet
  if time.time() - start > timelimit:
    return None, 0 , None
  optm = Hex.oppCH(ptm)
  Fill_in.fillin(board)
  result = tt.lookup(board.brd)
  if result != None:
    if result == optm:
      return False, 0 , None
    elif result == ptm:
      return True, 0 , None
  if Hex.has_win(board.brd, optm):
        tt.store(board.brd, optm)
        return False, 0 , None
  calls = 1
  captured = Fill_in.capture(board,ptm)
  for k in Hex.CELLS:
    if board.brd[k]==Hex.ECH and k not in captured:
      board.change_str(k, ptm)
      cw, prev_calls,_ = negamx_2(board, optm,tt,start,timelimit)
      calls += prev_calls
      board.undo()
      if cw == None:
        return None, calls , None
      if cw == False:
        tt.store(board.brd, ptm)
        return True, calls,k
  tt.store(board.brd, optm)
  return False, calls, None

'''t = time.time()
p = Hex.Position(5, 5)
p.change_str(6,Hex.BCH)
Fill_in.fillin(p)
Hex.showboard(p.brd, Hex.ROWS, Hex.COLS)
tt = TT.TranspositionTable()
print(negamx_2(p, Hex.WCH, tt,t, 1))
print('Time taken:', time.time()-t)'''
