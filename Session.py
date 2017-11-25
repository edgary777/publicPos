from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Menu
import TextInput
import Holder
import Buttons
import random
import math

class MultiSession(QWidget):
    """Object meant to hold sessions.

    This object handles the sessions creation, destruction and switching.
    """

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.sessions = []

        self.sessionsLayout = QStackedLayout()
        self.btnLayout = QHBoxLayout()

        self.activeSession = 0

        self.createSession()

        self.initUi()

    def initUi(self):
        """Ui is created here."""
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.sessionsLayout)
        self.layout.addLayout(self.btnLayout)

        self.setLayout(self.layout)

    def createSession(self):
        """Create a new session."""
        session = Session(self)
        self.sessions.append(session)
        self.UpdateUi()
        self.activeSession = self.sessions.index(session)
        self.switchSession(self.activeSession)

    def deleteSession(self, session):
        """Delete a session."""
        index = self.sessions.index(session)
        self.sessions.remove(session)
        self.UpdateUi()

    def switchSession(self, index):
        """Switch session."""
        self.activeSession = index
        self.UpdateUi()
        self.sessionsLayout.setCurrentIndex(index)

    def addEverything(self):
        """Add all Sessions to the layout."""
        # Buttons configuration
        width = 90
        height = 90
        roundness = 10
        color1 = qRgb(101,60,240)
        color2 = qRgb(18,157,226)
        style = """
            QLabel {
                color: black;
                font-weight: bold;
                font-size: 25pt;
                font-family: Asap;
            };
            """

        for session in self.sessions:
            indxN = self.sessions.index(session)
            sessionN = session.getID()

            btn = Buttons.SessionBtn(width, height, roundness, color1, color2,
                                     sessionN, style, parent=self, obj=self,
                                     index=indxN)

            self.sessionsLayout.addWidget(session)
            self.btnLayout.addWidget(btn)
        NewSessionBtn = Buttons.NewSessionBtn(width, height, roundness, color1,
                                              style, parent=self, obj=self)

        if len(self.sessions) < 13:
            self.btnLayout.addWidget(NewSessionBtn)

    def removeEverything(self):
        """Remove all Sessions from the layout."""
        for i in reversed(range(self.sessionsLayout.count())):
            self.sessionsLayout.takeAt(i).widget().setParent(None)

        for i in reversed(range(self.btnLayout.count())):
            self.btnLayout.takeAt(i).widget().setParent(None)

    def UpdateUi(self):
        """Update the Ui."""
        self.removeEverything()

        self.addEverything()

        if not self.sessions:
            self.createSession()


class Session(QWidget):
    """Object meant to hold all objects pertaining to an order.

    To enable multi-sessions, each order must be a Session object, all sessions
    objects need to be in either a QStackedLayout or QStackedWidget to be able
    to switch between them.
    """

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.ID = None
        self.setID()

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

    def setID(self):
        """Set an id for the session."""
        self.ID = math.floor((random.random()) * 1000)

    def getID(self):
        """Return an id for the session."""
        return self.ID
