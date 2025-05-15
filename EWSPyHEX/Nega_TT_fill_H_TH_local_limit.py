import Hex,TT,time
import Fill_in,Fill_in_Nega
import H_local_limit as nb
def negamx(s,ptm,tt): # assume neither player has won yet
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
      cw, prev_calls,_ = negamx(t, optm,tt)
      calls += prev_calls
      if cw == False:
        tt.store(s, ptm)
        return True, calls,k
  tt.store(s, optm)
  return False, calls, None

def negamx_2(board,ptm,tt,th,start,timelimit = 1000): # assume neither player has won yet
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
  mustplay = []
  reslt = th.lookup(board.brd)
  if reslt != None:
    op_win,player_win,mustplay = reslt[0],reslt[1],reslt[2]
    if op_win:
        tt.store(board.brd, optm)
        return False, 0 , None
    elif player_win:
        tt.store(board.brd, ptm)
        return True, 0 , None
    else:
        calls = 1
        move_list = mustplay
  else:
    calls = 1
    captured = Fill_in.capture(board,ptm)
    Ovcs, Osvcs,_,Ovw,Osw = nb.hsearch(board.brd,optm,False,0)
    if Ovw == True:
        tt.store(board.brd, optm)
        return False, 0 , None
    pvcs, psvcs,_,pvw,psw = nb.hsearch(board.brd,ptm,True,0)
    if psw == True:
        tt.store(board.brd, ptm)
        return True, 0 , None
    move_list = []
    mustplay = nb.mustplay_zone(board.brd,Ovcs,Osvcs,optm)
    if mustplay == "nowin":
        tt.store(board.brd, optm)
        return False, 0 , None
    elif len(mustplay) == 0:
        for k in Hex.CELLS:
            if board.brd[k]==Hex.ECH and k not in captured:
                move_list.append(k)
    else:
        for k in mustplay:
            if board.brd[k]==Hex.ECH and k not in captured:
                move_list.append(k)
    #move_list,slist = nb.mustplay_order(move_list,board.brd,pvcs,psvcs,ptm)
    th.store(board.brd,[False,False,move_list])
  for k in move_list:
    board.change_str(k, ptm)
    cw, prev_calls,_ = negamx_2(board, optm,tt,th,start,timelimit)
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
p = Hex.Position(6, 6)
p.change_str(15,Hex.BCH)
Hex.showboard(p.brd, Hex.ROWS, Hex.COLS)
tt = TT.TranspositionTable()
th = TT.TranspositionConnection()
vcs, svcs,_,vw,sw = nb.hsearch(p.brd,Hex.BCH,True,1)
mustplay = nb.mustplay_zone(p.brd,vcs,svcs,Hex.BCH)
print('mustplay:', mustplay)
print(negamx_2(p, Hex.WCH, tt,th,t, 1))
print('Time taken:', time.time()-t)'''
