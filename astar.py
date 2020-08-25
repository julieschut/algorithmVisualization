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

	def is_barrier(self):
		return self.colour == BLACK

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

	def update_adjacent_nodes(self, grid):
		self.neighbours = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Can we move down from this node?
			self.neighbours.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Can we move up from this node?
			self.neighbours.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # # Can we move right from this node?
			self.neighbours.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Can we move right from this node?
			self.neighbours.append(grid[self.row][self.col - 1])
	
	def __lt__(self, other):
		return False

# Heuristic function: the Manhattan distance between two nodes. 
def manhattan_heur(node1, node2):
	x1, y1 = node1
	x2, y2 = node2
	return abs(x1 - x2) + abs(y1 - y2)

def astar(draw, grid, start, end):
	
	count = 0 
	open_set = PriorityQueue()
	open_set.put((0, count, start)) # count is a tiebreaker for nodes with same score
	
	came_from = {} # keeps track of what node the optimal path came from
	
	g_score = {node: float("inf") for row in grid for node in row} # dictionary comprehension
	g_score[start] = 0 
	
	f_score = {node: float("inf") for row in grid for node in row} # dictionary comprehension
	f_score[start] = manhattan_heur(start.get_position(), end.get_position()) # The estimate of the distance

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current) # sync with PiorityQueue

		if current == end:	
			pass #make path
			return True 


		for neighbour in current.neighbours:

			temp_g_score = g_score[current] + 1 # assuming all edges are 1 

			if temp_g_score < g_score[neighbour]:
				came_from[neighbour] = current
				g_score[neighbour] = temp_g_score
				f_score[neighbour] = temp_g_score + manhattan_heur(neighbour.get_position(), end.get_position())
				
				if neighbour not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbour]), count, neighbour)
					open_set_hash.add(neighbour)

					neighbour.make_optional()

		
		draw()


		if current != start: 
			current.evaluate()

	return False

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
				
				if not start and node != end: # if start not set, do this firt
					start = node
					start.make_start_node()

				elif not end and node != start: 
					end = node
					end.make_end_node()

				elif node != end and node != start: 
					 node.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # right click
				position = pygame.mouse.get_pos()
				row, col = get_clicked_pos(position, ROWS, width)
				node = grid[row][col]
				node.reset()
				if node == start:
					start = None

				elif node == end:
					end = None 

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
									node.update_adjacent_nodes(grid)
					astar(lambda: draw(win, grid, ROWS, width), grid, start, end)




	pygame.quit()



main(WIN, WIDTH)


