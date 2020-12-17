import random, sys


class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.change_type('Water')

	def change_type(self, tp):
		self.type = tp
		if tp == 'Water': self.letter = ' '
		elif tp == 'Grass': self.letter = 'G'
		else: self.letter = str(tp)

	def propagate(self, grid, lastlyer, size):
		adjacents = [(self.y-1, self.x  ),
					 (self.y+1, self.x  ),
					 (self.y  , self.x-1),
					 (self.y  , self.x+1)]

		for coords in adjacents:
			x, y = coords[0], coords[1]
			if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
				cell = grid[x][y]
				if lastlyer[x][y].type != 'Water' and size > 0 and random.getrandbits(1):
					cell.change_type('Grass')
					cell.propagate(grid, lastlyer, (size-1))



def createGrid(width, length, height, size):
	middle = ((width//2), length//2)
	layers = []
	cellList = []
	for y in range(length):
		t = []
		for x in range(width):
			t.append(Cell(x, y))
			t[-1].change_type('Grass')
		cellList.append(t)
	layers.append(cellList)

	for layer in range(height):
		cellList = []
		for y in range(length):
			t = []
			for x in range(width):
				t.append(Cell(x, y))
			cellList.append(t)

		cellList[middle[0]][middle[1]].change_type('Grass')
		cellList[middle[0]][middle[1]].propagate(cellList, layers[-1], size)

		layers.append(cellList)
	saveLayers(layers)


def showGrid(grid):
	for x in grid:
		print(" ".join([y.letter for y in x]))



def saveLayers(layers):
	ttw = []
	for layer in layers:
		for row in layer:
			ttw.append(" ".join([y.letter for y in row]))
		ttw.append('='*(len(layers[0])*2))
	with open('layers.txt', 'w') as file:
		file.write("\n".join(ttw))



if len(sys.argv) != 5: print('Usage : python main.py [width] [length] [height] [size]')
else: createGrid(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
