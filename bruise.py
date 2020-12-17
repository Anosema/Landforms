import random, sys, time
from pynput.keyboard import Key, Controller
keyboard = Controller()
c_end = '\x1b[0m'

colorList = ['\x1b[31m',
			 '\x1b[32m',
			 '\x1b[33m',
			 '\x1b[34m',
			 '\x1b[35m',
			 '\x1b[36m',
			 '\x1b[37m',
			 '\x1b[90m',
			 '\x1b[91m',
			 '\x1b[92m',
			 '\x1b[93m',
			 '\x1b[94m',
			 '\x1b[95m',
			 '\x1b[96m',
			 '\x1b[97m']

class Cell:
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.letter = 'X'
		self.changed = False
		self.depth = colorList.index(color)
		self.color = color
	def changeColor(self, color):
		self.color = color
		self.depth = colorList.index(color)
		self.changed = True

	def propagate(self, grid):
		adjacents = [(self.y-1, self.x  ),
					 (self.y+1, self.x  ),
					 (self.y  , self.x-1),
					 (self.y  , self.x+1)]

		for coords in adjacents:
			x, y = coords[0], coords[1]
			if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
				cell = grid[x][y]
				if random.getrandbits(1):
					cell.changeColor(self.color)
					if random.getrandbits(1):
						cell.propagate(grid)


def createGrid(width, length, size):
	middle = ((width//2), length//2)
	cellList = []
	for y in range(length):
		t = []
		for x in range(width):
			t.append(Cell(x, y, random.choice(colorList[0:size])))
		cellList.append(t)
	for i in range(width):
		for i in range(10):
			cell = random.choice(random.choice(cellList[0:size]))
			if not cell.changed:
				cell.propagate(cellList)
				break
	showGrid(cellList)
	saveGrid(cellList)
	time.sleep(4)
	for x in range(0, width):
		for z in range(0, length):
			y = cellList[z][x].depth
			keyboard.press('t')
			keyboard.release('t')
			keyboard.type(f"/setblock ~{x+1} ~{y+1} ~{z} minecraft:green_wool")
			keyboard.press(Key.enter)
			keyboard.release(Key.enter)






def saveGrid(grid):
	ttw = []
	for row in grid:
		ttw.append(" ".join([str(y.depth) for y in row]))
	with open('layers.txt', 'w') as file:
		file.write("\n".join(ttw))

def showGrid(grid):
	for x in grid:
		print(" ".join([y.color+y.letter+c_end for y in x]))


if len(sys.argv) != 4: print('Usage : python main.py [width] [length] [height]')
else: createGrid(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
