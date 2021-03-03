from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMenu, QMenuBar, QAction
from sys import argv, exit

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import figure
from mpl_toolkits import mplot3d
from matplotlib import cm

from random import random
from math import floor, ceil
import numpy as np





class Vector2:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def dot(self, other):
		return self.x*other.x + self.y*other.y




class graphWidget(QWidget):
	def __init__(self, p):
		super().__init__(p)

		self.fig = figure()
		self.ax = self.fig.gca(projection='3d')
		self.ax.set_xlabel('X')
		self.ax.set_ylabel('Y')
		self.ax.set_zlabel('Z')
		self.ax.patch.set_facecolor('#F0F0F0')
		self.fig.patch.set_facecolor('#F0F0F0')

		self.canvas = FigureCanvas(self.fig)

		self.layout  = QVBoxLayout()
		self.layout.addWidget(self.canvas)
		self.setLayout(self.layout)

		self.createP()

	def createP(self):
		self.P = MakePermutation()

	def Noise2D(self, x, y):
		X = floor(x) & 255
		Y = floor(y) & 255

		xf = x - floor(x)
		yf = y - floor(y)

		topRight = Vector2(xf-1.0, yf-1.0)
		topLeft = Vector2(xf, yf-1.0)
		bottomRight = Vector2(xf-1.0, yf)
		bottomLeft = Vector2(xf, yf)


		valueTopRight = self.P[self.P[X+1]+Y+1]
		valueTopLeft  = self.P[self.P[X]+Y+1]
		valueBottomRight = self.P[self.P[X+1]+Y]
		valueBottomLeft  = self.P[self.P[X]+Y]

		dotTopRight = topRight.dot(GetConstantVector(valueTopRight))
		dotTopLeft  = topLeft.dot(GetConstantVector(valueTopLeft))
		dotBottomRight = bottomRight.dot(GetConstantVector(valueBottomRight))
		dotBottomLeft  = bottomLeft.dot(GetConstantVector(valueBottomLeft))

		u = Fade(xf)
		v = Fade(yf)

		return Lerp(u, Lerp(v, dotBottomLeft, dotTopLeft), Lerp(v, dotBottomRight, dotTopRight))

	def drawGraph(self, w=100, l=100, F=.005, A=1.0, hmax=100, oF=2.0, oA=.5, O=8):
		self.X, self.Y = np.meshgrid(np.arange(w), np.arange(l))
		self.Z = np.array([[0.0 for x in range(len(self.X))] for y in range(len(self.Y))])

		for x in range(w):
			for y in range(l):
				n = 0.0
				a = A
				f = F
				for o in range(O):
					v = a*self.Noise2D(x*f, y*f)
					n += v
					a *= oA
					f *= oF

				n += 1.0
				n *= 0.5
				rgb = round(hmax*n*.5)

				self.Z[y][x] = rgb

		elev, azim = self.ax.elev, self.ax.azim
		self.fig.clear()
		self.ax = self.fig.gca(projection='3d')
		self.ax.set_xlabel('X')
		self.ax.set_ylabel('Y')
		self.ax.set_zlabel('Z')
		self.ax.plot_surface(self.X, self.Y, self.Z, cmap = cm.coolwarm)
		self.ax.view_init(elev = elev, azim=azim)
		self.ax.patch.set_facecolor('#F0F0F0')
		self.canvas.draw()


class Main(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Landforms")
		self.setFixedSize(1000, 600)

		self.graph = graphWidget(self)
		self.setCentralWidget(self.graph)

		self.menubar = QMenuBar(self)
		self.menubar.setGeometry(0, 0, 100, 21)
		self.menubar.setStyleSheet("border: 1px solid white;")
		self.menuFile = QMenu("File", self.menubar)
		
		self.setMenuBar(self.menubar)

		self.actionNew = QAction("New", self)
		self.actionNew.triggered.connect(self.graph.drawGraph)
		self.menuFile.addAction(self.actionNew)



	# def resizeEvent(self, e):
	# 	self.graph.setGeometry(int(self.width()*(400/1000)), 20, int(self.width()*(600/1000)), self.height()-20)
	# 	self.menubar.setGeometry(0, 0, self.width(), 20)


Fade = lambda t: ((6*t - 15)*t + 10)*t*t*t
Lerp = lambda t, a1 ,a2: a1 + t*(a2-a1)

def Shuffle(tab):
	for e in range(len(tab)-1, 0, -1):
		index = round(random()*(e-1))
		temp  = tab[e]
		tab[e] = tab[index]
		tab[index] = temp

def MakePermutation():
	P = [x for x in range(256)]
	Shuffle(P)
	P += [P[x] for x in range(256)]
	return P

def GetConstantVector(v):
	h = v & 3
	if h == 0:
		return Vector2(1.0, 1.0)
	elif h == 1:
		return Vector2(-1.0, 1.0)
	elif h == 2:
		return Vector2(-1.0, -1.0)
	else:
		return Vector2(1.0, -1.0)




app = QApplication(argv)

mw = Main()
mw.show()

exit(app.exec_())