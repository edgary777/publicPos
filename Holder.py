from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Holder(QWidget):
    """This holds and shows and manipulates all orders."""

    def __init__(self, ID, discount, parent=None):
        """Init."""
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        """Ui is created here."""
        pass

    def addOrder(self, item):
        """Add an order."""
        pass

    def removeOrder(self, item):
        """Remove an order."""
        pass

    def printOrder(self):
        """Print an order."""
        pass

    def recordOrder(self):
        """Add order to data base."""
        pass


class Order(QWidget):
    """This holds and shows all the selected items for the order."""

    def __init__(self, ID, discount, parent=None):
        """Init."""
        super().__init__(parent)

        self.ID = ID
        self.items = []

        self.initUi()

    def initUI(self):
        """Ui is created here."""
        pass

    def addItem(self, item):
        """Add an item."""
        pass

    def removeItem(self, item):
        """Remove an item."""
        pass

    def extractItem(self, item, order):
        """Extract an item.

        Moves the item to another order deleting it from this one.
        """
        pass


class Item(QWidget):
    """This is the individual visual representation of each product chosen."""

    def __init(self, name, quant, price, parent=None):
        super().__init__(parent)

        self.name = name
        self.quant = quant
        self.price = price
        self.total = quant * price

    def editQuant(self, new):
        """Edits the quantity of products and updates the total."""
        self.quant = new
        self.total = self.quant * self.price
