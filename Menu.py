from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Buttons


class Menu(QWidget):
    """Food Menu widget."""

    def __init__(self, items):
        """Init."""
        super().__init__()

        self.items = items
        self.initUi()

    def initUi(self):
        """Ui Setup."""
        # List setup
        items = self.items
        items = [item.strip() for item in items.split(',')]

        # Buttons configuration
        width = 150
        height = 70
        roundness = 20
        color = qRgb(240, 216, 60)
        style = """
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 17pt;
                font-family: Asap;
            };
            """

        # Buttons creator
        layout = QGridLayout()
        x = 0
        y = 0
        for item in items:
            setattr(self, item, Buttons.MenuBtn(width, height, roundness,
                                                color, item, style))
            if y == 4:
                x += 1
                y = 0
            layout.addWidget(getattr(self, item), x, y)
            y += 1
        self.setLayout(layout)


class Tabs(QWidget):
    """Food Menu widget."""

    def __init__(self, items):
        """Init."""
        super().__init__()

        self.items = items
        self.initUi()

    def initUi(self):
        """Ui Setup."""
        # List setup
        items = self.items
        items = [item.strip() for item in items.split(',')]

        # Buttons configuration
        width = 150
        height = 70
        roundness = 20
        color = qRgb(154, 179, 174)
        style = """
            QLabel {
                color: black;
                font-weight: bold;
                font-size: 30pt;
                font-family: Asap;
            };
            """

        # Buttons creator
        layout = QHBoxLayout()
        for item in items:
            setattr(self, item, Buttons.StrokeBtn(width, height, roundness,
                                                color, item, style))
            layout.addWidget(getattr(self, item))
        self.setLayout(layout)
