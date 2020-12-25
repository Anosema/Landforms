import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import random, sys, time, pydirectinput
from pynput.keyboard import Key, Controller

keyboard = Controller()

def createGrid(width=5.0, length=5.0, precision=0.05):
	X = np.arange(-width , width , precision)
	Y = np.arange(-length, length, precision)
	x, y = np.meshgrid(X, Y)
	X, Y = np.rint(x), np.rint(y)
	height = 20

	nbr = 5
	z = 0

	for i in range(nbr):
		a = random.uniform(-width, width)
		b = random.uniform(-length, length)
		q = random.uniform(width, width*10)
		h = random.randint(int(height/10), height)
		z += h * np.exp(-((X - a)**2 + (Y - b)**2) / q)

	Z = np.rint(z)

	return (X, Y, Z)

def showStructure(grid):
	X, Y, Z = grid[0], grid[1], grid[2]
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	ax.plot_surface(X, Y, Z, cmap = cm.coolwarm)
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')
	plt.tight_layout()
	plt.show()


def saveCoos(grid):
	with open('X.txt', 'w') as file:
		for x in grid[0]:
			file.write("; ".join([str(i) for i in x]) + '\n')
	with open('Y.txt', 'w') as file:
		for y in grid[1]:
			file.write("; ".join([str(i) for i in y]) + '\n')
	with open('Z.txt', 'w') as file:
		for z in grid[2]:
			file.write("; ".join([str(i) for i in z]) + '\n')
		


def setStructure(grid):
	gridList = []
	t0 = time.time()
	print(len(grid[0])*len(grid[0][1]))
	time.sleep(5)

	for i in range(len(grid[0])):
		for blockIndex in range(len(grid[0][i])):
			x, z, y = grid[0][i][blockIndex], grid[1][i][blockIndex], grid[2][i][blockIndex]
			if (x, z, y) not in gridList: gridList.append((x, z, y)), print('Added')
			else: print('Not Added')
	print('Finished', len(gridList))

	time.sleep(5)

	for i in gridList:
		x, z, y = i[0], i[1], i[2]
		print(x, z, y)
		pydirectinput.keyDown('t')
		pydirectinput.keyUp('t')
		keyboard.type(f"/fill ~{x} 10 ~{z} ~{x} ~{y} ~{z} minecraft:stone\n")
		pydirectinput.keyDown('enter')
		pydirectinput.keyUp('enter')
		pydirectinput.keyDown('t')
		pydirectinput.keyUp('t')
		keyboard.type(f"/setblock ~{x} ~{y} ~{z} minecraft:grass_block\n")
		pydirectinput.keyDown('enter')
		pydirectinput.keyUp('enter')
	t1 = time.time()
	print(t1-t0 + 's')

grid = createGrid(50, 50, 1)
showStructure(grid)
setStructure(grid)

