#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Vassilis Athitsos
# Written to be Python 2.4 compatible for omega

from copy import deepcopy
import random
import sys

class maxConnect4Game:
    def __init__(self):
        self.gameBoard = [[0 for i in range(7)] for j in range(6)]
        self.currentTurn = 1
        self.player1Score = 0
        self.player2Score = 0
        self.pieceCount = 0
        self.gameFile = None
	self.children = []
        self.name = 'root'
	self.player = 0
	self.alpha = -99
	self.beta = 99
	self.depth = 0
        
    # Count the number of pieces already played
    def checkPieceCount(self):
        self.pieceCount = sum(1 for row in self.gameBoard for piece in row if piece)

    # Output current game status to console
    def printGameBoard(self):
        print ' -----------------'
        for i in range(6):
            print ' |',
            for j in range(7):
                print('%d' % self.gameBoard[i][j]),
            print '| '
        print ' -----------------'

    # Output current game status to file
    def printGameBoardToFile(self):
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # write output of interactive mode to file
    def interactive_printGameBoardToFile(self, outfile):
        self.gameFile = open(outfile, 'w')
        for row in self.gameBoard:
            self.gameFile.write(''.join(str(col) for col in row) + '\r\n')
        self.gameFile.write('%s\r\n' % str(self.currentTurn))

    # Place the current player's piece in the requested column
    def playPiece(self, column):
        if not self.gameBoard[0][column]:
            for i in range(5, -1, -1):
                if not self.gameBoard[i][column]:
                    # print "innner if"
                    self.gameBoard[i][column] = self.currentTurn
                    self.pieceCount += 1
                    return 1

    # The AI section. Currently plays randomly. modified for one-mode game
    def aiPlay(self, depth):
	    #Select thee move with the minimax algo
	    #pass the move to the playpiece method
        # randColumn = random.randrange(0,7)
        # result = self.playPiece(randColumn)
        # if not result:
        #    self.aiPlay()
        # else:
        #    print('\n\nmove %d: Player %d, column %d\n' % (self.pieceCount, self.currentTurn, randColumn+1))
        #    if self.currentTurn == 1:
        #        self.currentTurn = 2
        #    elif self.currentTurn == 2:
        #        self.currentTurn = 1
		#in generate children function
		# for i in range(7)
		#    state = maxConnect4Game()
		#	result = state.playPiece(i)
		#	if result == 1:
		#	   state.name = self.name + str(i)
		#	   print str(state.gameBoard)
		#	   # self.gameBoard = state.gameBoard
		#	   self.children.append(state)
		#	   state.parent = self.name
		#	   state.aiPlay() # recursively call to generate trees
		# call minimax function
		# result = self.playPiece(1)
                #if not result:
		if self.pieceCount == 42:
                   return
		selected_state = self.minimax_decision(depth)
		self.gameBoard = deepcopy(selected_state.gameBoard)
		self.children = []
		self.changePlayerTurn()

    # AI section for interactive mode
    def aiplay_interactive(self, interactive_move, depth):
	if interactive_move == 'computer-next':
	   result = self.computer_turn(interactive_move,depth)
	else:
            if interactive_move == 'human-next':
               result = self.human_turn(interactive_move,depth)
	return result

    # computer turn
    def computer_turn(self, interactive_move, depth):
	self.checkPieceCount()
	selected_state = self.minimax_decision(depth)
	self.gameBoard = deepcopy(selected_state.gameBoard)
	self.children = []
	interactive_move = 'human-next'
	self.changePlayerTurn()
        outfile = 'computer.txt'
        self.interactive_printGameBoardToFile(outfile)
	return interactive_move

    # Human turn
    def human_turn(self, interactive_move, depth):
	self.checkPieceCount()
        outfile = 'human.txt'
        while True:
              human_move = input("Enter the column number you want to play: ")
              human_move = human_move - 1
	      result = self.playPiece(human_move)
              if result:
	         interactive_move = 'computer-next'
	         self.changePlayerTurn()
                 self.interactive_printGameBoardToFile(outfile)
	         return interactive_move
              else:
                 print "Invalid move..!!"
	
    # minimax function 
    def minimax_decision(self, depth):
	selected_move = maxConnect4Game()
        self.generateStates()
	utility = -99
	for row in self.children:
	    row.changePlayerTurn()
       	    this_state_utility = row.min_value(depth)
            # maximizing move
            if utility < this_state_utility:
	           utility = this_state_utility
		   self.alpha = max(utility,self.alpha)
	           selected_move = row
	    
        return selected_move
		
    # min-value function
    def min_value(self, depth):
	turn = 'min'
	# check terminal state 
	utility = self.terminal_test(turn)
	if utility < 99:
           return utility
	else:
	    if int(depth) == self.depth:
               return self.eval_fn()	
            else:
	        utility = 99
	        self.generateStates()
                for row in self.children:
		    row.beta = self.beta
		    row.changePlayerTurn()
	            utility = min(utility, row.max_value(depth))
		    if utility <= self.alpha:
		       return utility
		    self.beta = min(utility, self.beta)
	        return utility
	
    # max-value function 
    def max_value(self, depth):
	turn = 'max'
	utility = self.terminal_test(turn)
	if utility < 99:
	   return utility
	else:	
	    if int(depth) == self.depth:
               return self.eval_fn()
            else:
	        utility = -99
	        self.generateStates()
	        for row in self.children:
		    row.alpha = self.alpha
		    row.changePlayerTurn()
                    utility = max(utility, row.min_value(depth))
	            if utility >= self.beta:
	               return utility
        	    self.alpha = max(utility, self.alpha)
	        return utility
	
    # check for terminal state
    def terminal_test(self, turn):
	self.checkPieceCount()
	if self.pieceCount == 42:
	   self.countScore()
           if self.player1Score == self.player2Score:
              return 0
           if self.player1Score > self.player2Score and self.player == 1:
              return 1
           else:
	       if self.player1Score > self.player2Score:
		  return -1
	       else:
	           if self.player1Score < self.player2Score and self.player == 2:
	              return 1
		   else:
                       if self.player1Score < self.player2Score:
			  return -1
	      	       else:
	                  return 0
	else:
	    return 99		
		
    #switch turn of player
    def changePlayerTurn(self):	
	if self.currentTurn == 1:
           self.currentTurn = 2
        elif self.currentTurn == 2:
	     self.currentTurn = 1

    def generateStates(self):
	for i in range(7):
            state = maxConnect4Game()
	    state.name = str(self.name) + str(i)
	    state.currentTurn = self.currentTurn
            state.depth = self.depth + 1
	    state.player = self.player
	    state.gameBoard = deepcopy(self.gameBoard)
	    state.pieceCount = self.pieceCount
	    result = state.playPiece(i)
	    if result:
	       self.children.append(state)
	
    #eval func
    def eval_fn(self):
	
	if self.player == 1:
	   result =  self.player1_eval()
	else:
	    if self.player == 2:
               result = self.player2_eval()
	return result

    # eval func for player 1
    def player1_eval(self):
        # Check horizontally
        four_cnt_1 = 0
        four_cnt_2 = 0
	for row in self.gameBoard:
            
            # Check player 1
            if row[0:4] == [1]*4:
                four_cnt_1 += 1
            if row[1:5] == [1]*4:
                four_cnt_1 += 1
            if row[2:6] == [1]*4:
                four_cnt_1 += 1
            if row[3:7] == [1]*4:
                four_cnt_1 += 1
	   
            # for 3 horizontally
            if row[0:3] == [1]*4:
                four_cnt_1 += 0.80
            if row[1:4] == [1]*4:
                four_cnt_1 += 0.80
            if row[2:5] == [1]*4:
                four_cnt_1 += 0.80
            if row[3:6] == [1]*4:
                four_cnt_1 += 0.80
            if row[4:7] == [1]*4:
                four_cnt_1 += 0.80

            # for 2 horizontally
            if row[0:2] == [1]*4:
                four_cnt_1 += 0.15
            if row[1:3] == [1]*4:
                four_cnt_1 += 0.15
            if row[2:4] == [1]*4:
                four_cnt_1 += 0.15
            if row[3:5] == [1]*4:
                four_cnt_1 += 0.15
            if row[4:6] == [1]*4:
                four_cnt_1 += 0.15
            if row[5:7] == [1]*4:
                four_cnt_1 += 0.15


            # Check player 2
            if row[0:4] == [2]*4:
                four_cnt_2 += -1
            if row[1:5] == [2]*4:
                four_cnt_2 += -1
            if row[2:6] == [2]*4:
                four_cnt_2 += -1
            if row[3:7] == [2]*4:
                four_cnt_2 += -1

            # for 3 horizontally
            if row[0:3] == [2]*4:
                four_cnt_2 += -0.80
            if row[1:4] == [2]*4:
                four_cnt_2 += -0.80
            if row[2:5] == [2]*4:
                four_cnt_2 += -0.80
            if row[3:6] == [2]*4:
                four_cnt_2 += -0.80
            if row[4:7] == [2]*4:
                four_cnt_2 += -0.80

            # for 2 horizontally
            if row[0:2] == [2]*4:
                four_cnt_2 += -0.15
            if row[1:3] == [2]*4:
                four_cnt_2 += -0.15
            if row[2:4] == [2]*4:
                four_cnt_2 += -0.15
            if row[3:5] == [2]*4:
                four_cnt_2 += -0.15
            if row[4:6] == [2]*4:
                four_cnt_2 += -0.15
            if row[5:7] == [2]*4:
                four_cnt_2 += -0.15

            # Check vertically for four
	    # player 1
            for j in range(7):
                # Check player 1
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                    self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                   four_cnt_1 += 1
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                    self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                   four_cnt_1 += 1
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                    self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                   four_cnt_1 += 1

                # Check vertically for 3                
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                    self.gameBoard[2][j] == 1):
                   four_cnt_1 += 0.80
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                    self.gameBoard[3][j] == 1):
                   four_cnt_1 += 0.80
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                    self.gameBoard[4][j] == 1):
                   four_cnt_1 += 0.80
                if (self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1 and
                    self.gameBoard[5][j] == 1):
                   four_cnt_1 += 0.80
		
		# Check vertically for 2
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1):
                   four_cnt_1 += 0.15
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1):
                   four_cnt_1 += 0.15
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                   four_cnt_1 += 0.15
                if (self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                   four_cnt_1 += 0.15
                if (self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                   four_cnt_1 += 0.15

                # Check player 2
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                    self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                   four_cnt_2 += -1
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                    self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                   four_cnt_2 += -1
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                    self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                   four_cnt_2 += -1

                # Check vertically for 3                
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                    self.gameBoard[2][j] == 2):
                   four_cnt_2 += -0.80
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                    self.gameBoard[3][j] == 2):
                   four_cnt_2 += -0.80
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                    self.gameBoard[4][j] == 2):
                   four_cnt_2 += -0.80
                if (self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2 and
                    self.gameBoard[5][j] == 2):
                   four_cnt_2 += -0.80
		
		# Check vertically for 2
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2):
                   four_cnt_2 += -0.15
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2):
                   four_cnt_2 += -0.15
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                   four_cnt_2 += -0.15
                if (self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                   four_cnt_2 += -0.15
                if (self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                   four_cnt_2 += -0.15
		
		
        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            four_cnt_1 += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            four_cnt_1 += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            four_cnt_1 += 1

        # check diagonally for 3 and blank
    
        if (self.gameBoard[5][3] == 1 and self.gameBoard[4][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[3][0] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[2][1] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[4][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[1][0] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[5][5] == 1 and self.gameBoard[4][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[2][2] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[4][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[1][1] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[3][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[1][1] == 1 and self.gameBoard[0][0] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[5][6] == 1 and self.gameBoard[4][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[2][3] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[4][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[1][2] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[3][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[1][2] == 1 and self.gameBoard[0][1] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[4][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[1][3] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[3][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[1][3] == 1 and self.gameBoard[0][2] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[5][3] == 1 and self.gameBoard[4][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[2][6] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[5][2] == 1 and self.gameBoard[4][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[2][5] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[4][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[1][6] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[5][1] == 1 and self.gameBoard[4][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[2][4] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[4][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[1][5] == 1):
            four_cnt_1 += 0.70
        if (self.gameBoard[3][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[1][5] == 1 and self.gameBoard[0][6] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[5][0] == 1 and self.gameBoard[4][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[2][3] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[4][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[1][4] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[3][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[1][4] == 1 and self.gameBoard[0][5] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[4][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[1][3] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[3][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[1][3] == 1 and self.gameBoard[0][4] == 0):
            four_cnt_1 += 0.70
        if (self.gameBoard[3][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[1][2] == 1 and self.gameBoard[0][3] == 0):
            four_cnt_1 += 0.70
        

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            four_cnt_2 += -1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            four_cnt_2 +=-1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            four_cnt_2 += -1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            four_cnt_2 += -1
         
	# check player 2 diag 3
        if (self.gameBoard[5][3] == 2 and self.gameBoard[4][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[3][0] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[2][1] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[4][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[1][0] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[5][5] == 2 and self.gameBoard[4][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[2][2] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[4][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[1][1] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[3][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[1][1] == 2 and self.gameBoard[0][0] == 0):
            four_cnt_2 +=  -0.70
        if (self.gameBoard[5][6] == 2 and self.gameBoard[4][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[2][3] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[4][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[1][2] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[3][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[1][2] == 2 and self.gameBoard[0][1] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[4][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[1][3] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[3][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[1][3] == 2 and self.gameBoard[0][2] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[5][3] == 2 and self.gameBoard[4][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[2][6] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[5][2] == 2 and self.gameBoard[4][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[2][5] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[4][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[1][6] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[5][1] == 2 and self.gameBoard[4][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[2][4] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[4][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[1][5] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[3][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[1][5] == 2 and self.gameBoard[0][6] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[5][0] == 2 and self.gameBoard[4][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[2][3] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[4][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[1][4] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[3][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[1][4] == 2 and self.gameBoard[0][5] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[4][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[1][3] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[3][1] == 2 and self.gameBoard[2][2] == 2and
               self.gameBoard[1][3] == 2 and self.gameBoard[0][4] == 0):
            four_cnt_2 += -0.70
        if (self.gameBoard[3][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[1][2] == 2 and self.gameBoard[0][3] == 0):
            four_cnt_2 += -0.70
        
	sum = four_cnt_2 + four_cnt_1
        return sum

    # evaluation function for player 2
    def player2_eval(self):
        four_cnt_1 = 0
        four_cnt_2 = 0
        # Check horizontally
	for row in self.gameBoard:
            
            # Check player 1
            if row[0:4] == [1]*4:
                four_cnt_1 += -1
            if row[1:5] == [1]*4:
                four_cnt_1 += -1
            if row[2:6] == [1]*4:
                four_cnt_1 += -1
            if row[3:7] == [1]*4:
                four_cnt_1 += -1
	   
            # for 3 horizontally
            if row[0:3] == [1]*4:
                four_cnt_1 += -0.80
            if row[1:4] == [1]*4:
                four_cnt_1 += -0.80
            if row[2:5] == [1]*4:
                four_cnt_1 += -0.80
            if row[3:6] == [1]*4:
                four_cnt_1 += -0.80
            if row[4:7] == [1]*4:
                four_cnt_1 += -0.80

            # for 2 horizontally
            if row[0:2] == [1]*4:
                four_cnt_1 += -0.15
            if row[1:3] == [1]*4:
                four_cnt_1 += -0.15
            if row[2:4] == [1]*4:
                four_cnt_1 += -0.15
            if row[3:5] == [1]*4:
                four_cnt_1 += -0.15
            if row[4:6] == [1]*4:
                four_cnt_1 += -0.15
            if row[5:7] == [1]*4:
                four_cnt_1 += -0.15


            # Check player 2
            if row[0:4] == [2]*4:
                four_cnt_2 += 1
            if row[1:5] == [2]*4:
                four_cnt_2 += 1
            if row[2:6] == [2]*4:
                four_cnt_2 += 1
            if row[3:7] == [2]*4:
                four_cnt_2 += 1

            # for 3 horizontally
            if row[0:3] == [2]*4:
                four_cnt_2 += 0.80
            if row[1:4] == [2]*4:
                four_cnt_2 += 0.80
            if row[2:5] == [2]*4:
                four_cnt_2 += 0.80
            if row[3:6] == [2]*4:
                four_cnt_2 += 0.80
            if row[4:7] == [2]*4:
                four_cnt_2 += 0.80

            # for 2 horizontally
            if row[0:2] == [2]*4:
                four_cnt_2 += 0.15
            if row[1:3] == [2]*4:
                four_cnt_2 += 0.15
            if row[2:4] == [2]*4:
                four_cnt_2 += 0.15
            if row[3:5] == [2]*4:
                four_cnt_2 += 0.15
            if row[4:6] == [2]*4:
                four_cnt_2 += 0.15
            if row[5:7] == [2]*4:
                four_cnt_2 += 0.15

            # Check vertically for four
	    # player 1
            for j in range(7):
                # Check player 1
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                    self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                   four_cnt_1 += -1
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                    self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                   four_cnt_1 += -1
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                    self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                   four_cnt_1 += -1

                # Check vertically for 3                
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                    self.gameBoard[2][j] == 1):
                   four_cnt_1 += -0.80
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                    self.gameBoard[3][j] == 1):
                   four_cnt_1 += -0.80
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                    self.gameBoard[4][j] == 1):
                   four_cnt_1 += -0.80
                if (self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1 and
                    self.gameBoard[5][j] == 1):
                   four_cnt_1 += -0.80
		
		# Check vertically for 2
                if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1):
                   four_cnt_1 += -0.15
                if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1):
                   four_cnt_1 += -0.15
                if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                   four_cnt_1 += -0.15
                if (self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                   four_cnt_1 += -0.15
                if (self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                   four_cnt_1 += -0.15

                # Check player 2
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                    self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                   four_cnt_2 += 1
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                    self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                   four_cnt_2 += 1
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                    self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                   four_cnt_2 += 1

                # Check vertically for 3                
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                    self.gameBoard[2][j] == 2):
                   four_cnt_2 += 0.80
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                    self.gameBoard[3][j] == 2):
                   four_cnt_2 += 0.80
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                    self.gameBoard[4][j] == 2):
                   four_cnt_2 += 0.80
                if (self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2 and
                    self.gameBoard[5][j] == 2):
                   four_cnt_2 += 0.80
		
		# Check vertically for 2
                if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2):
                   four_cnt_2 += 0.15
                if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2):
                   four_cnt_2 += 0.15
                if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                   four_cnt_2 += 0.15
                if (self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                   four_cnt_2 += 0.15
                if (self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                   four_cnt_2 += 0.15
		
		
        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            four_cnt_1 += -1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            four_cnt_1 += -1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            four_cnt_1 += -1

	# check player 1 diagonally for 3
        if (self.gameBoard[5][3] == 1 and self.gameBoard[4][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[3][0] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[2][1] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[4][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[1][0] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[5][5] == 1 and self.gameBoard[4][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[2][2] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[4][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[1][1] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[3][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[1][1] == 1 and self.gameBoard[0][0] == 0):
            four_cnt_1 +=  -0.70
        if (self.gameBoard[5][6] == 1 and self.gameBoard[4][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[2][3] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[4][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[1][2] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[3][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[1][2] == 1 and self.gameBoard[0][1] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[4][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[1][3] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[3][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[1][3] == 1 and self.gameBoard[0][2] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[5][3] == 1 and self.gameBoard[4][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[2][6] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[5][2] == 1 and self.gameBoard[4][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[2][5] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[4][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[1][6] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[5][1] == 1 and self.gameBoard[4][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[2][4] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[4][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[1][5] == 1):
            four_cnt_1 += -0.70
        if (self.gameBoard[3][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[1][5] == 1 and self.gameBoard[0][6] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[5][0] == 1 and self.gameBoard[4][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[2][3] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[4][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[1][4] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[3][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[1][4] == 1 and self.gameBoard[0][5] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[4][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[1][3] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[3][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[1][3] == 1 and self.gameBoard[0][4] == 0):
            four_cnt_1 += -0.70
        if (self.gameBoard[3][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[1][2] == 1 and self.gameBoard[0][3] == 0):
            four_cnt_1 += -0.70
        


        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            four_cnt_2 += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            four_cnt_2 +=1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            four_cnt_2 += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            four_cnt_2 += 1
      
        # player 2 diagonal for 3
        if (self.gameBoard[5][3] == 2 and self.gameBoard[4][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[3][0] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[2][1] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[4][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[1][0] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[5][5] == 2 and self.gameBoard[4][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[2][2] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[4][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[1][1] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[3][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[1][1] == 2 and self.gameBoard[0][0] == 0):
            four_cnt_2 +=  0.70
        if (self.gameBoard[5][6] == 2 and self.gameBoard[4][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[2][3] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[4][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[1][2] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[3][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[1][2] == 2 and self.gameBoard[0][1] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[4][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[1][3] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[3][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[1][3] == 2 and self.gameBoard[0][2] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[5][3] == 2 and self.gameBoard[4][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[2][6] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[5][2] == 2 and self.gameBoard[4][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[2][5] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[4][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[1][6] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[5][1] == 2 and self.gameBoard[4][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[2][4] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[4][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[1][5] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[3][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[1][5] == 2 and self.gameBoard[0][6] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[5][0] == 2 and self.gameBoard[4][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[2][3] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[4][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[1][4] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[3][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[1][4] == 2 and self.gameBoard[0][5] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[4][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[1][3] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[3][1] == 2 and self.gameBoard[2][2] == 2and
               self.gameBoard[1][3] == 2 and self.gameBoard[0][4] == 0):
            four_cnt_2 += 0.70
        if (self.gameBoard[3][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[1][2] == 2 and self.gameBoard[0][3] == 0):
            four_cnt_2 += 0.70
        


        sum = four_cnt_2 + four_cnt_1
        return sum 

    # Check 4's in-a-row
    def countScore(self):
        self.player1Score = 0;
        self.player2Score = 0;

        # Check horizontally
        for row in self.gameBoard:
            # Check player 1
            if row[0:4] == [1]*4:
                self.player1Score += 1
            if row[1:5] == [1]*4:
                self.player1Score += 1
            if row[2:6] == [1]*4:
                self.player1Score += 1
            if row[3:7] == [1]*4:
                self.player1Score += 1
            # Check player 2
            if row[0:4] == [2]*4:
                self.player2Score += 1
            if row[1:5] == [2]*4:
                self.player2Score += 1
            if row[2:6] == [2]*4:
                self.player2Score += 1
            if row[3:7] == [2]*4:
                self.player2Score += 1

        # Check vertically
        for j in range(7):
            # Check player 1
            if (self.gameBoard[0][j] == 1 and self.gameBoard[1][j] == 1 and
                   self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[1][j] == 1 and self.gameBoard[2][j] == 1 and
                   self.gameBoard[3][j] == 1 and self.gameBoard[4][j] == 1):
                self.player1Score += 1
            if (self.gameBoard[2][j] == 1 and self.gameBoard[3][j] == 1 and
                   self.gameBoard[4][j] == 1 and self.gameBoard[5][j] == 1):
                self.player1Score += 1
            # Check player 2
            if (self.gameBoard[0][j] == 2 and self.gameBoard[1][j] == 2 and
                   self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[1][j] == 2 and self.gameBoard[2][j] == 2 and
                   self.gameBoard[3][j] == 2 and self.gameBoard[4][j] == 2):
                self.player2Score += 1
            if (self.gameBoard[2][j] == 2 and self.gameBoard[3][j] == 2 and
                   self.gameBoard[4][j] == 2 and self.gameBoard[5][j] == 2):
                self.player2Score += 1

        # Check diagonally

        # Check player 1
        if (self.gameBoard[2][0] == 1 and self.gameBoard[3][1] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][0] == 1 and self.gameBoard[2][1] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][1] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][0] == 1 and self.gameBoard[1][1] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][1] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][2] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][1] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][2] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][5] == 1 and self.gameBoard[5][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][2] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][5] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][5] == 1 and self.gameBoard[4][6] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][5] == 1 and self.gameBoard[3][6] == 1):
            self.player1Score += 1

        if (self.gameBoard[0][3] == 1 and self.gameBoard[1][2] == 1 and
               self.gameBoard[2][1] == 1 and self.gameBoard[3][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][4] == 1 and self.gameBoard[1][3] == 1 and
               self.gameBoard[2][2] == 1 and self.gameBoard[3][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][3] == 1 and self.gameBoard[2][2] == 1 and
               self.gameBoard[3][1] == 1 and self.gameBoard[4][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][5] == 1 and self.gameBoard[1][4] == 1 and
               self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][4] == 1 and self.gameBoard[2][3] == 1 and
               self.gameBoard[3][2] == 1 and self.gameBoard[4][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][3] == 1 and self.gameBoard[3][2] == 1 and
               self.gameBoard[4][1] == 1 and self.gameBoard[5][0] == 1):
            self.player1Score += 1
        if (self.gameBoard[0][6] == 1 and self.gameBoard[1][5] == 1 and
               self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][5] == 1 and self.gameBoard[2][4] == 1 and
               self.gameBoard[3][3] == 1 and self.gameBoard[4][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][4] == 1 and self.gameBoard[3][3] == 1 and
               self.gameBoard[4][2] == 1 and self.gameBoard[5][1] == 1):
            self.player1Score += 1
        if (self.gameBoard[1][6] == 1 and self.gameBoard[2][5] == 1 and
               self.gameBoard[3][4] == 1 and self.gameBoard[4][3] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][5] == 1 and self.gameBoard[3][4] == 1 and
               self.gameBoard[4][3] == 1 and self.gameBoard[5][2] == 1):
            self.player1Score += 1
        if (self.gameBoard[2][6] == 1 and self.gameBoard[3][5] == 1 and
               self.gameBoard[4][4] == 1 and self.gameBoard[5][3] == 1):
            self.player1Score += 1

        # Check player 2
        if (self.gameBoard[2][0] == 2 and self.gameBoard[3][1] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][0] == 2 and self.gameBoard[2][1] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][1] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][0] == 2 and self.gameBoard[1][1] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][1] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][2] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][1] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][2] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][5] == 2 and self.gameBoard[5][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][2] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][5] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][5] == 2 and self.gameBoard[4][6] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][5] == 2 and self.gameBoard[3][6] == 2):
            self.player2Score += 1

        if (self.gameBoard[0][3] == 2 and self.gameBoard[1][2] == 2 and
               self.gameBoard[2][1] == 2 and self.gameBoard[3][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][4] == 2 and self.gameBoard[1][3] == 2 and
               self.gameBoard[2][2] == 2 and self.gameBoard[3][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][3] == 2 and self.gameBoard[2][2] == 2 and
               self.gameBoard[3][1] == 2 and self.gameBoard[4][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][5] == 2 and self.gameBoard[1][4] == 2 and
               self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][4] == 2 and self.gameBoard[2][3] == 2 and
               self.gameBoard[3][2] == 2 and self.gameBoard[4][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][3] == 2 and self.gameBoard[3][2] == 2 and
               self.gameBoard[4][1] == 2 and self.gameBoard[5][0] == 2):
            self.player2Score += 1
        if (self.gameBoard[0][6] == 2 and self.gameBoard[1][5] == 2 and
               self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][5] == 2 and self.gameBoard[2][4] == 2 and
               self.gameBoard[3][3] == 2 and self.gameBoard[4][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][4] == 2 and self.gameBoard[3][3] == 2 and
               self.gameBoard[4][2] == 2 and self.gameBoard[5][1] == 2):
            self.player2Score += 1
        if (self.gameBoard[1][6] == 2 and self.gameBoard[2][5] == 2 and
               self.gameBoard[3][4] == 2 and self.gameBoard[4][3] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][5] == 2 and self.gameBoard[3][4] == 2 and
               self.gameBoard[4][3] == 2 and self.gameBoard[5][2] == 2):
            self.player2Score += 1
        if (self.gameBoard[2][6] == 2 and self.gameBoard[3][5] == 2 and
               self.gameBoard[4][4] == 2 and self.gameBoard[5][3] == 2):
            self.player2Score += 1


# REFERENCES: Github, Stackoverflow and other online forums