from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Buttons


class Menu(QWidget):
    """Food Menu widget."""

    def __init__(self, items, parent, hold=None):
        """Init."""
        super().__init__(parent)

        self.hold = hold
        self.items = items
        self.initUi()

    def initUi(self):
        """Ui Setup."""
        # List setup
        items = self.items
        items = [item.strip() for item in items.split(',')]

        # Buttons configuration
        width = 150
        height = 60
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
                                                color, item, style,
                                                parent=self, holder=self.hold))
            if y == 4:
                x += 1
                y = 0
            layout.addWidget(getattr(self, item), x, y)
            y += 1
        self.setLayout(layout)


class Tabs(QWidget):
    """Food Menu widget."""

    def __init__(self, items, parent=None):
        """Init."""
        super().__init__(parent)

        self.items = items
        self.initUi()

    def initUi(self):
        """Ui Setup."""
        # List setup
        # items = self.items
        # items = [item.strip() for item in items.split(',')]

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
        for key, value in self.items.items():
            setattr(self, key, Buttons.StrokeBtn(width, height, roundness,
                    color, key, style, index=value[0], obj=value[1],
                    parent=self))
            layout.addWidget(getattr(self, key))
        self.setLayout(layout)
