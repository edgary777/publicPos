from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Ticket(QWidget):
    """Ticket widget."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.parseData()

        self.initUi()

    def initUi(self):
        """Visualization is created here."""
        pass

    def parseData(self):
        """Parse and arrange the data for the ticket."""
        pass
