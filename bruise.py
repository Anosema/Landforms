import random, sys, time,  pydirectinput
from statistics import mean
from pynput.keyboard import Key, Controller

keyboard = Controller()


class Cell:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.letter = 'X'
		self.changed = False
		self.depth = 0
	def changeDepth(self, depth):
		self.depth = depth
		self.changed = True

	def checkDepths(self, grid):
		adjacents = [(self.y-1, self.x  ),
					 (self.y+1, self.x  ),
					 (self.y  , self.x-1),
					 (self.y  , self.x+1)]
		depthsList = []
		for coords in adjacents:
			x, y = coords[0], coords[1]
			if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
				cell = grid[x][y]
				depthsList.append(cell.depth)
		return depthsList


	def propagate(self, grid, size):
		adjacents = [(self.y-1, self.x  ),
					 (self.y+1, self.x  ),
					 (self.y  , self.x-1),
					 (self.y  , self.x+1)]

		for coords in adjacents:
			x, y = coords[0], coords[1]
			if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
				cell = grid[x][y]
				if random.getrandbits(1):
					depthsList = self.checkDepths(grid)
					depth = max(depthsList)-1
					if abs(depth) > size: depth += 1
					cell.changeDepth(depth)
					if random.getrandbits(1):
						cell.propagate(grid, size)


def createGrid(width, length, size):
	middle = ((width//2), length//2)
	cellList = []
	for y in range(length):
		t = []
		for x in range(width):
			t.append(Cell(x, y))
		cellList.append(t)
	for i in range(width):
		for j in range(10):
			cell = random.choice(random.choice(cellList))
			if not cell.changed:
				cell.propagate(cellList, size)
				break
	# saveGrid(cellList)
	# showGrid(cellList)
	setStructure(cellList)

def setStructure(grid):
	time.sleep(5)
	for x, row in enumerate(grid):
		for z, column in enumerate(row):
			y = column.depth
			pydirectinput.keyDown('t')
			pydirectinput.keyUp('t')
			keyboard.type(f"/fill ~{x+1} ~ ~{z} ~{x+1} ~{abs(y)} ~{z} minecraft:stone\n")
			pydirectinput.keyDown('enter')
			pydirectinput.keyUp('enter')
			pydirectinput.keyDown('t')
			pydirectinput.keyUp('t')
			keyboard.type(f"/setblock ~{x+1} ~{abs(y)+1} ~{z} minecraft:grass_block\n")
			pydirectinput.keyDown('enter')
			pydirectinput.keyUp('enter')






def saveGrid(grid):
	ttw = []
	for row in grid:
		ttw.append(" ".join([str(y.depth) for y in row]))
	with open('layers.txt', 'w') as file:
		file.write("\n".join(ttw))

def showGrid(grid):
	for x in grid:
		print(" ".join([str(y.depth) for y in x]))


if len(sys.argv) != 4: print('Usage : python main.py [width] [length] [height]')
else: createGrid(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
