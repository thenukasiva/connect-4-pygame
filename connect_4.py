
import numpy as np
import pygame
import sys
import math

#colors for game
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#columns and rows of game.
ROW_COUNT = 6
COLUMN_COUNT = 7

#flips the original axis of pygame
def flip(m, axis):
    if not hasattr(m, 'ndim'):
        m = asarray(m)
    indexer = [slice(None)] * m.ndim
    try:
        indexer[axis] = slice(None, None, -1)
    except IndexError:
        raise ValueError("axis=%i is invalid for the %i-dimensional input array"
                         % (axis, m.ndim))
    return m[tuple(indexer)]

def create_gameBoard():
	gameBoard = np.zeros((ROW_COUNT,COLUMN_COUNT));
	return gameBoard

def add_piece(gameBoard, row, col, playerPiece):
	gameBoard[row][col] = playerPiece

def location_valid(gameBoard,col):
	return gameBoard[ROW_COUNT-1][col] == 0

def grab_next_free_row(gameBoard, col):
	for r in range(ROW_COUNT):
		if gameBoard[r][col] == 0:
			return r
	
def display_board(gameBoard):
	print(flip(gameBoard,0))

def winning_move(gameBoard, piece):
	#check horizontally for possible win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if gameBoard[r][c] == piece and gameBoard[r][c+1] == piece and gameBoard[r][c+2] and gameBoard[r][c+3] == piece:
				return True

	#check vertically for possible win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if gameBoard[r][c] == piece and gameBoard[r+1][c] == piece and gameBoard[r+2][c] and gameBoard[r+3][c] == piece:
				return True

	#check positive diagonal for possible win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if gameBoard[r][c] == piece and gameBoard[r+1][c+1] == piece and gameBoard[r+2][c+2] and gameBoard[r+3][c+3] == piece: 
				return True

	#check negative diagonal for possible win
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if gameBoard[r][c] == piece and gameBoard[r-1][c+1] == piece and gameBoard[r-2][c+2] and gameBoard[r-3][c+3] == piece: 
				return True

def draw_board(gameBoard):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			if gameBoard[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif gameBoard[r][c] == 2:
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


gameBoard = create_gameBoard();
print(gameBoard)
game_over = False

turn = 0
SQUARESIZE = 100

pygame.init()

width = COLUMN_COUNT * SQUARESIZE
height =(ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(gameBoard)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over: 
	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			pygame.display.quit()
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEMOTION: 
			pygame.draw.rect(screen, BLACK, (0,0, width,SQUARESIZE))
			posx = event.pos[0]
			if turn == 0: 
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW , (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width,SQUARESIZE))
			#player 1 
			if turn == 0: 
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if location_valid(gameBoard, col):
					row = grab_next_free_row(gameBoard,col)
					add_piece(gameBoard,row,col,1)

				if winning_move(gameBoard, 1):
					label = myfont.render("PLAYER 1 WINS", 1, RED)
					screen.blit(label, (40,10))
					game_over = True
			#player 2 
			else:	
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if location_valid(gameBoard, col):
					row = grab_next_free_row(gameBoard,col)
					add_piece(gameBoard,row,col,2)

				if winning_move(gameBoard, 1):
					label = myfont.render("PLAYER 2 WINS", 1, YELLOW)
					screen.blit(label, (40,10))
					game_over = True
					break

			display_board(gameBoard)
			draw_board(gameBoard)
			turn +=1
			turn = turn % 2 #helps alternate the turn by 0 and 1

			if game_over: 
				pygame.time.wait(3000)
				pygame.quit()
				sys.exit()
				


