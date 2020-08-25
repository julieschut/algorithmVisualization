import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("A* Algorithm visualization")


CRIMSON = (220,20,60)
TEAL = (0,128,128)
LIME = (0,255,0)
BLUE = 	(0,0,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
CYAN = 	(0,255,255)
WHITE = (255,255,255)
GREY = (192,192,192)


class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = width * row # keeping track of coordinate position on the screen, drawing the node.
		self.y = width * col # ditto ^
		self.colour = WHITE
		self.neighbours = []
		self.width = width
		self.total_rows = total_rows

	def get_position(self):
		return self.row, self.col

	def evaluated(self): # if true, assumes that after visiting a node you mark it CRIMSON
		return self.colour == CRIMSON

	def optional(self): # if true, assumes that after visiting a node you mark it CRIMSON
		return self.colour == TEAL

	def is_start(self): # if true, assumes that after visiting a node you mark it CRIMSON
		return self.colour == CYAN

	def is_end(self): # if true, assumes that after visiting a node you mark it CRIMSON
		return self.colour == BLUE

	def reset(self):
		self.colour = WHITE

	def evaluate(self):
		self.colour = CRIMSON

	def make_optional(self):
		self.colour = TEAL

	def make_barrier(self):
		self.colour = BLACK

	def make_start_node(self):
		self.colour = CYAN

	def make_end_node(self):
		self.colour = BLUE

	def make_path(self):
		self.colour = PURPLE

		# Drawing starts at top left of the screen
		# Passing width twice because the window is square
	def draw(self, win):
		pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

	def update_adjacent_nodes(self):
		pass # Update later

	def __lt__(self, other):
		return False

# Heuristic function: the Manhattan distance between two nodes. 
def manhattan_heur(node1, node2):
	x1, y1 = node1
	x2, y2 = node2
	return abs(x1 - x2) + abs(y1 - y2)

def initialize_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
			grid.append([])
			for j in range(rows):
				node = Node(i, j, gap, rows)
				grid[i].append(node)
	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows): # draw horizontal lines
		pygame.draw.line(win, GREY, (0, i * gap),(width, i * gap))
		for j in range(rows): # draw vertical lines
			pygame.draw.line(win, GREY, (j * gap, 0),(j * gap, width))


# draw 
def draw(win, grid, rows, width):
	win.fill(WHITE) # At beginning of frame, draw over everything and redraw. Not efficient, improve later.

	for row in grid:
			for node in row:
					node.draw(win)
	draw_grid(win, rows, width)
	pygame.display.update()

# Capture mouse positions
def get_clicked_pos(position, rows, width):
	gap = width // rows 
	y, x = position
	# Determine which node the mouse was on basic on its coordinate by dividing by node width. 
	row = y // gap
	col = x // gap

	return row, col


# Main loop
def main(win, width):

	ROWS = 50;
	grid = initialize_grid(ROWS, width)

	start = None
	end = None

	run = True
	started = False

	while run: 
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False

			if started: # While the algorithms run, don't allow input
				continue

			if pygame.mouse.get_pressed()[0]: # left click
				position = pygame.mouse.get_pos()
				row, col = get_clicked_pos(position, ROWS, width)
				node = grid[row][col]
				if not start: # if start not set, do this firt
					start = node
					start.make_start_node()

				elif not end: 
					end = node
					end.make_end_node()

				elif node != end and node != start: 
					 node.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # right click
				pass

	pygame.quit()



main(WIN, WIDTH)
