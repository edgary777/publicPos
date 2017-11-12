import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
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

        #List setup
        items = self.items
        items = [item.strip() for item in items.split(',')]

        #Buttons configuration
        width = 150
        height = 70
        roundness = 20
        color = Qt.red
        style = """
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 17pt;
                font-family: Asap;
            };
            """

        #Buttons creator
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
