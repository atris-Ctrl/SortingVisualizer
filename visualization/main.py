import sys
import random
import pyqtgraph as pg
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox

MAX_DATA = 100


class SortingVisualizer(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)

        self.timer = QTimer()
        self.timer.setInterval(100)  # Delay between iterations in milliseconds

        self.setGeometry(500, 200, width, height)
        self.data = random.sample(range(0, 100), 100)
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

    def randomizeData(self):
        random.shuffle(self.data)
        colors = [(128,0,123)]*len(self.data)
        colors[0] = (100,22,200)
        self.dataPlot.setOpts(brushes=colors,height=self.data)

    def sorting(self):
        algorithm = self.sortingComboBox.currentText()

        if algorithm == "Bubble Sort":
            self.timer.timeout.connect(self.bubbleSort)
            self.timer.start(2000)
            #self.bubbleSort()
        elif algorithm == "Insertion Sort":
            self.insertionSort()
        elif algorithm == "Selection Sort":
            self.selectionSort()

    def bubbleSort(self):
        print("1111")
        n = len(self.data)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    self.dataPlot.setOpts(height=self.data)
                    self.updateLabel()
        self.timer.stop()

    def insertionSort(self):
        # Implementation of insertion sort
        pass

    def selectionSort(self):
        # Implementation of selection sort
        pass

    def updateLabel(self):
        self.iterationCount += 1
        self.iterLabel.setText("Iteration Count: " + str(self.iterationCount))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SortingVisualizer(600, 600)
    window.show()
    sys.exit(app.exec())
