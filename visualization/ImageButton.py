from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QPushButton


class ImageButton(QPushButton):
    def __init__(self, image_path, parent=None):
        super(ImageButton, self).__init__(parent)
        # Load the image and set it as the background
        image = QPixmap(image_path)
        self.setIcon(QIcon(image))
        self.setIconSize(QSize(image.width()+50, image.height()+50))
        self.setFixedSize(image.width(), image.height())
        self.setFlat(True)  # Remove button border to make it look like an image

