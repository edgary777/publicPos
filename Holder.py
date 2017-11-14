from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Holder(QWidget):
    """This holds and shows and manipulates all orders."""

    def __init__(self, parent=None):
        """Init."""
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        """Ui is created here."""
        # This is set as a QScrollArea so oversized orders can be seen
        layout = QVBoxLayout()
        self.area = QScrollArea()
        layout.addWidget(self.area)
        self.setLayout(layout)

    def addOrder(self, order):
        """Print an order."""
        self.area.setWidget(order)

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

        self.items = []

        self.initUi()

    def initUI(self):
        """Ui is created here."""
        self.Vlayout = QVBoxLayout()
        self.setLayout(layout)

    def addItem(self, item):
        """Add an item."""
        item = Item(item[0], item[1], item[2])
        self.items.append(item)
        self.update()

    def removeItem(self, item):
        """Remove an item."""
        try:
            self.items.remove(item)
            self.update()
        except ValueError:
            print("There was an error removing the item.")

    def clean(self):
        """Remove all items."""
        self.items = []
        self.update()

    def extractItem(self, item):
        """Extract an item.

        Remove the item from the list and return it to add it to other list.
        """
        item = self.items.pop(self.items.index(item))
        self.update()
        return item

    def editItem(self, item, edit):
        """Edit an item."""
        item.editQuant(edit)
        self.update()

    def update(self):
        """Update the UI to show changes."""
        # First remove all items.
        for i in reversed(range(self.layout.count())):
            self.layout.takeAt(i).widget().setParent(None)

        # Then if any left add them back.
        if self.items:
            for item in self.items:
                self.Vlayout.addWidget(item)
                pass


class ItemUI(QWidget):
    """This is the UI representation of each product chosen."""

    def __init(self, item, index, parent=None):
        """Init."""
        super().__init__(parent)
        """Item UI and Data representations are separated because I don't.
        want to keep tracking and updating the index of each item in the order.
        I'd rather delete all UI representations every time there is a change
        and create them again from the updated list of items.
        """
        self.item = item
        self.index = index

        self.hLayout = QHBoxLayout()
        self.setLayout(layout)

        self.initUi()

    def initUi(self):
        """Ui is created here."""
        close = QPushButton("X")
        close.clicked.connection(lambda: parent.removeItem(self))
        self.hLayout.addWidget(close)

        attr = ["Name", "Quant", "Price", "Total"]
        for x in attr:
            setattr(self, x, QLabel(getattr(self.item, "get" + x)()))
            getattr(self.x).setAlignment(Qt.AlignCenter)
            self.hLayout.addWidget(getattr(self, x))


class Item(QWidget):
    """This is the data representation of each product chosen."""

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

    def getName(self):
        """Return the name of the Item."""
        return self.name

    def getQuant(self):
        """Return the amount of items."""
        return self.quant

    def getPrice(self):
        """Return the price of the item."""
        return self.price

    def getTotal(self):
        """Return the total cost of the items."""
        return self.total
