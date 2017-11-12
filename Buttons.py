from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MenuBtn(QAbstractButton):
    """
    Color is defined as Qt.'color'
    style is a stylesheet as 'QLabel { color : color;'
    """
    def __init__(self, width, height, rounded, color, label, style ,
                 product=None, parent=None):
        """Init.
        product is meant to be the product ID and it is to be emmited
        as a signal when the button is clicked so the ticket knows
        which item it is.
        """
        super().__init__(parent)

        self.width = width
        self.height = height
        self.rounded = rounded
        self.color = QColor(color)
        self.label = label
        self.text = style

        label = QLabel(self.label)
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        self.setFixedSize(self.width, self.height)

    def paintEvent(self, event):
        color = self.color.lighter(130) if self.underMouse() else self.color
        if self.isDown():
            color = self.color.darker(150)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(0.0, 0.0, self.width, self.height),
                            self.rounded, self.rounded)
        painter.fillPath(path, color)
