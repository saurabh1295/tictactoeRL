# This is an attempt to create a learning agent that can learn to play tic tac toe using the Q-learning algorithm
# I first attempted to create an agent that always tried to win, but this led to an agent that was losing too easily
# Thus, I started "punishing" the agent for losing by giving negative rewards 
# The state has been depicted as a numpy array of 10 axes, the first 9 of which indicate the 9 boxes and the last is for the actions 
# The board has a configuration of 
#   7| 8| 9
#  __|__|__
#   4| 5| 6
#  __|__|__
#   1| 2| 3
#    |  |


import random
import numpy as np
#initialize some global variables
alpha = 0.99
epsilon = 0.1
playerchar='X'
compchar = 'O'

# Some helper functions to 
#Print the current board
def printBoard(board):
	print('   |  |   ');
	print(' '+board[6]+' |'+board[7]+' |'+board[8])
	print('___|__|___');
	print(' '+board[3]+' |'+board[4]+' |'+board[5])
	print('___|__|___');
	print(' '+board[0]+' |'+board[1]+' |'+board[2])
	print('   |  |');

#Initializes the board for a new game	
def boardInit():	
	board =[]
	for i in range(9):
		board.append(' ')
	return board

# This state is a numpy array which stores the 9 elements 0 indicates blank
# 1 indicates O
# 2 indicates X
def getState(board):
	global compchar
	state = np.zeros(9,dtype="int")
	for i in range(len(board)):
		if(board[i] == 'O'):
			state[i]=1
		elif board[i] == 'X':
			state[i]=2
	return state

# Returns a list of possible actions from current state

def getPossibleActions(board):
	possibleactions = []
	for i in range(len(board)):
		if(board[i] == ' '):
			possibleactions.append(i)
	return possibleactions


# Q values stores the Qvalue for all states 
# The first dim is for blanks
# The second dim is for computer's states
# The third dim is for the turn's states
# The fourth dim is for actions
def qValInit():
	qVal = np.ones([3,3,3,3,3,3,3,3,3,9])
	qVal = qVal*0.5
	return qVal

# Returns true if the next state is valid
def isValidAction(board,action):
	if board[action] == ' ':
		return True
	else:
		return False

def isBoardFull(board):
	for i in range(len(board)):
		if board[i] == ' ':
			return False
	return True

def getPlayerMove(board):
		print("Choose the next action input(1-9)")
		move = raw_input()
		move = int(move) -1
		while not isValidAction(board,move):
			print("Choose the next action input(1-9)")
			move = raw_input()
			move = int(move) -1
			if isValidAction(board,move):
				break
		board = getNextBoardState(board,'user',move)
		return board

def getPlayerMoveauto(board):
	possibleactions=getPossibleActions(board)
	move = random.choice(possibleactions)
	board = getNextBoardState(board,'user',move)
	return board

 
def getNextBoardState(boarde,turn,action):
	global playerchar
	global compchar
	lamb = []
	for i in range(9):
		lamb.append(boarde[i])
	if isValidAction(lamb,action):
		if turn == 'comp':
			lamb[action] = compchar
		else:
			lamb[action] = playerchar
	return lamb


def hasWon(bo,turn):
	global playerchar
	global compchar
	if turn == 'comp':
		le = compchar
	else:
		le = playerchar
	return ((bo[6] == le and bo[7] == le and bo[8] == le) or # across the top
      (bo[3] == le and bo[4] == le and bo[5] == le) or # across the middle
      (bo[0] == le and bo[1] == le and bo[2] == le) or # across the bottom
      (bo[6] == le and bo[3] == le and bo[0] == le) or # down the left side
      (bo[7] == le and bo[4] == le and bo[1] == le) or # down the middle
      (bo[8] == le and bo[5] == le and bo[2] == le) or # down the right side
      (bo[6] == le and bo[4] == le and bo[2] == le) or # diagonal
      (bo[8] == le and bo[4] == le and bo[0] == le)) # diagonal
def evalNextStateforComp(board,player,opp):
	global alpha 
	global epsilon
	global qvals
	possibleactions = getPossibleActions(board)
	state =getState(board)
	possibleactions = np.array(possibleactions,dtype = "int")
	max = float("-inf")
	nextAction = -1
	choice = random.random()
	if choice >=epsilon:
		for i in range(possibleactions.size):
			if max < qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],possibleactions[i]]:
				max = qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],possibleactions[i]]
				nextAction = possibleactions[i]
	else:
		nextAction = random.choice(possibleactions)
 	
	checkBoard = getNextBoardState(board,player,nextAction)
	checker = getNextBoardState(board, player,nextAction)
	nextState = getState(checkBoard)
	if hasWon(board,player):
		qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],nextAction] = (1-alpha)*qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],nextAction] + alpha*1#+#alpha*np.amax(qvals[nextState[0],nextState[1],nextState[2],nextState[3],nextState[4],nextState[5],nextState[6],nextState[7],nextState[8]],0)
	else:
		for l in range(9):
			if isValidAction(checker,l):
				test = getNextBoardState(checker,opp,l)
				testState = getState(test)
				if hasWon(test,opp):
					qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],nextAction] = (1-alpha)*qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],nextAction] - alpha*1
					qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],l] = (1-alpha)*qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],l] + alpha*1
			
		qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],nextAction] = (1-alpha)*qvals[state[0],state[1],state[2],state[3],state[4],state[5],state[6],state[7],state[8],nextAction] + alpha*np.amax(qvals[nextState[0],nextState[1],nextState[2],nextState[3],nextState[4],nextState[5],nextState[6],nextState[7],nextState[8]],0)
	return checkBoard

def chooseVals():
		print("You are X")
		return ['X','O']

########################################
comp = 'comp'
user = 'user'
qvals = qValInit()
qvals2 = qValInit()
inPlayauto = True
playerchar,compchar=['X','O']
compwins = 0
playerwins = 0
ties = 0	
	
for i in range(100000):
	board = boardInit()

	if random.randint(0,1) == 0:
		turn = comp
	else:
		turn = user

	while inPlayauto:
		if isBoardFull(board):
			ties = ties+1
			#print "Tie!!"
			break
		if(turn == user):
			board = getPlayerMoveauto(board)
			if hasWon(board,turn):
				playerwins = playerwins + 1
# 					print("You won!\n")
				break
			turn = comp
		else:
			board = evalNextStateforComp(board,comp,user)
			if hasWon(board,turn):
				compwins= compwins+1
				# print("You lost!")
				break
			turn = user


print("Computer won ",compwins)
print("Player won ",playerwins)
print("ties ",ties)


epsilon = 0.05
while True:
	board = boardInit()
	playerchar,compchar=chooseVals()
	if random.randint(0,1) == 0:
		turn = comp
	else:
		turn = user
	inPlay = True
	inPlayauto = False
	while inPlay:
		printBoard(board)
		if isBoardFull(board):
			print "Tie!!"
			break
		if(turn == user):
			board = getPlayerMove(board)
			if hasWon(board,turn):
				print("You won!\n")
				break
			turn = comp
		else:
			board = evalNextStateforComp(board,comp,user)
			if hasWon(board,turn):
				print("You lost!")
				break
			turn = user