# 1005031
# python 2.7.6

import copy
import pygame


class minMax:
	def __init__(self):
		print "\tPlayer First"
		
		
	def maxMove(self,state):
		global moveCount
		score = -2
		output, gameover, tie, win, lose = self.isGoal(state)

		if win or tie or lose:
			if win:
				score = 1
			elif lose:
				score = -1
			elif tie:
				score = 0
			return score

		for move in self.legalMoves(state, "X"):
			moveCount = moveCount+1
			score = max(score, self.minMove(move))
				
		return score


	def minMove(self, state):
		global moveCount
		score = 2
		output, gameover, tie, win, lose = self.isGoal(state)
	
		if win or tie or lose:
			if win:
				score = 1
			elif lose:
				score = -1
			elif tie:
				score = 0
			return score

		for move in self.legalMoves(state, "O"):
			moveCount = moveCount+1
			score = min(score, self.maxMove(move))

		return score
	

class Move(minMax):
	def __init__(self):
		minMax.__init__(self)
	
	
	def isGoal(self, board):
		tie = True
		win = False
		lose = False
		gameover = False

		for i in range(0,3):
			if board[i][0] == board[i][1] == board[i][2] == 'X' or board[0][i]==board[1][i]==board[2][i] == 'X':
				output = "Congratulation !! You Win."
				gameover = True
				win = True
				lose = False
			elif board[i][0] == board[i][1] == board[i][2] == 'O' or board[0][i]==board[1][i]==board[2][i] == 'O':
				output = "Alas !! You Lost.Please Try Again."
				gameover = True
				lose = True

		if gameover == False:
			if board[0][0] == board[1][1] == board[2][2] == 'X' or board[2][0]==board[1][1]==board[0][2] == 'X':
				output = "Congratulation !! You Win."
				gameover = True
				win = True
			elif board[0][0] == board[1][1] == board[2][2] == 'O' or board[2][0]==board[1][1]==board[0][2] == 'O':
				output = "Alas !! You Lost.Please Try Again."
				gameover = True
				lose = True
			elif tie == True:
				for row in board:
					for column in row:
						if column == None:
							tie = False
							gameover = False
							output = ""
				if tie == True:
					output = "It's a tie!"
					gameover = True
			else:
				output = ""
				gameover = False

		return output, gameover, tie, win, lose
	
	
	def legalMoves(self, board, option = ""):
		if option == "":
			if self.playerTurn == True:
				option = 'X'
			else:
				option = 'O'

		checkBoard = copy.deepcopy(board)
		moveList = []

		for i in range(3):
			for j in range(3):
				if checkBoard[i][j] == None:
					nextMoveCandidate = copy.deepcopy(checkBoard)
					nextMoveCandidate[i][j] = option
					moveList.append(nextMoveCandidate)

		return moveList


	def makeMove(self, state):
		possibleBoards = []
		nextMove = self.legalMoves(state, "O")
		foundWinner = False

		for move in nextMove:
			possibleBoards.append((move, self.maxMove(move)))
			output, gameover, tie, win, lose = self.isGoal(move)
			if lose:
				foundWinner = True
				winner = move

		possibleBoards.sort(key = lambda tempBoards: tempBoards[1])

		if foundWinner:
			self.board = winner
		else:
			self.board = possibleBoards[0][0]
		self.playerTurn = True
	
	
	def playerMove(self, row, column):
		if self.board[row][column] == None and self.playerTurn == True:
			self.board[row][column] = "X"
			self.playerTurn = False


	def aiMove(self):
		if self.playerTurn == False:
			pygame.time.delay(150)
			if self.board[1][1] == None:
				self.board[1][1] = 'O'
				return self.board
			elif self.board == [[None, None, None], [None, 'X', None], [None, None, None]]:
					self.board = [['O', None, None], [None, 'X', None], [None, None, None]]
					return self.board
			else:
				self.makeMove(self.board)
	
	
class ticTacToe(Move):
	def __init__(self):
		Move.__init__(self)
		self.board = [[None, None, None], [None, None, None], [None, None, None]]
		self.playerTurn = True
		self.font = pygame.font.Font(None, 45)
		self.gamePlay()


	def getPosition(self, mouseX,mouseY):
		if mouseY < 190:
			row = 0
		elif mouseY < 310:
			row = 1
		else:
			row = 2

		if mouseX < 190:
			column = 0
		elif mouseX < 310:
			column = 1
		else:
			column = 2

		return row, column

	
	def gui(self):
		screen.fill((50,50,50))
		pygame.draw.line(screen,(255,255,255),(70,190),(430,190),4)
		pygame.draw.line(screen,(255,255,255),(70,310),(430,310),4)
		pygame.draw.line(screen,(255,255,255),(190,70),(190,430),4)
		pygame.draw.line(screen,(255,255,255),(310,70),(310,430),4)

		for row in range(3):
			for column in range(3):
				placement = pygame.Rect(80 + column * 120, 80 + row * 120, 50, 50)
				if self.board[row][column] == 'X':
					screen.blit(placeX, placement)
				elif self.board[row][column] == 'O':
					screen.blit(placeO, placement)

		pygame.display.flip()
	
	
	def gamePlay(self):
		global running,leave
		while running:
			self.gui()
			output, gameover, tie, win, lose = self.isGoal(self.board)

			if gameover == True:
				print "\tGame over"
				endGame = self.font.render(output, True, (0, 255, 0), (0,0,0))
				endGame.set_colorkey((0,0,0))
				endResult = endGame.get_rect(centerx = width/2, centery = height / 2)
				screen.blit(endGame, endResult)
				pygame.display.flip()
				pygame.time.delay(1500)
				running = False

			if running == True and self.playerTurn == False:
				self.aiMove()
				self.gui()
				output, gameover, tie, win, lose = self.isGoal(self.board)
				self.playerTurn = True

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					leave = True
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouseX,mouseY = pygame.mouse.get_pos()
					row,column = self.getPosition(mouseX, mouseY)
					self.playerMove(row,column)

			pygame.display.flip()


if __name__ == "__main__" :
	count,moveCount = 0,0
	leave = False
	print "\nUsing Min Max Algorithm :\n"
	while True:
		count += 1
		print "Game Number : %d" % count
		pygame.font.init()
		
		width = 500
		height = 500
		running = True

		screen = pygame.display.set_mode((width, height))
		
		placeX = pygame.image.load('cross.bmp').convert()
		placeX = pygame.transform.scale(placeX, (100,100))
		placeX.set_colorkey((255,255,255))
		
		placeO = pygame.image.load('zero.bmp').convert()
		placeO = pygame.transform.scale(placeO, (100,100))
		placeO.set_colorkey((255,255,255))

		ticTacToe()
		
		print "\tTotal Move = %d" % moveCount
		moveCount = 0
		print
		
		if leave:
			print "Alas !! Game is Interruted. Now, Exiting ..."
			print
			break
