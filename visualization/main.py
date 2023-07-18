from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPainter, QColor, QPen
import pyqtgraph as pg
import sys
import random

MAX_DATA = 100
class Page(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.data = [10, 20, 30]
        self.plot = pg.plot()
        self.plot.getPlotItem().hideAxis('bottom')
        self.plot.getPlotItem().hideAxis('left')

        self.dataPlot = pg.BarGraphItem(x = range(len(self.data)),height = self.data, width = 0.5)
        title = QLabel("Sorting Visualizer")
        self.dataLabel = QLabel(' '.join(str(c) for c in self.data))
        layout = QVBoxLayout()
        self.setGeometry(500, 500, width, height)
        self.setWindowTitle("Sorting Visualization")
        self.setLayout(layout)
        layout.addWidget(title)
        layout.addWidget(self.dataLabel)
        self.plot.addItem(self.dataPlot)
        layout.addWidget(self.plot)
        randomBtn = QPushButton("Randomize")
        randomBtn.clicked.connect(self.randomizeData)
        layout.addWidget(randomBtn)
        addBtn = QPushButton("Add Data")
        addBtn.clicked.connect(self.addData)
        layout.addWidget(addBtn)

    def randomizeData(self):
        random.shuffle(self.data)
        self.dataLabel.setText(' '.join(str(c) for c in self.data))

    def plotData(self):
        pass
    def addData(self):
        x = random.randint(0,100)
        self.data.append(x)
        self.dataLabel.setText(' '.join(str(c) for c in self.data))

    def resetData(self):
        self.data = [4,2,5]
    def sorting(self, name=None):
        pass
        # Implement your sorting algorithm here
        # Update self.data with the changes
        # Call self.update() after each step to trigger repaint


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Page(600, 600)
    window.show()
    sys.exit(app.exec())
