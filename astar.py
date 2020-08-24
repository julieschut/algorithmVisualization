import pygame
import math
from queue import PriorityQueue


pygame.display.set_caption("A* Algorithm visualization")

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))


CRIMSON = (220,20,60)
TEAL = (0,128,128)
LIME = (0,255,0)
BLUE = 	(0,0,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
CYAN = 	(0,255,255)


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

	def make_end_node(self):
		self.colour = BLUE

	def make_path(self):
		self.colour = PURPLE

		# Drawing starts at top left of the screen
		# Passing width twice because the window is square
	def draw(self, win):
		pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, width))

	def update_adjacent_nodes(self):
		pass # Update later

	def __lt__(self, other):
		return False

# Heuristic function: the Manhattan distance between two nodes. 
def manhattan_heur(node1, node2):
	x1, y1 = node1
	x2, y2 = node2
	return abs(x1 - x2) + abs(y1 - y2)










