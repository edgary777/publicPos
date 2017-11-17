from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Holder(QWidget):
    """This holds and shows and manipulates all orders."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.initUI()
        self.addOrder(Order(parent=self))

    def initUI(self):
        """Ui is created here."""
        # This is set as a QScrollArea so oversized orders can be seen
        layout = QVBoxLayout()
        self.area = QScrollArea()

        # This must be done so it can update dynamically
        self.area.setWidgetResizable(True)

        layout.addWidget(self.area)
        self.setLayout(layout)

    def addOrder(self, order):
        """Add an order."""
        self.order = order
        self.area.setWidget(order)

    def getOrder(self):
        """Return the order."""
        return self.order

    def printOrder(self):
        """Print an order."""
        pass

    def recordOrder(self):
        """Add order to data base."""
        pass


class Order(QWidget):
    """This holds and shows all the selected items for the order."""

    def __init__(self, parent, discount=None):
        """Init."""
        super().__init__(parent)

        self.items = []

        self.initUi()

    def initUi(self):
        """Ui is created here."""
        self.orderLayout = QGridLayout()
        self.orderLayout.setColumnStretch(0, 1)
        self.orderLayout.setColumnStretch(1, 6)

        self.titles = self.createTitles()
        print(self.titles)
        self.orderLayout.addLayout(self.titles, 0, 1)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.orderLayout)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def createTitles(self):
        """Add titles to layout."""
        titles = ["ARTICULO", "CANTIDAD", "PRECIO", "TOTAL"]
        layout = QHBoxLayout()
        for title in titles:
            setattr(self, title, QLabel(title))
            getattr(self, title).setAlignment(Qt.AlignCenter)
            layout.addWidget(getattr(self, title))
        return layout

    def addItem(self, item):
        """Add an item."""
        itemIn = Item(item, parent=self)
        search = self.searchItem(item[0])
        if search:
            self.editItem(search, search.getQuant() + 1)
        else:
            self.items.append(itemIn)
            self.update()

    def searchItem(self, item):
        """Pass a name as a string and returns the item with that name."""
        result = None
        for x in self.items:
            if x.getName() == item:
                result = x
        if result:
            return result
        else:
            return None

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

    def removeEverything(self):
        """Remove all items from the layout."""
        for i in reversed(range(self.orderLayout.count())):
            if i > 0:
                it = self.orderLayout.itemAt(i)
                try:
                    self.orderLayout.takeAt(i).widget().setParent(None)
                except AttributeError:
                    for i in reversed(range(it.count())):
                        it.takeAt(i).widget().setParent(None)
                    self.orderLayout.removeItem(it)

    def addEverything(self):
        """Add all items to the layout."""
        if self.items:
            for item in self.items:
                index = self.items.index(item)
                itui = ItemUI(item, index, parent=self)
                x = index + 1
                self.orderLayout.addWidget(itui.getBtn(), x, 0)
                self.orderLayout.addLayout(itui.getItem(), x, 1)

    def update(self):
        """Update the UI to show changes."""
        # First remove all items.
        self.removeEverything()

        # Then if any left add them back.
        self.addEverything()


class ItemUI(QWidget):
    """This is the UI representation of each product chosen."""

    def __init__(self, item, index, parent):
        """Init."""
        super().__init__(parent)
        """Item UI and Data representations are separated because I don't.
        want to keep tracking and updating the index of each item in the order.
        I'd rather delete all UI representations every time there is a change
        and create them again from the updated list of items.
        """
        self.item = item
        self.index = index
        self.parent = parent

    def getItem(self):
        """Return Item Ui."""
        attr = ["Name", "Quant", "Price", "Total"]
        layout = QHBoxLayout()
        for x in attr:
            setattr(self, x, QLabel(str(getattr(self.item, "get" + x)())))
            getattr(self, x).setAlignment(Qt.AlignCenter)
            layout.addWidget(getattr(self, x))
        return layout

    def getBtn(self):
        """Return the button to delete the item."""
        close = QPushButton("X")
        close.clicked.connect(lambda: self.parent.removeItem(self.item))
        return close



class Item(QWidget):
    """This is the data representation of each product chosen."""

    def __init__(self, data, parent):
        """Init."""
        super().__init__(parent)

        self.name = data[0]
        self.quant = data[1]
        self.price = data[2]
        self.total = self.quant * self.price

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
