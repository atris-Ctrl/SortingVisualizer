import sys
import random

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QPixmap, QIcon, QFontDatabase
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox
import ctypes
from ImageButton import ImageButton
import sounddevice as sd

MAX_DATA = 100
i = 0
j = 0
minInd = 0
current_value = -1
def generate_sound(frequency, duration):
    pass
class SortingVisualizer(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)

        customFont = QFont("Arial")

        self.setWindowTitle("Sorting Visualizer")
        self.setWindowIcon(QIcon('styles/logosorting.png'))
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.setGeometry(500, 200, width, height)
        self.data = random.sample(range(1, MAX_DATA+1), MAX_DATA)
        self.n = len(self.data)
        self.iterationCount = 0

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Sorting Visualizer")
        pixmap = QPixmap("styles/sortingvisualTitle.png")

        title.setPixmap(pixmap)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Plot Widget
        self.plotWidget = pg.plot()
        self.plotWidget.getPlotItem().hideAxis('bottom')
        self.plotWidget.getPlotItem().hideAxis('left')
        self.plotWidget.setBackground("#34495E")
        self.dataPlot = pg.BarGraphItem(x=range(self.n), height=self.data, width=0.5)
        self.plotWidget.addItem(self.dataPlot)
        layout.addWidget(self.plotWidget)
        self.resetChart()

        control_layout = QHBoxLayout()

        reduceBtn = ImageButton("styles/plusButton.png")
        reduceBtn.clicked.connect(self.reduceData)
        control_layout.addWidget(reduceBtn)

        addBtn = ImageButton("styles/plusplus.png")
        addBtn.clicked.connect(self.addData)
        control_layout.addWidget(addBtn)

        randomBtn = QPushButton("Randomize")
        randomBtn.clicked.connect(self.randomizeData)
        control_layout.addWidget(randomBtn)

        layout.addLayout(control_layout)

        self.iterLabel = QLabel("Iteration Count: " + str(self.iterationCount))
        layout.addWidget(self.iterLabel)

        sortingLayout = QHBoxLayout()
        layout.addLayout(sortingLayout)

        sortingLabel = QLabel("Sort Algorithm:")
        sortingLabel.setFont(customFont)
        sortingLayout.addWidget(sortingLabel)

        self.sortingComboBox = QComboBox()
        self.sortingComboBox.addItems(["Bubble Sort", "Insertion Sort", "Selection Sort"])
        sortingLayout.addWidget(self.sortingComboBox)

        sortBtn = QPushButton("Sort")
        sortBtn.clicked.connect(self.sorting)
        layout.addWidget(sortBtn)

        self.algorithm = None
        self.historyStack = []

        historyLayout = QHBoxLayout()
        layout.addLayout(historyLayout)

        backBtn = QPushButton("Back")
        backBtn.clicked.connect(self.previousSort)
        historyLayout.addWidget(backBtn)

        nextBtn = QPushButton("Next")
        nextBtn.clicked.connect(self.stepWiseSort)
        historyLayout.addWidget(nextBtn)
    def resetChart(self):
        colors = ["#f5f6fa"] * self.n
        self.dataPlot.setOpts(brushes=colors, height=self.data,pens= colors)
    def updateChart(self):
        self.plotWidget.clear()
        colors = ["#f5f6fa"] * self.n
        self.dataPlot = pg.BarGraphItem(x=range(self.n), height=self.data, width=0.5, pens = colors, brushes = colors)
        self.plotWidget.addItem(self.dataPlot)

    def reduceData(self):
        if self.n >= 10:
            self.data.pop()
            self.n -= 1
            self.updateChart()

    def addData(self):
        x = random.randint(1, MAX_DATA + 1)
        if self.n < 100:
            self.data.append(x)
            self.n += 1
            self.updateChart()

    def randomizeData(self):
        random.shuffle(self.data)
        self.resetChart()

    def sorting(self):
        self.timer.stop()
        self.algorithm = self.sortingComboBox.currentText()
        self.historyStack = []
        self.resetLabel()
        global i, j, minInd, current_value
        i = 0
        j = 0
        if self.algorithm == "Bubble Sort":
            self.timer.timeout.connect(self.bubbleSort)
        elif self.algorithm == "Insertion Sort":
            i = 1
            current_value = self.data[i]
            self.timer.timeout.connect(self.insertionSort)
        elif self.algorithm == "Selection Sort":
            minInd = 0
            self.timer.timeout.connect(self.selectionSort)
        self.timer.start(10)

    def bubbleSort(self):
        global i, j
        if i < self.n:
            if j < self.n - i - 1:
                self.highlightBars(j, j + 1)
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                j += 1
                self.updateLabel()
                self.historyStack.append(self.data)
            else:
                i += 1
                j = 0
        else:
            self.resetChart()
            self.timer.stop()
            try:
                self.timer.timeout.disconnect()
            except TypeError:
                pass

    def selectionSort(self):
        global i, j, minInd
        if i < self.n:
            if j < self.n:
                self.highlightBars(j, minInd)
                if self.data[j] < self.data[minInd]:
                    minInd = j
                j += 1
                self.updateLabel()

            else:
                self.data[i], self.data[minInd] = self.data[minInd], self.data[i]
                self.resetChart()
                i += 1
                minInd = i
                j = i + 1



        else:
            minInd = 0
            self.resetChart()
            self.timer.stop()
            try:
                self.timer.timeout.disconnect()
            except TypeError:
                pass
    def insertionSort(self):
        global i, j, current_value
        if i < self.n:
            if j >= 0 and self.data[j] > current_value:
                self.data[j + 1] = self.data[j]
                j -= 1
                self.updateLabel()
            else:
                self.data[j + 1] = current_value
                self.highlightBars(j + 1, i)
                i += 1
                if i < self.n:
                    current_value = self.data[i]
                    j = i - 1
            self.resetChart()

        else:
            self.resetChart()
            self.timer.stop()
            try:
                self.timer.timeout.disconnect()
            except TypeError:
                pass
    def stepWiseSort(self):
        self.algorithm = self.sortingComboBox.currentText()
        if self.algorithm == "Bubble Sort":
            self.bubbleSort()
        elif self.algorithm == "Insertion Sort":
            self.insertionSort()
        elif self.algorithm == "Selection Sort":
            self.selectionSort()

    def previousSort(self):
        if len(self.historyStack) > 0:
            previousData = self.historyStack.pop()
            self.data = previousData
            self.n = len(previousData)
            self.updateChart()

    def updateLabel(self):
        self.iterationCount += 1
        self.iterLabel.setText("Iteration Count: " + str(self.iterationCount))

    def resetLabel(self):
        self.iterationCount = 0
        self.iterLabel.setText("Iteration Count: 0")

    def highlightBars(self, ind, ind1):
        colors = ["#f5f6fa"] * len(self.data)
        colors[ind] = (102, 255, 0)
        colors[ind1] = (255, 165, 0)
        self.dataPlot.setOpts(brushes=colors, height=self.data, pens=colors)


if __name__ == '__main__':
    myappid = 'arbitarystringtoshowtaskicon'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    stylesheet = open("styles/styles.css").read()
    app.setStyleSheet(stylesheet)
    window = SortingVisualizer(600, 700)
    window.show()
    sys.exit(app.exec())
