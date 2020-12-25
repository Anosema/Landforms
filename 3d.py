import random, sys, time, numpy

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from mpl_toolkits.mplot3d import axes3d

from pynput.keyboard import Key, Controller
# import pydirectinput

keyboard = Controller()

# class Relief:
	# def __init__(self,)
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Relief Generator')
		self.setFixedWidth (800)
		self.setFixedHeight(600)

		self.totalReliefs = 0

	# Options
		self.frameOptions = QFrame(self)
		self.frameOptions.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		self.frameOptions.setGeometry(0, 0, 200, 175)

		self.LabelTitleOptions = QLabel('Change Grid Config', self.frameOptions)
		self.LabelTitleOptions.setGeometry(5, 5, 190, 30)
		self.LabelTitleOptions.setAlignment(Qt.AlignCenter)
		self.LabelTitleOptions.setFont(QFont('Arial', 14))
	# Precision
		self.LabelTitlePrecision = QLabel('Precision', self.frameOptions)
		self.LabelTitlePrecision.setGeometry(5, 40, 150, 30)

		self.SliderPrecision = QSlider(self.frameOptions)
		self.SliderPrecision.setOrientation(Qt.Horizontal)
		self.SliderPrecision.setRange(1, 250)
		self.SliderPrecision.setValue(100)
		self.SliderPrecision.setGeometry(35, 70, 120, 30)
		self.SliderPrecision.valueChanged.connect(self.ChangePrecision)

		self.LabelTickPrecision = QLabel(str(self.SliderPrecision.value()), self.frameOptions)
		self.LabelTickPrecision.setGeometry(5, 60, 25, 30)

		self.ButtonReloadPrecision = QPushButton('R', self.frameOptions)
		self.ButtonReloadPrecision.clicked.connect(self.initGrid)
		self.ButtonReloadPrecision.setGeometry(160, 60, 25, 30)
	# Size
		self.LabelTitleSize = QLabel('Size', self.frameOptions)
		self.LabelTitleSize.setGeometry(5, 100, 150, 30)

		self.SliderSize = QSlider(self.frameOptions)
		self.SliderSize.setOrientation(Qt.Horizontal)
		self.SliderSize.setRange(1, 250)
		self.SliderSize.setValue(5)
		self.SliderSize.setGeometry(35, 130, 120, 30)
		self.SliderSize.valueChanged.connect(self.ChangeSize)

		self.LabelTickSize = QLabel(str(self.SliderSize.value()), self.frameOptions)
		self.LabelTickSize.setGeometry(5, 120, 25, 30)

		self.ButtonReloadSize = QPushButton('R', self.frameOptions)
		self.ButtonReloadSize.clicked.connect(self.initGrid)
		self.ButtonReloadSize.setGeometry(160, 120, 25, 30)
	# Reliefs
		self.frameReliefs = QFrame(self)
		self.frameReliefs.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		self.frameReliefs.setGeometry(0, 175, 200, 425)
		self.LabelTitleReliefs = QLabel('Add New Relief', self.frameReliefs)
		self.LabelTitleReliefs.setGeometry(5, 5, 190, 30)
		self.LabelTitleReliefs.setAlignment(Qt.AlignCenter)
		self.LabelTitleReliefs.setFont(QFont('Arial', 14))
	# Height
		self.LabelTitleHeight = QLabel('Height', self.frameReliefs)
		self.LabelTitleHeight.setGeometry(5, 40, 150, 30)

		self.SliderHeight = QSlider(self.frameReliefs)
		self.SliderHeight.setOrientation(Qt.Horizontal)
		self.SliderHeight.setRange(-250, 250)
		self.SliderHeight.setGeometry(35, 70, 120, 30)
		self.SliderHeight.valueChanged.connect(self.ChangeHeight)

		self.LabelTickHeight = QLabel(str(self.SliderHeight.value()), self.frameReliefs)
		self.LabelTickHeight.setGeometry(5, 60, 25, 30)

		self.ButtonVisualizeHeight = QPushButton('P', self.frameReliefs)
		self.ButtonVisualizeHeight.clicked.connect(self.visualize)
		self.ButtonVisualizeHeight.setGeometry(160, 60, 25, 30)
	# OffsetX
		self.LabelTitleOffsetX = QLabel('OffsetX', self.frameReliefs)
		self.LabelTitleOffsetX.setGeometry(5, 100, 150, 30)

		self.SliderOffsetX = QSlider(self.frameReliefs)
		self.SliderOffsetX.setOrientation(Qt.Horizontal)
		self.SliderOffsetX.setRange(-self.SliderSize.value(), self.SliderSize.value())
		self.SliderOffsetX.setGeometry(35, 130, 120, 30)
		self.SliderOffsetX.valueChanged.connect(self.ChangeOffsetX)

		self.LabelTickOffsetX = QLabel(str(self.SliderOffsetX.value()), self.frameReliefs)
		self.LabelTickOffsetX.setGeometry(5, 120, 25, 30)

		self.ButtonVisualizeOffsetX = QPushButton('P', self.frameReliefs)
		self.ButtonVisualizeOffsetX.clicked.connect(self.visualize)
		self.ButtonVisualizeOffsetX.setGeometry(160, 120, 25, 30)
	# OffsetY
		self.LabelTitleOffsetY = QLabel('OffsetY', self.frameReliefs)
		self.LabelTitleOffsetY.setGeometry(5, 160, 150, 30)

		self.SliderOffsetY = QSlider(self.frameReliefs)
		self.SliderOffsetY.setOrientation(Qt.Horizontal)
		self.SliderOffsetY.setRange(-self.SliderSize.value(), self.SliderSize.value())
		self.SliderOffsetY.setGeometry(35, 190, 120, 30)
		self.SliderOffsetY.valueChanged.connect(self.ChangeOffsetY)

		self.LabelTickOffsetY = QLabel(str(self.SliderOffsetY.value()), self.frameReliefs)
		self.LabelTickOffsetY.setGeometry(5, 180, 25, 30)

		self.ButtonVisualizeOffsetY = QPushButton('P', self.frameReliefs)
		self.ButtonVisualizeOffsetY.clicked.connect(self.visualize)
		self.ButtonVisualizeOffsetY.setGeometry(160, 180, 25, 30)
	# Q
		self.LabelTitleQ = QLabel('Q', self.frameReliefs)
		self.LabelTitleQ.setGeometry(5, 220, 150, 30)

		self.SliderQ = QSlider(self.frameReliefs)
		self.SliderQ.setOrientation(Qt.Horizontal)
		self.SliderQ.setRange(-50, 50)
		self.SliderQ.setValue(5)
		self.SliderQ.setGeometry(35, 250, 120, 30)
		self.SliderQ.valueChanged.connect(self.ChangeQ)

		self.LabelTickQ = QLabel(str(self.SliderQ.value()), self.frameReliefs)
		self.LabelTickQ.setGeometry(5, 240, 25, 30)

		self.ButtonVisualizeQ = QPushButton('P', self.frameReliefs)
		self.ButtonVisualizeQ.clicked.connect(self.visualize)
		self.ButtonVisualizeQ.setGeometry(160, 240, 25, 30)
	# Graph
		self.frameGraph = QFrame(self)
		self.frameGraph.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		self.frameGraph.setGeometry(200, 0, 600, 600)

		self.figure = plt.figure()
		self.figure.patch.set_facecolor('#F0F0F0')
		self.canvas  = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self.frameGraph)
		self.wid     = QWidget(self.frameGraph)
		self.layout  = QVBoxLayout()
		self.layout.addWidget(self.toolbar) 
		self.layout.addWidget(self.canvas) 
		self.wid.setLayout(self.layout)
	# Grid
		self.initGrid()

		
	def ChangePrecision(self):
		self.LabelTickPrecision.setText(str(self.SliderPrecision.value()))
	def ChangeSize(self):
		self.LabelTickSize.setText(str(self.SliderSize.value()))
		self.SliderOffsetX.setRange(-self.SliderSize.value(), self.SliderSize.value())
		self.SliderOffsetY.setRange(-self.SliderSize.value(), self.SliderSize.value())
	def ChangeHeight(self):
		self.LabelTickHeight.setText(str(self.SliderHeight.value()))
	def ChangeOffsetX(self):
		self.LabelTickOffsetX.setText(str(self.SliderOffsetX.value()))
	def ChangeOffsetY(self):
		self.LabelTickOffsetY.setText(str(self.SliderOffsetY.value()))
	def ChangeQ(self):
		self.LabelTickQ.setText(str(self.SliderQ.value()))
	def ChangeGrid(self):
		self.grid = self.initGrid()

	def initGrid(self):
		precision = self.SliderPrecision.value()/100
		size      = self.SliderSize     .value()
		Y = numpy.arange(-size, size+1, precision)
		X = numpy.arange(-size, size+1, precision)
		x, y = numpy.meshgrid(X, Y)
		X, Y = numpy.rint(x), numpy.rint(y)
		Z = numpy.array([[0 for x in range(len(X))] for y in range(len(Y))])
		self.grid = (X, Y, Z)
		self.showGrid(self.grid)
		

	def visualize(self):
		height  = self.SliderHeight .value()
		offsetX = self.SliderOffsetX.value()
		offsetY = self.SliderOffsetY.value()
		Q       = self.SliderQ      .value()
		self.z = 0
		if Q != 0:
			self.z = self.grid[2] + numpy.array(height * numpy.exp(-((self.grid[0] - offsetX)**2 + (self.grid[1] - offsetY)**2) / Q))
			self.showGrid((self.grid[0], self.grid[1], self.z))

	def addRelief(self):
		height  = self.SliderHeight .value()
		offsetX = self.SliderOffsetX.value()
		offsetY = self.SliderOffsetY.value()
		Q       = self.SliderQ      .value()
		if Q != 0:
			self.grid[2] += numpy.array(height * numpy.exp(-((self.grid[0] - offsetX)**2 + (self.grid[1] - offsetY)**2) / Q))
			self.showGrid((self.grid[0], self.grid[1], self.grid[2]))

	def showGrid(self, cells):
		X, Y, Z = cells[0], cells[1], cells[2]
		self.figure.clear()
		ax = self.figure.gca(projection='3d')
		ax.plot_surface(X, Y, Z, cmap = cm.coolwarm)
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		ax.patch.set_facecolor('#F0F0F0')
		self.canvas.draw()




def setStructure(grid):
	gridList = []
	t0 = time.time()
	for i in range(len(grid[0])):
		for blockIndex in range(len(grid[0][i])):
			x, z, y = grid[0][i][blockIndex], grid[1][i][blockIndex], grid[2][i][blockIndex]
			if (x, z, y) not in gridList: gridList.append((x, z, y))

	time.sleep(5)

	for i in gridList:
		x, z, y = i[0], i[1], i[2]
		print(x, z, y)
		pydirectinumpyut.keyDown('t')
		pydirectinumpyut.keyUp('t')
		keyboard.type(f"/fill ~{x} 10 ~{z} ~{x} ~{y} ~{z} minecraft:stone\n")
		pydirectinumpyut.keyDown('enter')
		pydirectinumpyut.keyUp('enter')
		pydirectinumpyut.keyDown('t')
		pydirectinumpyut.keyUp('t')
		keyboard.type(f"/setblock ~{x} ~{y} ~{z} minecraft:grass_block\n")
		pydirectinumpyut.keyDown('enter')
		pydirectinumpyut.keyUp('enter')
	t1 = time.time()
	process_time = t1-t0

app = QApplication(sys.argv)

window = MainWindow()

window.show()
app.exec_()
