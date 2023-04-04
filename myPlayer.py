# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
import random
from playerInterface import *
import numpy as np
from parce import pickOpening

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None
        self._opening = pickOpening() 
        self._decimalPoint = 0
        self._initialDepth = 2

    def getPlayerName(self):
        return "CSGO"
    
    def heuristic(self,depth):
        if (depth==0 or self._board.is_game_over()):
            self._decimalPoint+=0.000000000000001
            if self._mycolor==self._board._BLACK:
                return self._board._nbBLACK  + self._board._capturedWHITE + self._decimalPoint
            else:
                return self._board._nbWHITE + self._board._capturedBLACK + self._decimalPoint
        else:
             return "NO_LEAF"

    def maxAB(self,alpha,beta,depth):
        heuristicResult = self.heuristic(depth)
        if heuristicResult!="NO_LEAF":
            return heuristicResult
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            alpha = max(alpha,self.minAB(alpha,beta,depth-1))
            self._board.pop()
            if alpha >= beta:
                return beta
        return alpha
    
    def minAB(self,alpha,beta,depth):
        heuristicResult = self.heuristic(depth)
        if heuristicResult!="NO_LEAF":
            return heuristicResult
        moves = self._board.legal_moves()
        for move in moves:
            self._board.push(move)
            beta = min(beta,self.maxAB(alpha,beta,depth-1))
            self._board.pop()
            if alpha >= beta:
                return alpha
        return beta
    
    def indiceMax(self,array):
        max=np.amax(array)
        for i in range(len(array)):
            if array[i]==max:
                return i

    def getPlayerMove(self):
        if self._opening!=[]:
            move=self._opening[0]
            self._opening=self._opening[1:]
            if Goban.Board.name_to_flat(move) in self._board.legal_moves() :
                self._board.push(Goban.Board.name_to_flat(move)) # MOVE POTENTIELLEMENT ILLEGAL : A CORRIGER
                return move # MOVE POTENTIELLEMENT ILLEGAL
            else:
                print("Opening became illegal, starting midgame")
                self._opening=[]
        if self._board.is_game_over():
            return "PASS" 
        if self._board._lastPlayerHasPassed:
            return "PASS" 
        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
        movesPower = []
        for i in range(len(moves)):
            self._board.push(moves[i])
            movesPower+=[self.maxAB(-100000,100000,self._initialDepth)]
            self._board.pop()
        move=moves[self.indiceMax(movesPower)]
        print(movesPower)
        self._board.push(move)

        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("CSGO won!!!")
        else:
            print("CSGO lost :(!!")



# A FAIRE : 
#   Parcer .json pour obtenir des entry
#   Ajouter à l'heuristique un calcul en plus des captures
#   Trouver vraie heuristique (chercher degrés de liberté)