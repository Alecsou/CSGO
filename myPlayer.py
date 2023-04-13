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
from random import choice

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
        self._totalTime = 0
        self._actualDepth = self._initialDepth
        self._moveNb = 0

        self._criticalMode = False
        self._ultraCriticalMode = False
        self._openingDisturbed = False
        

    def getPlayerName(self):
        return "CSGO"
    
    def heuristic(self,depth):
        if (depth==0 or self._board.is_game_over()):
            self._decimalPoint+=0.000000000000001
            stoneDiff = self._board._nbBLACK - self._board._nbWHITE 
            captureDiff = self._board._capturedWHITE - self._board._capturedBLACK
            overallStatus = stoneDiff + captureDiff
            if self._mycolor==self._board._BLACK:
                return overallStatus + self._decimalPoint # self._board._nbBLACK + self._board._capturedWHITE - self._board._nbWHITE - self._board._capturedBLACK
            else:
                return -1*overallStatus + self._decimalPoint # self._board._nbWHITE + self._board._capturedBLACK - self._board._nbBLACK - self._board._capturedWHITE
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

    def checkKillerMove(self):
        moves = self._board.legal_moves()
        if self._mycolor==self._board._BLACK:
            initialWhites = self._board._nbWHITE
            for i in range(len(moves)):
                self._board.push(moves[i])
                if self._board._nbWHITE < 0.90 * initialWhites:
                    self._actualDepth=self._initialDepth
                    print("                                       [Player CSGO]                                                ")
                    print("Killer move detected on next turn ! For time safety reson, decreasing depth of AlphaBeta to ",self._initialDepth)
                    print("                                       [Player CSGO]                                                ")
                self._board.pop()
        if self._mycolor==self._board._WHITE:
            initialBlacks = self._board._nbBLACK
            for i in range(len(moves)):
                self._board.push(moves[i])
                if self._board._nbBLACK < 0.90 * initialBlacks:
                    self._actualDepth=self._initialDepth
                    print("                                       [Player CSGO]                                                ")
                    print("Killer move detected on next turn ! For time safety reson, decreasing depth of AlphaBeta to ",self._initialDepth)
                    print("                                       [Player CSGO]                                                ")
                self._board.pop()

    def getPlayerMove(self):
        startTime=time.time()
        print("")
        self._moveNb+=1
        if self._opening!=[]:
            print("                                       [Player CSGO]                                                ")
            print("                                       Opening move")
            print("                                       [Player CSGO]                                                ")
            move=self._opening[0]
            self._opening=self._opening[1:]
            if Goban.Board.name_to_flat(move) in self._board.legal_moves() :
                self._board.push(Goban.Board.name_to_flat(move))
                print("I am playing ", move)
                print("My current board :")
                self._board.prettyPrint()
                turnTime=time.time()-startTime
                self._totalTime+=turnTime
                print("                                       [Player CSGO]                                                ")
                print("                                   It took ",turnTime,"s")
                print("                                       [Player CSGO]                                                ")
                return move
            else:
                print("                                       [Player CSGO]                                                ")
                print("   Opening became illegal with move ", move ,", starting Disturbed Opening Mode until Turn 16!")
                print("                                       [Player CSGO]                                                ")
                self._opening=[]
                self._openingDisturbed=True
                self._actualDepth=1
        if self._openingDisturbed==True:
            if self._moveNb==16:
                print("                                       [Player CSGO]                                                ")
                print("                        Stopping Disturbed Opening Mode at Turn 16!")
                print("                                       [Player CSGO]                                                ")
                self._openingDisturbed=False
                self._actualDepth=self._initialDepth
            else:
                print("                                       [Player CSGO]                                                ")
                print("                              Playing in Disturbed Opening Mode")
                print("                                       [Player CSGO]                                                ")
                moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
                move = choice(moves) 
                self._board.push(move)
                print("I am playing ", self._board.move_to_str(move))
                print("My current board :")
                self._board.prettyPrint()
                turnTime=time.time()-startTime
                self._totalTime+=turnTime
                print("                                       [Player CSGO]                                                ")
                print("                                  It took ",turnTime,"s")
                print("                                       [Player CSGO]                                                ")
                return Goban.Board.flat_to_name(move) 
        print("                                       [Player CSGO]                                                ")
        print("                      Depth of AlphaBeta is ", self._actualDepth)
        print("                                       [Player CSGO]                                                ")
        if self._board.is_game_over():
            return "PASS" 
        if self._board._lastPlayerHasPassed:
            return "PASS" 
        moves = self._board.legal_moves()
        movesPower = []
        for i in range(len(moves)):
            self._board.push(moves[i])
            movesPower+=[self.maxAB(-100000,100000,self._actualDepth)]
            self._board.pop()
        move=moves[self.indiceMax(movesPower)]
        self._board.push(move)
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        turnTime=time.time()-startTime
        self._totalTime+=turnTime
        diff=time.time()
        print("                                       [Player CSGO]                                                ")
        print("                                  It took ",turnTime,"s")
        print("                                       [Player CSGO]                                                ")

        if (30*60)-self._totalTime<60:
            self._criticalMode=True
            print("                                       [Player CSGO]                                                ")
            print("        60 seconds or less remaining. Critical mode activated ! AlphaBeta depth set to 2.")
            print("                                       [Player CSGO]                                                ")
            self._actualDepth=2
        if (30*60)-self._totalTime<10:
            self._ultraCriticalMode=True
            print("                                       [Player CSGO]                                                ")
            print("     10 seconds or less remaining. ULTRA CRITICAL MODE activated ! AlphaBeta depth set to 1.")
            print("                                       [Player CSGO]                                                ")
            self._actualDepth=1

        if self._criticalMode==False and self._ultraCriticalMode==False:
            totalStones=self._board._nbBLACK + self._board._nbWHITE 
            if self._actualDepth < 6 and (2*turnTime*(81-(totalStones+1)))<= (30*60)-self._totalTime:
                self._actualDepth+=1
                print("                                       [Player CSGO]                                                ")
                print("                    Increasing depth of AlphaBeta to ",self._actualDepth)
                print("                                       [Player CSGO]                                                ")
            elif self._actualDepth > 2 and (turnTime*(81-(totalStones+1))) > 1.50*((30*60)-self._totalTime):
                self._actualDepth-=1
                print("                                       [Player CSGO]                                                ")
                print("                    Decreasing depth of AlphaBeta to ",self._actualDepth)
                print("                                       [Player CSGO]                                                ")
            self.checkKillerMove()
        self._totalTime+=time.time()-diff
        print("                                       [Player CSGO]                                                ")
        print("                            Time remaining: ", (30*60)-self._totalTime)
        print("                                       [Player CSGO]                                                ")
        return Goban.Board.flat_to_name(move) 


    def playOpponentMove(self, move):
        print("Opponent played ", move)
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
#   Trouver vraie heuristique (chercher degrés de liberté)