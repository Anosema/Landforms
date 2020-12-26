import sys, numpy
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
		self.setFixedHeight(625)

	# Menu
		self.menu = self.menuBar()
		self.subMenuFile   = self.menu.addMenu('File')
		self.buttonOpen = QAction('Open plot', self)
		self.buttonOpen.triggered.connect(self.OpenFile)
		self.subMenuFile.addAction(self.buttonOpen)

		self.subMenuExport = self.subMenuFile.addMenu('Export')
		self.buttonExportTxt = QAction('Export as txt', self)
		self.buttonExportTxt.triggered.connect(self.ExportTXT)
		self.buttonExportLitematic = QAction('Export as Litematic', self)
		self.buttonExportLitematic.triggered.connect(self.ExportLMT)
		self.subMenuExport.addAction(self.buttonExportTxt), self.subMenuExport.addAction(self.buttonExportLitematic)




	# Options
		self.frameOptions = QFrame(self)
		self.frameOptions.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		self.frameOptions.setGeometry(0, 25, 200, 225)

		self.labelTitleOptions = QLabel('Change Grid Config', self.frameOptions)
		self.labelTitleOptions.setGeometry(5, 5, 190, 30)
		self.labelTitleOptions.setAlignment(Qt.AlignCenter)
		self.labelTitleOptions.setFont(QFont('Arial', 14))
	# Precision
		self.labelTitlePrecision = QLabel('Precision', self.frameOptions)
		self.labelTitlePrecision.setGeometry(5, 40, 150, 30)

		self.sliderPrecision = QSlider(self.frameOptions)
		self.sliderPrecision.setOrientation(Qt.Horizontal)
		self.sliderPrecision.setRange(1, 250)
		self.sliderPrecision.setValue(100)
		self.sliderPrecision.setGeometry(35, 70, 120, 30)
		self.sliderPrecision.valueChanged.connect(self.ChangePrecision)

		self.labelTickPrecision = QLabel(str(self.sliderPrecision.value()), self.frameOptions)
		self.labelTickPrecision.setGeometry(5, 60, 25, 30)

		self.buttonReloadPrecision = QPushButton('R', self.frameOptions)
		self.buttonReloadPrecision.clicked.connect(self.initGrid)
		self.buttonReloadPrecision.setGeometry(160, 60, 25, 30)
	# Size
		self.labelTitleSize = QLabel('Size', self.frameOptions)
		self.labelTitleSize.setGeometry(5, 100, 150, 30)

		self.sliderSize = QSlider(self.frameOptions)
		self.sliderSize.setOrientation(Qt.Horizontal)
		self.sliderSize.setRange(1, 250)
		self.sliderSize.setValue(5)
		self.sliderSize.setGeometry(35, 130, 120, 30)
		self.sliderSize.valueChanged.connect(self.ChangeSize)

		self.labelTickSize = QLabel(str(self.sliderSize.value()), self.frameOptions)
		self.labelTickSize.setGeometry(5, 120, 25, 30)

		self.buttonReloadSize = QPushButton('R', self.frameOptions)
		self.buttonReloadSize.clicked.connect(self.initGrid)
		self.buttonReloadSize.setGeometry(160, 120, 25, 30)
	# Reliefs
		self.frameReliefs = QFrame(self)
		self.frameReliefs.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		self.frameReliefs.setGeometry(0, 250, 200, 375)
		self.labelTitleReliefs = QLabel('Add New Relief', self.frameReliefs)
		self.labelTitleReliefs.setGeometry(5, 5, 190, 30)
		self.labelTitleReliefs.setAlignment(Qt.AlignCenter)
		self.labelTitleReliefs.setFont(QFont('Arial', 14))
	# Height
		self.labelTitleHeight = QLabel('Height', self.frameReliefs)
		self.labelTitleHeight.setGeometry(5, 40, 150, 30)

		self.sliderHeight = QSlider(self.frameReliefs)
		self.sliderHeight.setOrientation(Qt.Horizontal)
		self.sliderHeight.setRange(-250, 250)
		self.sliderHeight.setGeometry(35, 70, 120, 30)
		self.sliderHeight.valueChanged.connect(self.ChangeHeight)

		self.labelTickHeight = QLabel(str(self.sliderHeight.value()), self.frameReliefs)
		self.labelTickHeight.setGeometry(5, 60, 25, 30)

		self.buttonVisualizeHeight = QPushButton('P', self.frameReliefs)
		self.buttonVisualizeHeight.clicked.connect(self.visualize)
		self.buttonVisualizeHeight.setGeometry(160, 60, 25, 30)
	# OffsetX
		self.labelTitleOffsetX = QLabel('OffsetX', self.frameReliefs)
		self.labelTitleOffsetX.setGeometry(5, 100, 150, 30)

		self.sliderOffsetX = QSlider(self.frameReliefs)
		self.sliderOffsetX.setOrientation(Qt.Horizontal)
		self.sliderOffsetX.setRange(-self.sliderSize.value(), self.sliderSize.value())
		self.sliderOffsetX.setGeometry(35, 130, 120, 30)
		self.sliderOffsetX.valueChanged.connect(self.ChangeOffsetX)

		self.labelTickOffsetX = QLabel(str(self.sliderOffsetX.value()), self.frameReliefs)
		self.labelTickOffsetX.setGeometry(5, 120, 25, 30)

		self.buttonVisualizeOffsetX = QPushButton('P', self.frameReliefs)
		self.buttonVisualizeOffsetX.clicked.connect(self.visualize)
		self.buttonVisualizeOffsetX.setGeometry(160, 120, 25, 30)
	# OffsetY
		self.labelTitleOffsetY = QLabel('OffsetY', self.frameReliefs)
		self.labelTitleOffsetY.setGeometry(5, 160, 150, 30)

		self.sliderOffsetY = QSlider(self.frameReliefs)
		self.sliderOffsetY.setOrientation(Qt.Horizontal)
		self.sliderOffsetY.setRange(-self.sliderSize.value(), self.sliderSize.value())
		self.sliderOffsetY.setGeometry(35, 190, 120, 30)
		self.sliderOffsetY.valueChanged.connect(self.ChangeOffsetY)

		self.labelTickOffsetY = QLabel(str(self.sliderOffsetY.value()), self.frameReliefs)
		self.labelTickOffsetY.setGeometry(5, 180, 25, 30)

		self.buttonVisualizeOffsetY = QPushButton('P', self.frameReliefs)
		self.buttonVisualizeOffsetY.clicked.connect(self.visualize)
		self.buttonVisualizeOffsetY.setGeometry(160, 180, 25, 30)
	# Q
		self.labelTitleQ = QLabel('Q', self.frameReliefs)
		self.labelTitleQ.setGeometry(5, 220, 150, 30)

		self.sliderQ = QSlider(self.frameReliefs)
		self.sliderQ.setOrientation(Qt.Horizontal)
		self.sliderQ.setRange(-500, 500)
		self.sliderQ.setValue(5)
		self.sliderQ.setGeometry(35, 250, 120, 30)
		self.sliderQ.valueChanged.connect(self.ChangeQ)

		self.labelTickQ = QLabel(str(self.sliderQ.value()), self.frameReliefs)
		self.labelTickQ.setGeometry(5, 240, 25, 30)

		self.buttonVisualizeQ = QPushButton('P', self.frameReliefs)
		self.buttonVisualizeQ.clicked.connect(self.visualize)
		self.buttonVisualizeQ.setGeometry(160, 240, 25, 30)
	# Add & Build
		self.buttonAddRelief = QPushButton('Add Relief', self.frameReliefs)
		self.buttonAddRelief.clicked.connect(self.addRelief)
		self.buttonAddRelief.setGeometry(5, 350, 190, 30)

		self.buttonBuildRelief = QPushButton('Build in Minecraft', self.frameReliefs)
		self.buttonBuildRelief.clicked.connect(self.ExportLMT)
		self.buttonBuildRelief.setGeometry(5, 385, 190, 30)
	# Graph
		self.frameGraph = QFrame(self)
		self.frameGraph.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
		self.frameGraph.setGeometry(200, 25, 600, 600)

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
	def ExportTXT(self):
		filename = QFileDialog.getExistingDirectory(self, 'Choose Folder')
		if filename:
			Xttw, Yttw, Zttw = [], [], []
			filename += f'/Generator_{datetime.now().strftime("%d%m%Y_%H%M%S")}.txt'
			for i in range(len(self.grid[0])):
				Xttw.append(str(list(self.grid[0][i])))
				Yttw.append(str(list(self.grid[1][i])))
				Zttw.append(str(list(self.grid[2][i])))
			with open(filename, 'w') as file:
				file.write(('|'.join(Xttw)).replace('[', '').replace(']', '')+'\n')
				file.write(('|'.join(Yttw)).replace('[', '').replace(']', '')+'\n')
				file.write(('|'.join(Zttw)).replace('[', '').replace(']', ''))



	def OpenFile(self):
		filename = QFileDialog.getOpenFileName(self,"Load Archives","","Txt Files (*.txt)")[0]
		if filename:
			with open(filename, 'r') as file:
				content = file.readlines()
			Xline, Yline, Zline = content[0], content[1], content[2]
			tmp1, tmp2 = [], []
			for x in Xline.split('|'):
				for j in x.split(', '):
					tmp2.append(float(j))
				tmp1.append(tmp2)
			Xlist = numpy.array(tmp1)

			tmp1, tmp2 = [], []
			for y in Yline.split('|'):
				for j in y.split(', '):
					tmp2.append(float(j))
				tmp1.append(tmp2)
			Ylist = numpy.array(tmp1)

			tmp1, tmp2 = [], []
			for z in Zline.split('|'):
				for j in z.split(', '):
					tmp2.append(float(j))
				tmp1.append(tmp2)
			Zlist = numpy.array(tmp1)

			Z = numpy.array([[0 for x in range(len(X))] for y in range(len(Y))])

			Zlist += Z

			self.sliderSize.setValue(int(len(Xlist)/2))
			self.ChangeSize()
			self.grid = (Xlist, Ylist, Zlist)

			self.showGrid(self.grid)
	def ChangePrecision(self):
		self.labelTickPrecision.setText(str(self.sliderPrecision.value()))
	def ChangeSize(self):
		self.labelTickSize.setText(str(self.sliderSize.value()))
		self.sliderOffsetX.setRange(-self.sliderSize.value(), self.sliderSize.value())
		self.sliderOffsetY.setRange(-self.sliderSize.value(), self.sliderSize.value())
	def ChangeHeight(self):
		self.labelTickHeight.setText(str(self.sliderHeight.value()))
	def ChangeOffsetX(self):
		self.labelTickOffsetX.setText(str(self.sliderOffsetX.value()))
	def ChangeOffsetY(self):
		self.labelTickOffsetY.setText(str(self.sliderOffsetY.value()))
	def ChangeQ(self):
		self.labelTickQ.setText(str(self.sliderQ.value()))
	def ChangeGrid(self):
		self.grid = self.initGrid()

	def initGrid(self):
		precision = self.sliderPrecision.value()/100
		size      = self.sliderSize     .value()
		Y = numpy.arange(-size, size+1, precision)
		X = numpy.arange(-size, size+1, precision)
		x, y = numpy.meshgrid(X, Y)
		X, Y = numpy.rint(x), numpy.rint(y)
		Z = numpy.array([[0 for x in range(len(X))] for y in range(len(Y))])
		self.grid = (X, Y, Z)
		self.showGrid(self.grid)
	def visualize(self):
		height  = self.sliderHeight .value()
		offsetX = self.sliderOffsetX.value()
		offsetY = self.sliderOffsetY.value()
		Q       = self.sliderQ      .value()
		self.z = 0
		if Q != 0:
			self.z = self.grid[2] + numpy.array(height * numpy.exp(-((self.grid[0] - offsetX)**2 + (self.grid[1] - offsetY)**2) / Q))
			self.showGrid((self.grid[0], self.grid[1], self.z))
	def addRelief(self):
		height  = self.sliderHeight .value()
		offsetX = self.sliderOffsetX.value()
		offsetY = self.sliderOffsetY.value()
		Q       = self.sliderQ      .value()
		self.z = 0
		if Q != 0:
			self.z = self.grid[2] + numpy.array(height * numpy.exp(-((self.grid[0] - offsetX)**2 + (self.grid[1] - offsetY)**2) / Q))
			self.grid = (self.grid[0], self.grid[1], self.z)
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

	def ExportLMT(self):
		filename = QFileDialog.getExistingDirectory(self, 'Choose Folder')
		if filename:
			filename = filename.replace('/', '\\') + f'\\Generator_{datetime.now().strftime("%d%m%Y_%H%M%S")}.litematic'
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
	
			podzol     = BlockState("minecraft:podzol")
			coarseDirt = BlockState("minecraft:coarse_dirt")
			grass      = BlockState("minecraft:grass_block")
			Soils  = [grass, podzol, coarseDirt]
	
			stone       = BlockState("minecraft:stone")
			cobblestone = BlockState("minecraft:cobblestone")
			andesite    = BlockState("minecraft:andesite")
			gravel      = BlockState("minecraft:gravel")
			Stones = [stone, cobblestone, andesite, gravel, dirt]
	
			t0 = time()
			for i in gridList:
				x, z, y, block = i[0], i[1], i[2], choices(Soils, weights=(91, 3, 3), k=1)[0]
				reg.setblock(x, y, z, block)
				for j in range(y):
					block = choices(Stones, weights=(80, 5, 5, 5, 5), k=1)[0]
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
			self.initGrid()




app = QApplication(sys.argv)
app.setStyle('Fusion')

window = MainWindow()

window.show()
app.exec_()
