from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class OrderTotal(QWidget):
    """Object to show the total of the order in a session."""

    def __init__(self, total, parent, dcto=None):
        """Init."""
        super().__init__(parent)

        self.parent = parent
        self.total = total

        self.color = QColor(Qt.black)
        self.rounded = 20

        self.initUi()

    def initUi(self):
        """Init."""
        self.totalLabel = QLabel(str(self.total))

        layout = QHBoxLayout()

        layout.addWidget(self.totalLabel)

        self.setLayout(layout)

    def updateTotal(self, total):
        """Update the total shown."""
        self.total = total
        self.updateUi()

    def updateDcto(self, dcto):
        """Update the discount."""
        self.dcto = dcto

    def showTax(self):
        """Update view to show tax."""
        pass

    def hideTax(self):
        """Update view to hide tax."""
        pass

    def updateUi(self):
        """Update the Ui."""
        self.totalLabel.setText(str(self.total))
        # self.update()

    def paintEvent(self, event):
        """Paint Event."""
        # Set up the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create the path for the big figure
        path = QPainterPath()
        path.addRoundedRect(QRectF(0.0, 0.0, self.width(), self.height()),
                            self.rounded, self.rounded)

        # Calculate the percentage ratio to get a 3 px margin
        ratioX = (1 - ((3 / self.width()) * 2))
        ratioY = (1 - ((3 / self.height()) * 2))

        # calculate the distance the shape has to be moved to be centered
        x = (self.width() - (self.width() * ratioX)) / 2
        y = (self.height() - (self.height() * ratioY)) / 2

        # Create the path for the small figure
        path2 = QPainterPath()
        path2.addRoundedRect(QRectF(x, y, self.width() * ratioX,
                             self.height() * ratioY), self.rounded * ratioY,
                             self.rounded * ratioY)

        # Fill the paths with color
        painter.fillPath(path, self.color)
        painter.fillPath(path2, Qt.white)
