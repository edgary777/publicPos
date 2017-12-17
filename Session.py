from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Menu
import TextInput
import Holder
import Buttons
import OrderTotal
import random
import math
import Dialogs


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

        # We always start with the session 0 from the array
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
        return session

    def deleteSession(self, session, index):
        """Delete a session."""
        if session.getID() == self.activeSession:
            if index > 0:
                # If the activeSession is not 0 then the previous one in the
                # index is the one that is selected.
                self.activeSession = self.sessions[index - 1].getID()
            else:
                # I used try in here because I couldn't think of any other
                # way to not crash the program when the activeSession is 0
                # and there are no other sessions.
                try:
                    self.activeSession = self.sessions[index + 1].getID()
                except IndexError:
                    pass  # nothing to be done here, just avoiding a crash
        self.sessions.remove(session)
        self.UpdateUi()

        # If the active session is the same than the session being deleted,
        # then the activeSession is switched to the one that has the index
        # the one being deleted had, this is to make deleting sessions less
        # confusing
        for session in self.sessions:
            if self.activeSession == session.getID():
                self.switchSession(self.sessions.index(session))
                break

    def switchSession(self, index):
        """Switch session."""
        self.activeSession = self.sessions[index].getID()
        self.UpdateUi()
        self.sessionsLayout.setCurrentIndex(index)

    def addEverything(self):
        """Add all Sessions to the layout."""
        # Buttons configuration
        width = 90
        height = 90
        roundness = 10
        color1 = qRgb(101, 60, 240)
        color2 = qRgb(18, 157, 226)
        style = """
            QLabel {
                color: black;
                font-weight: bold;
                font-size: 25pt;
                font-family: Asap;
            };
            """

        # We loop through all session objects in the self.sessions list and
        # create some UI buttons for each of them
        for session in self.sessions:
            indexN = self.sessions.index(session)  # Get the session index
            sessionN = session.getID()  # Get the session ID (Folio)

            # The button object is created
            btn = Buttons.SessionBtn(width, height, roundness, color1, color2,
                                     sessionN, style, parent=self, obj=self,
                                     index=indexN)

            # the button object is added to the layout
            self.sessionsLayout.addWidget(session)
            self.btnLayout.addWidget(btn)

        # This is the button that creates new sessions.
        NewSessionBtn = Buttons.NewSessionBtn(width, height, roundness, color1,
                                              style, parent=self, obj=self)

        # The button that creates new sessions is only added when there are
        # less than 13 sessions on the screen because otherwise they overflow
        # the screen.
        if len(self.sessions) < 13:
            self.btnLayout.addWidget(NewSessionBtn)

    def removeEverything(self):
        """Remove all Sessions from the layout."""
        for i in reversed(range(self.sessionsLayout.count())):
            self.sessionsLayout.takeAt(i).widget().setParent(None)
            # self.sessionsLayout.takeAt(i).widget().deleteLater()

        for i in reversed(range(self.btnLayout.count())):
            # self.btnLayout.takeAt(i).widget().setParent(None)
            # The comment above this comment was the original way to delete the
            # buttons from the buttons layout, and while it worked fine in
            # windows it crashed on linux, so it was changed and it now works
            # on both.
            self.btnLayout.takeAt(i).widget().deleteLater()

    def UpdateUi(self):
        """Update the Ui."""
        self.removeEverything()

        self.addEverything()

        # if all sessions are deleted then a new one is created
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

        self.parent = parent

        self.ID = None
        self.setID()

        self.initUi()

    def initUi(self):
        """Ui is created here."""
        self.holder = Holder.Holder(parent=self)

        self.orderTotal = OrderTotal.OrderTotal(0, self)

        lonches = """Jamón,Carnes Frias,Choriqueso,Campirana,Pechuga,Bistec,
                     Cubana,Pierna,Pibil,Adobada,Arrachera,Torréon,
                     Vegetariana"""

        bebidas = """Coca,Coca Light,Sprite,Fanta,Fanta Fresa,Fresca,Manzanita,
                     Agua,Naranjada,Limonada,ValleFrut,N Durazno,
                     N Guayaba,N Manzana,N Mango,J Manzana"""

        menuLonches = Menu.Menu(lonches, parent=self, hold=self.holder)
        menuBebidas = Menu.Menu(bebidas, parent=self, hold=self.holder)

        itemsLayout = QStackedLayout()
        itemsLayout.addWidget(menuLonches)
        itemsLayout.addWidget(menuBebidas)

        tabs = {"Lonches": (0, itemsLayout), "Bebidas": (1, itemsLayout)}
        tabsWidget = Menu.Tabs(tabs, parent=self)
        tabsLayout = QHBoxLayout()
        tabsLayout.addWidget(tabsWidget)

        inputField = TextInput.TextInput(parent=self)
        nameField = TextInput.TextInputSmall(parent=self)
        nameField.setFixedHeight(55)

        orderTopLayout = QHBoxLayout()
        orderTopLayout.addWidget(nameField)
        orderTopLayout.addWidget(self.orderTotal)

        layoutC1 = QVBoxLayout()
        layoutC1.addLayout(orderTopLayout)
        layoutC1.addWidget(self.holder)

        layoutH1C1 = QHBoxLayout()
        layoutH1C1.addLayout(self.imgBtns())
        layoutH1C1.addLayout(layoutC1)

        layoutC2 = QVBoxLayout()
        layoutC2.addLayout(tabsLayout)
        layoutC2.addLayout(itemsLayout)
        layoutC2.addWidget(inputField)

        layout = QHBoxLayout()
        layout.addLayout(layoutH1C1)
        layout.addLayout(layoutC2)

        self.setLayout(layout)

    def imgBtns(self):
        """Image buttons generator and layout creator."""
        names = ["separate", "print", "dcto", "iva", "close"]
        layout = QVBoxLayout()
        for name in names:
            setattr(self, "picBtn" + name,
                    Buttons.PicButton("resources/s-" + name,
                                      "resources/h-" + name,
                                      "resources/c-" + name, self))
            layout.addWidget(getattr(self, "picBtn" + name))
        layout.addStretch()
        self.picBtngear = Buttons.PicButton("resources/s-gear",
                                            "resources/h-gear",
                                            "resources/c-gear",
                                            self)
        layout.addWidget(self.picBtngear)

        # No idea how to do this action yet, it is meant to pop items from an
        # order and create a new order with them.
        self.picBtnseparate.clicked.connect(self.separateItems)

        # self.picBtnprint.clicked.connect()

        self.picBtndcto.clicked.connect(self.setDcto)

        self.picBtniva.clicked.connect(lambda: self.orderTotal.toggleTax())

        self.picBtnclose.clicked.connect(lambda:
                                         self.holder.getOrder().clean())

        return layout

    def separateItems(self):
        """Toggle and update discount."""
        if self.orderTotal.getTotal() > 0:
            dialog = Dialogs.PopOrderDialog(self)

            if dialog.exec_():
                pass

    def setDcto(self):
        """Toggle and update discount."""
        if self.orderTotal.getTotal() > 0:
            dcto = self.orderTotal.getDcto()
            dialog = Dialogs.DctDialog(self.orderTotal.getTotal(), parent=self,
                                       percentage=dcto[1], amount=dcto[2],
                                       code=dcto[3])
            if dialog.exec_():
                pass

    def setID(self):
        """Set an id for the session."""
        self.ID = math.floor((random.random()) * 1000)

    def getID(self):
        """Return an id for the session."""
        return self.ID

    def getParent(self):
        """Return the order parent."""
        return self.parent
