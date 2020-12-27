import sys, numpy, json
from datetime import datetime
from os.path import expanduser
from random import choices
from time import time

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar 
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from mpl_toolkits.mplot3d import axes3d

from litemapy import Schematic, Region, BlockState



class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Relief Generator')
		self.setFixedWidth (800)
		self.setFixedHeight(630)

		self.f = lambda self, Ox, Oy, H, q: numpy.array(H * numpy.exp(-((self.grid[0] - Ox)**2 + (self.grid[1] - Oy)**2) / q))
	# Undo/Redo

	# Menu
		# self.menu = self.menuBar()
		self.menu = QToolBar(self)
		self.menu.setGeometry(0, 0, 800, 30)

		self.buttonOpen   = QAction(QApplication.style().standardIcon(QStyle.SP_DirOpenIcon)     , 'Open plot', self)
		self.buttonExport = QAction(QApplication.style().standardIcon(QStyle.SP_DialogSaveButton), 'Export as txt', self)
		self.undoAction   = QAction(QApplication.style().standardIcon(QStyle.SP_ArrowLeft)       , 'Undo', self)
		self.redoAction   = QAction(QApplication.style().standardIcon(QStyle.SP_ArrowRight)      , 'Redo', self)


		self.redoAction.setShortcut('Ctrl+Y')
		self.undoAction.setShortcut('Ctrl+Z')
		
		self.buttonOpen  .triggered.connect(self.OpenFile)
		self.buttonExport.triggered.connect(self.saveFile)
		self.undoAction  .triggered.connect(self.undo)
		self.redoAction  .triggered.connect(self.redo)
		
		self.menu.addAction(self.buttonOpen)
		self.menu.addAction(self.buttonExport)
		self.menu.addSeparator()
		self.menu.addAction(self.undoAction)
		self.menu.addAction(self.redoAction)
		
		self.menu.setFloatable(False), self.menu.setMovable(False)


	# Options
		self.frameOptions = QFrame(self)
		self.frameOptions.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		self.frameOptions.setGeometry(0, 30, 200, 225)
		self.labelTitleOptions = QLabel('Change Grid Config', self.frameOptions)
		self.labelTitleOptions.setGeometry(5, 5, 190, 30)
		self.labelTitleOptions.setAlignment(Qt.AlignCenter)
		self.labelTitleOptions.setFont(QFont('Arial', 14))
	# Precision
		self.labelTitlePrecision = QLabel('Precision', self.frameOptions)
		self.labelTitlePrecision.setGeometry(15, 40, 150, 30)
		self.sliderPrecision = QSlider(self.frameOptions)
		self.sliderPrecision.setOrientation(Qt.Horizontal)
		self.sliderPrecision.setRange(1, 250)
		self.sliderPrecision.setValue(100)
		self.sliderPrecision.setGeometry(45, 70, 120, 30)
		self.sliderPrecision.valueChanged.connect(self.ChangePrecision)
		self.labelTickPrecision = QLabel(str(self.sliderPrecision.value()), self.frameOptions)
		self.labelTickPrecision.setGeometry(15, 60, 25, 30)
	# Size
		self.labelTitleSize = QLabel('Size', self.frameOptions)
		self.labelTitleSize.setGeometry(15, 100, 150, 30)
		self.sliderSize = QSlider(self.frameOptions)
		self.sliderSize.setOrientation(Qt.Horizontal)
		self.sliderSize.setRange(1, 250)
		self.sliderSize.setValue(5)
		self.sliderSize.setGeometry(45, 130, 120, 30)
		self.sliderSize.valueChanged.connect(self.ChangeSize)
		self.labelTickSize = QLabel(str(self.sliderSize.value()), self.frameOptions)
		self.labelTickSize.setGeometry(15, 120, 25, 30)
	# Reload
		self.buttonResetGrid = QPushButton('Reset Grid', self.frameOptions)
		self.buttonResetGrid.clicked.connect(self.resetGrid)
		self.buttonResetGrid.setGeometry(5, 160, 190, 30)

		self.buttonReloadGrid = QPushButton('Reload Grid', self.frameOptions)
		self.buttonReloadGrid.clicked.connect(self.initGrid)
		self.buttonReloadGrid.setGeometry(5, 190, 190, 30)

	# Reliefs
		self.frameReliefs = QFrame(self)
		self.frameReliefs.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		self.frameReliefs.setGeometry(0, 255, 200, 375)
		self.labelTitleReliefs = QLabel('Add New Relief', self.frameReliefs)
		self.labelTitleReliefs.setGeometry(5, 5, 190, 30)
		self.labelTitleReliefs.setAlignment(Qt.AlignCenter)
		self.labelTitleReliefs.setFont(QFont('Arial', 14))
	# Height
		self.labelTitleHeight = QLabel('Height', self.frameReliefs)
		self.labelTitleHeight.setGeometry(15, 40, 150, 30)
		self.sliderHeight = QSlider(self.frameReliefs)
		self.sliderHeight.setOrientation(Qt.Horizontal)
		self.sliderHeight.setRange(-250, 250)
		self.sliderHeight.setGeometry(45, 70, 120, 30)
		self.sliderHeight.valueChanged.connect(self.ChangeHeight)
		self.labelTickHeight = QLabel(str(self.sliderHeight.value()), self.frameReliefs)
		self.labelTickHeight.setGeometry(15, 60, 25, 30)
	# OffsetX
		self.labelTitleOffsetX = QLabel('OffsetX', self.frameReliefs)
		self.labelTitleOffsetX.setGeometry(15, 100, 150, 30)

		self.sliderOffsetX = QSlider(self.frameReliefs)
		self.sliderOffsetX.setOrientation(Qt.Horizontal)
		self.sliderOffsetX.setRange(-self.sliderSize.value(), self.sliderSize.value())
		self.sliderOffsetX.setGeometry(45, 130, 120, 30)
		self.sliderOffsetX.valueChanged.connect(self.ChangeOffsetX)

		self.labelTickOffsetX = QLabel(str(self.sliderOffsetX.value()), self.frameReliefs)
		self.labelTickOffsetX.setGeometry(15, 120, 25, 30)
	# OffsetY
		self.labelTitleOffsetY = QLabel('OffsetY', self.frameReliefs)
		self.labelTitleOffsetY.setGeometry(15, 160, 150, 30)

		self.sliderOffsetY = QSlider(self.frameReliefs)
		self.sliderOffsetY.setOrientation(Qt.Horizontal)
		self.sliderOffsetY.setRange(-self.sliderSize.value(), self.sliderSize.value())
		self.sliderOffsetY.setGeometry(45, 190, 120, 30)
		self.sliderOffsetY.valueChanged.connect(self.ChangeOffsetY)

		self.labelTickOffsetY = QLabel(str(self.sliderOffsetY.value()), self.frameReliefs)
		self.labelTickOffsetY.setGeometry(15, 180, 25, 30)
	# Q
		self.labelTitleQ = QLabel('Q', self.frameReliefs)
		self.labelTitleQ.setGeometry(15, 220, 150, 30)

		self.sliderQ = QSlider(self.frameReliefs)
		self.sliderQ.setOrientation(Qt.Horizontal)
		self.sliderQ.setRange(-500, 500)
		self.sliderQ.setValue(5)
		self.sliderQ.setGeometry(45, 250, 120, 30)
		self.sliderQ.valueChanged.connect(self.ChangeQ)

		self.labelTickQ = QLabel(str(self.sliderQ.value()), self.frameReliefs)
		self.labelTickQ.setGeometry(15, 240, 25, 30)
	# Visualize & Add
		self.radioButtonLive = QRadioButton('Live Render', self.frameReliefs)
		self.radioButtonLive.setGeometry(5, 280, 190, 30)

		self.buttonVisRelief = QPushButton('Visualize', self.frameReliefs)
		self.buttonVisRelief.clicked.connect(self.visualizeRelief)
		self.buttonVisRelief.setGeometry(5, 310, 190, 30)

		self.buttonAddRelief = QPushButton('Add Relief', self.frameReliefs)
		self.buttonAddRelief.clicked.connect(self.addRelief)
		self.buttonAddRelief.setGeometry(5, 340, 190, 30)

	# Graph
		self.frameGraph = QFrame(self)
		self.frameGraph.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		self.frameGraph.setGeometry(200, 30, 600, 600)
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
		self.reliefs, self.oldReliefs = [], []
		self.initGrid()

	def ChangePrecision(self):
		self.labelTickPrecision.setText(str(self.sliderPrecision.value()))
	def ChangeSize(self):
		self.labelTickSize.setText(str(self.sliderSize.value()))
		self.sliderOffsetX.setRange(-self.sliderSize.value(), self.sliderSize.value())
		self.sliderOffsetY.setRange(-self.sliderSize.value(), self.sliderSize.value())
	def ChangeHeight(self):
		self.labelTickHeight.setText(str(self.sliderHeight.value()))
		if self.radioButtonLive.isChecked(): self.visualizeRelief()
	def ChangeOffsetX(self):
		self.labelTickOffsetX.setText(str(self.sliderOffsetX.value()))
		if self.radioButtonLive.isChecked(): self.visualizeRelief()
	def ChangeOffsetY(self):
		self.labelTickOffsetY.setText(str(self.sliderOffsetY.value()))
		if self.radioButtonLive.isChecked(): self.visualizeRelief()
	def ChangeQ(self):
		self.labelTickQ.setText(str(self.sliderQ.value()))
		if self.radioButtonLive.isChecked(): self.visualizeRelief()

	def resetGrid(self):
		self.reliefs = []
		self.initGrid()

	def undo(self):
		if self.reliefs != []: self.oldReliefs.append(self.reliefs.pop()), self.initGrid()
	def redo(self):
		if self.oldReliefs != []: self.reliefs.append(self.oldReliefs.pop()), self.initGrid()

	def initGrid(self):
		precision = self.sliderPrecision.value()/100
		size      = self.sliderSize     .value()
		Y = numpy.arange(-size, size+1, precision)
		X = numpy.arange(-size, size+1, precision)
		x, y = numpy.meshgrid(X, Y)
		X, Y = numpy.rint(x), numpy.rint(y)
		Z = numpy.array([[0 for x in range(len(X))] for y in range(len(Y))])
		self.grid = [X, Y, Z]
		for i in self.reliefs: self.grid[2] = self.grid[2] + self.f(self, i[0], i[1], i[2], i[3])
		self.showGrid(self.grid)
	def visualizeRelief(self):
		offsetX = self.sliderOffsetX.value()
		offsetY = self.sliderOffsetY.value()
		height  = self.sliderHeight .value()
		Q       = self.sliderQ      .value()
		if Q != 0:
			self.z = self.grid[2] + self.f(self, offsetX, offsetY, height, Q)
			self.showGrid((self.grid[0], self.grid[1], self.z))
	def addRelief(self):
		offsetX = self.sliderOffsetX.value()
		offsetY = self.sliderOffsetY.value()
		height  = self.sliderHeight .value()
		Q       = self.sliderQ      .value()
		if Q != 0:
			self.reliefs.append((offsetX, offsetY, height, Q))
			self.z = self.grid[2] + self.f(self, offsetX, offsetY, height, Q)
			self.grid = [self.grid[0], self.grid[1], self.z]
			self.showGrid(self.grid)
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
	def OpenFile(self):
		filename = QFileDialog.getOpenFileName(self,"Load Archives","","Txt Files (*.txt)")[0]
		if filename:
			with open(filename, 'r') as file:
				content = file.readlines()
			Xline, Yline, Zline, Rline = content[0], content[1], content[2], content[3]
			tmp1 = []
			for x in Xline.split('|'):
				tmp2 = []
				for j in x.split(', '):
					tmp2.append(float(j))
				tmp1.append(tmp2)
			Xlist = numpy.array(tmp1)

			tmp1 = []
			for y in Yline.split('|'):
				tmp2 = []
				for j in y.split(', '):
					tmp2.append(float(j))
				tmp1.append(tmp2)
			Ylist = numpy.array(tmp1)

			tmp1 = []
			for z in Zline.split('|'):
				tmp2 = []
				for j in z.split(', '):
					tmp2.append(float(j))
				tmp1.append(tmp2)
			Zlist = numpy.array(tmp1)

			tmp1 = []
			for r in Rline.split('|'):
				tmp2 = []
				for j in r.split(', '):
					tmp2.append(float(j))
				tmp1.append(tuple(tmp2))
			self.reliefs = tmp1

			self.sliderSize.setValue(int(len(Xlist)/2))
			self.ChangeSize()
			self.grid = [Xlist, Ylist, Zlist]
			self.showGrid(self.grid)
	def saveFile(self):
		filename = QFileDialog.getSaveFileName(self,"Save Schematic","","Litematic Files (*.litematic);;Txt Files (*.txt)")
		if filename[0]:
			if '.litematic' in filename[1]: self.ExportLMT(filename[0])
			else: self.ExportTXT(filename[0])
	def ExportLMT(self, filename):
		if '.litematic' not in filename: filename += '.litematic'
		gridList = []
		maxi = 0
		for i in range(len(self.grid[0])):
			self.grid[0][i] += (len(self.grid[0][i]))/2
			self.grid[1][i] += (len(self.grid[1][i]))/2
			self.grid[2][i] += (len(self.grid[2][i]))/2
			for j in range(len(self.grid[0][i])):
				x, z, y = self.grid[0][i][j], self.grid[1][i][j], self.grid[2][i][j]
				if int(y) > maxi: maxi = int(y)
				if (x, z, y) not in gridList: gridList.append([int(x), int(z), int(y)])

		schem = Schematic(len(self.grid[0]), (maxi+1), len(self.grid[0]), name="ReliefGen", author="Anosema", description="Made with ReliefGenerator", main_region_name="Main")
		reg = schem.regions["Main"]

		with open('config.json', 'r') as file:
			data = json.load(file)
		Soils = [BlockState(x['id']) for x in data['soil']]
		SoilsWeights = tuple([x['weight'] for x in data['soil']])

		Stones = [BlockState(x['id']) for x in data['underground']]
		StonesWeights = tuple([x['weight'] for x in data['underground']])

		t0 = time()
		for i in gridList:
			x, z, y, block = i[0], i[1], i[2], choices(Soils, weights=SoilsWeights, k=1)[0]
			reg.setblock(x, y, z, block)
			for j in range(y):
				block = choices(Stones, weights=StonesWeights, k=1)[0]
				reg.setblock(x, j, z, block)
		schem.save(filename)
		t1 = time()
		process_time = t1-t0
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Your Litematic is ready, finished in")
		msg.setInformativeText(str(int(process_time*10)/10) + 's')
		msg.setWindowTitle("Finished")
		msg.show()
		msg.exec_()

	def ExportTXT(self, filename):
		if '.txt' not in filename: filename += '.txt'
		Xttw, Yttw, Zttw, Rttw = [], [], [], []
		for i in range(len(self.grid[0])):
			Xttw.append(str(list(self.grid[0][i])))
			Yttw.append(str(list(self.grid[1][i])))
			Zttw.append(str(list(self.grid[2][i])))
		for i in self.reliefs:
			Rttw.append(str(list(i)))
		with open(filename, 'w') as file:
			file.write(('|'.join(Xttw)).replace('[', '').replace(']', '')+'\n')
			file.write(('|'.join(Yttw)).replace('[', '').replace(']', '')+'\n')
			file.write(('|'.join(Zttw)).replace('[', '').replace(']', '')+'\n')
			file.write(('|'.join(Rttw)).replace('[', '').replace(']', ''))
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Your Save is ready")
		msg.setWindowTitle("Finished")
		msg.show()
		msg.exec_()




app = QApplication(sys.argv)
app.setStyle('Fusion')

window = MainWindow()

window.show()
app.exec_()
