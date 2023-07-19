import sys
import random
import pyqtgraph as pg
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox

MAX_DATA = 100
i = 0
j = 0
minInd = 0


class SortingVisualizer(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sorting Visualizer")
        self.timer = QTimer()

        self.setGeometry(500, 200, width, height)
        self.data = random.sample(range(1, 101), 5)
        self.iterationCount = 0

        font = QFont("Arial", 16, QFont.Weight.Bold)  # Specify the font family, size, and weight
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Sorting Visualizer")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(font)
        layout.addWidget(title)

        self.plotWidget = pg.plot()
        self.plotWidget.setBackground('w')
        self.plotWidget.getPlotItem().hideAxis('bottom')
        self.plotWidget.getPlotItem().hideAxis('left')
        self.plotWidget.setXRange(0, 100)
        self.dataPlot = pg.BarGraphItem(x=range(len(self.data)), height=self.data, width=0.5)
        self.plotWidget.addItem(self.dataPlot)
        layout.addWidget(self.plotWidget)

        randomBtn = QPushButton("Randomize")
        randomBtn.clicked.connect(self.randomizeData)
        layout.addWidget(randomBtn)

        self.iterLabel = QLabel("Iteration Count: " + str(self.iterationCount))
        layout.addWidget(self.iterLabel)

        sortingLayout = QHBoxLayout()
        layout.addLayout(sortingLayout)

        sortingLabel = QLabel("Sort Algorithm:")
        sortingLayout.addWidget(sortingLabel)

        self.sortingComboBox = QComboBox()
        self.sortingComboBox.addItems(["Bubble Sort", "Insertion Sort", "Selection Sort"])
        sortingLayout.addWidget(self.sortingComboBox)

        sortBtn = QPushButton("Sort")
        sortBtn.clicked.connect(self.sorting)
        layout.addWidget(sortBtn)

        self.algorithm = None
        nextBtn = QPushButton("Next")
        nextBtn.clicked.connect(self.stepWiseSort)
        layout.addWidget(nextBtn)

    def randomizeData(self):
        random.shuffle(self.data)
        self.dataPlot.setOpts(height=self.data)

    def sorting(self):
        self.algorithm = self.sortingComboBox.currentText()
        self.resetLabel()
        if self.algorithm == "Bubble Sort":
            self.timer.timeout.connect(self.bubbleSort)
            self.timer.start(40)

        elif self.algorithm == "Insertion Sort":
            self.timer.timeout.connect(self.insertionSort)
            self.timer.start(40)

        elif self.algorithm == "Selection Sort":
            global j
            j = 1
            self.timer.timeout.connect(self.selectionSort)
            self.timer.start(40)

    def bubbleSort(self):
        n = len(self.data)
        global i, j

        if i < n:
            if j < n - i - 1:
                colors = [(128, 128, 128)] * len(self.data)
                colors[j] = (100, 22, 200)
                colors[j + 1] = (100, 22, 0)
                self.dataPlot.setOpts(brushes=colors, height=self.data)
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                self.updateLabel()
                j += 1
            else:
                i += 1
                j = 0
        else:
            i = 0
            j = 0
            colors = [(128, 128, 128)] * len(self.data)
            self.dataPlot.setOpts(brushes=colors, height=self.data)
            self.timer.stop()

    def selectionSort(self):
        global i, j, minInd
        n = len(self.data)
        if i < n:
            print("i : " + str(i))

            if j < n:
                print("j : " + str(j))
                self.highlightBars(j, minInd)
                if self.data[j] < self.data[minInd]:
                    minInd = j
                j += 1
                self.updateLabel()

            else:
                print("min index : " + str(minInd))
                self.data[i], self.data[minInd] = self.data[minInd], self.data[i]
                self.dataPlot.setOpts(height=self.data)

                i += 1
                j = i + 1
                minInd = i


        else:
            i = 0
            j = 0
            minInd = 0
            colors = [(128, 128, 128)] * len(self.data)
            self.dataPlot.setOpts(brushes=colors, height=self.data)
            self.timer.stop()

    def stepWiseSort(self):
        self.algorithm = self.sortingComboBox.currentText()

        if self.algorithm == "Bubble Sort":
            self.bubbleSort()
        elif self.algorithm == "Insertion Sort":
            self.insertionSort()
        elif self.algorithm == "Selection Sort":
            self.selectionSort()

    def insertionSort(self):
        # Implementation of insertion sort
        pass

    def updateLabel(self):
        self.iterationCount += 1
        self.iterLabel.setText("Iteration Count: " + str(self.iterationCount))

    def resetLabel(self):
        self.iterationCount = 0
        self.iterLabel.setText("Iteration Count: " + str(self.iterationCount))

    def highlightBars(self, ind, ind1):
        colors = [(128, 128, 128)] * len(self.data)
        colors[ind] = (100, 22, 200)
        colors[ind1] = (100, 22, 0)
        self.dataPlot.setOpts(brushes=colors, height=self.data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SortingVisualizer(600, 600)
    window.show()
    sys.exit(app.exec())
