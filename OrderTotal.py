from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class orderTotal(QWidget):
    """Object to show the total of the order in a session."""

    def __init__(self, total, dcto, parent):
        """Init."""
        super().__init__(parent)

        self.total = total
        self.dcto = dcto

        self.initUi()

    def initUi(self):
        """Init."""
        pass

    def updateTotal(self, total):
        """Update the total shown."""
        pass

    def updateDcto(self, dcto):
        """Update the discount."""
        pass

    def showTax(self):
        """Update view to show tax."""
        pass

    def hideTax(self):
        """Update view to hide tax."""
        pass
