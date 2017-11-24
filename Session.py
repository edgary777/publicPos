from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Menu
import TextInput
import Holder


class MultiSession(QWidget):
    """Object meant to hold sessions.

    This object handles the sessions creation, destruction and switching.
    """

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.initUi()

    def initUi(self):
        """Ui is created here."""
        pass

    def createSession(self, session):
        """Create a new session."""
        pass

    def deleteSession(self, session):
        """Delete a session."""
        pass

    def switchSession(self, session):
        """Switch session."""
        pass


class Session(QWidget):
    """Object meant to hold orders.

    To enable multi-sessions, each order must be a Session object, all sessions
    objects need to be in either a QStackedLayout or QStackedWidget to be able
    to switch between them.
    """

    def __init__(self, parent, ID=None):
        """Init."""
        super().__init__(parent)

        self.ID = ID

        self.initUi()

    def initUi(self):
        """Ui is created here."""
        holder = Holder.Holder(parent=self)

        lonches = """Jamón,Carnes Frias,Choriqueso,Campirana,Pechuga,Bistec,
                     Cubana,Pierna,Pibil,Adobada,Arrachera,Torréon,
                     Vegetariana"""

        bebidas = """Coca,Coca Light,Sprite,Fanta,Fanta Fresa,Fresca,Manzanita,
                     Agua,Naranjada,Limonada,ValleFrut,N Durazno,
                     N Guayaba,N Manzana,N Mango,J Manzana"""

        menuLonches = Menu.Menu(lonches, parent=self, hold=holder)
        menuBebidas = Menu.Menu(bebidas, parent=self, hold=holder)

        itemsLayout = QStackedLayout()
        itemsLayout.addWidget(menuLonches)
        itemsLayout.addWidget(menuBebidas)

        tabs = {"Lonches": (0, itemsLayout), "Bebidas": (1, itemsLayout)}
        tabsWidget = Menu.Tabs(tabs, parent=self)
        tabsLayout = QHBoxLayout()
        tabsLayout.addWidget(tabsWidget)

        inputField = TextInput.TextInput(parent=self)

        layoutC1 = QVBoxLayout()
        layoutC1.addWidget(holder)

        layoutC2 = QVBoxLayout()
        layoutC2.addLayout(tabsLayout)
        layoutC2.addLayout(itemsLayout)
        layoutC2.addWidget(inputField)

        layout = QHBoxLayout()
        layout.addLayout(layoutC1)
        layout.addLayout(layoutC2)

        self.setLayout(layout)
