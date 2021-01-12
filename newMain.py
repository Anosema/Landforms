from numpy import meshgrid, arange, array, exp
from numpy import maximum as maxima
from numpy import minimum as minima
from os import name, system, getcwd
from PyQt5.QtWidgets import *
from json import dump, loads
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from time import time

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

from litemapy import Schematic, Region, BlockState





class Peak():
	def __init__(self, Ox, Oy, Oz, H, Q, X, Y):
		X, Y = meshgrid(X, Y)
		self.dict = {"OffsetX": Ox, "OffsetY": Oy, "OffsetZ": Oz, "Height": H, "q": Q}
		self.points = array((H * exp(-((X - Ox)**2 + (Y - Oy)**2) / Q)) + Oz)

class NewGridWindow(QDialog):
	def __init__(self, parent):
		super(NewGridWindow, self).__init__(parent)
		self.setWindowFlags(Qt.Drawer)
		self.setFixedWidth(300)
		self.setFixedHeight(110)
		self.setWindowTitle("New Grid")

		self.parent = parent

		self.label = QLabel('Grid Size :', self)
		self.label.setGeometry(5, 5, 140, 30)
		self.spin = QSpinBox(self)
		self.spin.setGeometry(155, 5, 140, 30)
		self.spin.setMinimum(1)
		self.spin.setValue(self.parent.totalPeaks["SideSize"])

		self.buttonValid = QPushButton('Create', self)
		self.buttonValid.setGeometry(5, 75, 290, 30)
		self.buttonValid.clicked.connect(self.ask)


	def actuallyShow(self):
		self.setWindowModality(Qt.ApplicationModal)
		self.setFocusPolicy(Qt.StrongFocus)
		self.activateWindow()
		self.setFocus(True)
		self.raise_()
		self.show()

	def ask(self):
		buttonReply = QMessageBox.question(self, 'Are you sure ?', 'Any unsaved changes will be destroyed', QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
		if buttonReply == QMessageBox.Yes:
			self.parent.initGrid(size = self.spin.value())
			self.hide()


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		self.setWindowTitle('Landform Generator')
		self.setFixedWidth(800)
		self.setFixedHeight(622)

		self.system = 0 if name == 'posix' else 1 

		self.oldReliefs = []

		self.totalPeaks = {}
		self.totalPeaks["SideSize"] = 5
		self.totalPeaks["Peaks"] = []

	# UI

		self.gridWindow = NewGridWindow(self)

		self.centralwidget = QWidget(self)
		self.frameGraph = QFrame(self.centralwidget)
		self.frameGraph.setGeometry(200, 0, 600, 600)
		self.frameGraph.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)

		self.widgetGraph = QWidget(self.frameGraph)
		self.widgetGraph.setGeometry(0, 0, 600, 600)

		self.figure = plt.figure()
		self.figure.patch.set_facecolor('#F0F0F0')
		self.canvas  = FigureCanvas(self.figure)
		self.toolbar = NavigationToolbar(self.canvas, self.frameGraph)
		self.layout  = QVBoxLayout()
		self.layout.addWidget(self.toolbar) 
		self.layout.addWidget(self.canvas) 
		self.widgetGraph.setLayout(self.layout)






		self.frameOption = QFrame(self.centralwidget)
		self.frameOption.setGeometry(0, 0, 200, 600)
		self.frameOption.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)


		self.spinOffsetX = QSpinBox(self.frameOption)
		self.spinOffsetX.setGeometry(5, 30, 150, 20)
		self.spinOffsetX.setMaximum(100)
		self.labelTitleOffsetX = QLabel("Offset X", self.frameOption)
		self.labelTitleOffsetX.setGeometry(5, 5, 190, 25)
		self.labelTitleOffsetX.setAlignment(Qt.AlignCenter)
		self.labelMaxOffsetX = QLabel("100", self.frameOption)
		self.labelMaxOffsetX.setGeometry(160, 30, 35, 20)
		self.labelMaxOffsetX.setAlignment(Qt.AlignCenter)

		self.labelTitleOffsetY = QLabel("Offset Y", self.frameOption)
		self.labelTitleOffsetY.setGeometry(5, 55, 190, 25)
		self.labelTitleOffsetY.setAlignment(Qt.AlignCenter)
		self.labelMaxOffsetY = QLabel("100", self.frameOption)
		self.labelMaxOffsetY.setGeometry(160, 80, 35, 20)
		self.labelMaxOffsetY.setAlignment(Qt.AlignCenter)
		self.spinOffsetY = QSpinBox(self.frameOption)
		self.spinOffsetY.setGeometry(5, 80, 150, 20)
		self.spinOffsetY.setMaximum(100)

		self.labelTitleOffsetZ = QLabel("Offset Z", self.frameOption)
		self.labelTitleOffsetZ.setGeometry(5, 105, 190, 25)
		self.labelTitleOffsetZ.setAlignment(Qt.AlignCenter)
		self.labelMaxOffsetZ = QLabel("250", self.frameOption)
		self.labelMaxOffsetZ.setGeometry(160, 130, 35, 20)
		self.labelMaxOffsetZ.setAlignment(Qt.AlignCenter)
		self.spinOffsetZ = QSpinBox(self.frameOption)
		self.spinOffsetZ.setGeometry(5, 130, 150, 20)
		self.spinOffsetZ.setRange(-250, 250)

		self.labelTitleHeight = QLabel("Height", self.frameOption)
		self.labelTitleHeight.setGeometry(5, 155, 190, 25)
		self.labelTitleHeight.setAlignment(Qt.AlignCenter)
		self.labelMaxHeight = QLabel("250", self.frameOption)
		self.labelMaxHeight.setGeometry(160, 180, 35, 20)
		self.labelMaxHeight.setAlignment(Qt.AlignCenter)
		self.spinHeight = QSpinBox(self.frameOption)
		self.spinHeight.setGeometry(5, 180, 150, 20)
		self.spinHeight.setRange(-250, 250)

		self.labelTitleQ = QLabel("Q", self.frameOption)
		self.labelTitleQ.setGeometry(5, 205, 190, 25)
		self.labelTitleQ.setAlignment(Qt.AlignCenter)
		self.labelMaxQ = QLabel("500", self.frameOption)
		self.labelMaxQ.setGeometry(160, 230, 35, 20)
		self.labelMaxQ.setAlignment(Qt.AlignCenter)
		self.spinQ = QSpinBox(self.frameOption)
		self.spinQ.setGeometry(5, 230, 150, 20)
		self.spinQ.setRange(1, 500)

		self.line = QFrame(self.frameOption)
		self.line.setGeometry(5, 255, 190, 5)
		self.line.setFrameShape(QFrame.HLine)
		self.line.setFrameShadow(QFrame.Sunken)
		self.buttonVizualise = QPushButton("Vizualise Relief", self.frameOption)
		self.buttonVizualise.setGeometry(5, 265, 190, 25)
		self.buttonVizualise.clicked.connect(self.showGrid)

		self.buttonAddRelief = QPushButton("Add Relief", self.frameOption)
		self.buttonAddRelief.setGeometry(6, 295, 190, 25)
		self.buttonAddRelief.clicked.connect(lambda: self.showGrid(True))

		self.setCentralWidget(self.centralwidget)
		self.menubar = QMenuBar(self)
		self.menubar.setGeometry(0, 0, 800, 21)
		self.menuFile = QMenu("File", self.menubar)
		self.menuConfig = QMenu("Config", self.menubar)
		self.menuEdit = QMenu("Edit", self.menubar)
		self.setMenuBar(self.menubar)

		self.actionNew = QAction(QApplication.style().standardIcon(QStyle.SP_FileIcon), "New", self)
		self.actionNew.setPriority(QAction.HighPriority)
		self.actionNew.triggered.connect(self.newGrid)
		self.actionNew.setShortcut('Ctrl+N')

		self.actionOpenFile = QAction(QApplication.style().standardIcon(QStyle.SP_DirOpenIcon), "Open File", self)
		self.actionOpenFile.setPriority(QAction.HighPriority)
		self.actionOpenFile.triggered.connect(self.openFile)
		self.actionOpenFile.setShortcut('Ctrl+O')

		self.actionSaveAs = QAction(QApplication.style().standardIcon(QStyle.SP_DialogSaveButton),"Save As...", self)
		self.actionSaveAs.setPriority(QAction.HighPriority)
		self.actionSaveAs.triggered.connect(self.saveFile)
		self.actionSaveAs.setShortcut('Ctrl+Shift+S')

		self.actionEditLitematicConfig = QAction("Litematic Settings", self)
		self.actionEditLitematicConfig.triggered.connect(self.openConfig)
		self.actionEditLitematicConfig.setPriority(QAction.HighPriority)

		self.actionUndo = QAction(QApplication.style().standardIcon(QStyle.SP_ArrowLeft), "Undo", self)
		self.actionUndo.setPriority(QAction.HighPriority)
		self.actionUndo.triggered.connect(self.undo)
		self.actionUndo.setShortcut('Ctrl+Z')

		self.actionRedo = QAction(QApplication.style().standardIcon(QStyle.SP_ArrowRight), "Redo", self)
		self.actionRedo.setPriority(QAction.HighPriority)
		self.actionRedo.triggered.connect(self.redo)
		self.actionRedo.setShortcut('Ctrl+Y')

		self.actionLiveRender = QAction("Live Render", self)
		self.actionLiveRender.triggered.connect(self.toggleLive)
		self.actionLiveRender.setPriority(QAction.HighPriority)
		self.actionLiveRender.setShortcut('Ctrl+L')
		self.actionLiveRender.setCheckable(True)


		self.menuFile.addAction(self.actionNew)
		self.menuFile.addAction(self.actionOpenFile)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionSaveAs)
		self.menuConfig.addAction(self.actionEditLitematicConfig)
		self.menuEdit.addAction(self.actionUndo)
		self.menuEdit.addAction(self.actionRedo)
		self.menuEdit.addAction(self.actionLiveRender)
		self.menubar.addAction(self.menuFile.menuAction())
		self.menubar.addAction(self.menuEdit.menuAction())
		self.menubar.addAction(self.menuConfig.menuAction())


		self.updateRange()


	def newGrid(self):
		self.gridWindow.actuallyShow()

	def initGrid(self, size=None, opened=False):
		if opened:
			while type(self.totalPeaks['Peaks'][0]) is dict:
				peak = self.totalPeaks['Peaks'].pop(0)
				self.totalPeaks['Peaks'].append(Peak(peak["OffsetX"], peak["OffsetY"], peak["OffsetZ"], peak["Height"], peak["q"], arange(self.totalPeaks['SideSize']), arange(self.totalPeaks['SideSize'])))
		else:
			self.totalPeaks['SideSize'] = size
			self.totalPeaks['Peaks'] = []


		self.updateRange()
		self.showGrid()

	def showGrid(self, toAdd = False, do = True):
		X, Y = meshgrid(arange(self.totalPeaks['SideSize']), arange(self.totalPeaks['SideSize']))
		Z = array([[0.0 for x in range(len(X))] for y in range(len(Y))])
		if do and self.spinQ.value() != 0:

			if toAdd: self.totalPeaks["Peaks"].append(Peak(self.spinOffsetX.value(), self.spinOffsetY.value(), self.spinOffsetZ.value(), self.spinHeight.value(), self.spinQ.value(), arange(self.totalPeaks['SideSize']), arange(self.totalPeaks['SideSize'])))
			else: Z += Peak(self.spinOffsetX.value(), self.spinOffsetY.value(), self.spinOffsetZ.value(), self.spinHeight.value(), self.spinQ.value(), arange(self.totalPeaks['SideSize']), arange(self.totalPeaks['SideSize'])).points

		for peak in self.totalPeaks['Peaks']:
			Z += peak.points

		self.figure.clear()
		ax = self.figure.gca(projection='3d')
		ax.plot_surface(X, Y, Z, cmap = cm.coolwarm)
		ax.set_xlabel('X')
		ax.set_ylabel('Y')
		ax.set_zlabel('Z')
		ax.patch.set_facecolor('#F0F0F0')
		self.canvas.draw()

	def openFile(self):
		filename = QFileDialog.getOpenFileName(self,"Load Archives","","JSON Files (*.json)")[0]
		if filename:
			with open(filename, 'r') as file: self.totalPeaks = loads(file.read())
			self.initGrid(opened=True)

	def saveFile(self):
		filename = QFileDialog.getSaveFileName(self, 'Save Schematic', '', 'JSON File (*.json);;Litematic File (*.litematic)')[0]
		if filename:
			if '.litematic' in filename:
				gridList = []
				X, Y = meshgrid(arange(self.totalPeaks['SideSize']), arange(self.totalPeaks['SideSize']))
				Z = array([[0.0 for x in range(len(X))] for y in range(len(Y))])
				for peak in self.totalPeaks['Peaks']:
					Z += peak.points

				mini, maxi = minima(Z), maxima(Z)

				for i in range(len(X)):
					for j in range(len(Y)):
						x, z, y = X[i][j], Y[i][j], Z[i][j]
						if (x, z, y) not in gridList: gridList.append([int(x), int(z), int(y)])
		
				schem = Schematic(len(X), (int(maxi-mini)+1), len(X), name="ReliefGen", author="Anosema", description="Made with LandFormGenerator", main_region_name="Main")
				reg = schem.regions["Main"]

				try: with open('config.json', 'r') as file: data = load(file)
				except: self.showError('config.json not found, see help on GitHub (Ctrl+H)', 'Error')
				Soils = [BlockState(x['id']) for x in data['soil']]
				SoilsWeights = tuple([x['weight'] for x in data['soil']])

				Stones = [BlockState(x['id']) for x in data['underground']]
				StonesWeights = tuple([x['weight'] for x in data['underground']])

				Layers = [BlockState(x['id']) for x in data['layer']]



				t0 = time()
				for i in gridList:
					x, z, y = i[0], i[1], i[2]
					if data['isLayered']: block = Layers[int(y*((len(Layers)-1)/int(maxi-mini)))]
					else: block = choices(Soils, weights=SoilsWeights, k=1)[0]
					reg.setblock(x, y, z, block)
					for j in range(y):
						if data['isLayered']: block = Layers[int(j*((len(Layers)-1)/int(maxi-mini)))]
						else: block = choices(Stones, weights=StonesWeights, k=1)[0]
						reg.setblock(x, j, z, block)
				schem.save(filename)
				t1 = time()
				process_time = t1-t0

				self.showError(f'Your Litematic is Finished (Done in {str(int(process_time*10)/10)}s', 'Finished')
			else:
				data = {}
				data = {"SideSize": self.totalPeaks["SideSize"]}
				data['Peaks'] = []
				for i in self.totalPeaks['Peaks']:
					data['Peaks'].append(i.dict)
				with open(filename, 'w') as file: dump(data, file, indent=4)

	def updateRange(self):
		self.spinOffsetX.setRange(0, self.totalPeaks['SideSize'])
		self.spinOffsetY.setRange(0, self.totalPeaks['SideSize'])
		self.spinOffsetX.setValue(int(self.totalPeaks['SideSize']/2))
		self.spinOffsetY.setValue(int(self.totalPeaks['SideSize']/2))
		self.labelMaxOffsetX.setText(str(self.totalPeaks['SideSize']))
		self.labelMaxOffsetY.setText(str(self.totalPeaks['SideSize']))

	def toggleLive(self):
		if self.actionLiveRender.isChecked():
			self.spinOffsetX.valueChanged.connect(lambda: self.showGrid(False))
			self.spinOffsetY.valueChanged.connect(lambda: self.showGrid(False))
			self.spinOffsetZ.valueChanged.connect(lambda: self.showGrid(False))
			self.spinHeight .valueChanged.connect(lambda: self.showGrid(False))
			self.spinQ      .valueChanged.connect(lambda: self.showGrid(False))
		else:
			self.spinOffsetX.valueChanged.disconnect()
			self.spinOffsetY.valueChanged.disconnect()
			self.spinOffsetZ.valueChanged.disconnect()
			self.spinHeight .valueChanged.disconnect()
			self.spinQ      .valueChanged.disconnect()

	def undo(self):
		if self.totalPeaks['Peaks'] != []:
			self.oldReliefs.append(self.totalPeaks['Peaks'].pop())
			self.showGrid()

	def redo(self):
		if self.oldReliefs != []:
			self.totalPeaks['Peaks'].append(self.oldReliefs.pop())
			self.showGrid()

	def openConfig(self):
		command, slash = ['xdg-open', 'start'], ['/', '\\']
		try: system(f'{command[self.system]} "{getcwd()}{slash[self.system]}config.json"')
		except: self.showError('config.json not found, see help on GitHub (Ctrl+H)', 'Error')

	def openHelp(self):
		command = ['xdg-open', 'start']
		system(f'{command[self.system]} "https://github.com/Anosema/Landforms"')

	def showError(self, message, title):
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText(message)
		msg.setWindowTitle(title)
		msg.show()
		msg.exec_()




app = QApplication(argv)
app.setStyle("Fusion")

Window = MainWindow()

Window.show()

app.exec_()