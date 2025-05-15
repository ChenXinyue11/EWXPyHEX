import numpy as np

class TranspositionTable(object):


    # Empty dictionary
    def __init__(self):

        self.table = {}

    # Used to print the whole table with print(tt)
    def __repr__(self):
        return self.table.__repr__()

    def store(self, brd, score):
        self.table[brd] = score

    # Python dictionary returns 'None' if key not found by get()
    def lookup(self, brd):
        return self.table.get(brd)

class TranspositionNode(object):


    # Empty dictionary
    def __init__(self):

        self.table = {}

    # Used to print the whole table with print(tt)
    def __repr__(self):
        return self.table.__repr__()

    def store(self, brd, lis):
        code = str(brd)
        self.table[code] = lis

    # Python dictionary returns 'None' if key not found by get()
    def lookup(self, brd):
        code = str(brd)
        return self.table.get(code)

class TranspositionConnection(object):


    # Empty dictionary
    # for each key, it stores a list of the form [player lose, player win, mustplay]
    def __init__(self):

        self.table = {}

    # Used to print the whole table with print(tt)
    def __repr__(self):
        return self.table.__repr__()

    def store(self, brd, lis):
        code = str(brd)
        self.table[code] = lis

    # Python dictionary returns 'None' if key not found by get()
    def lookup(self, brd):
        code = str(brd)
        return self.table.get(code)