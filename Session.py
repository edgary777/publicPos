from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Menu
import TextInput
import Holder
import Buttons
import OrderTotal
import Dialogs
import Ticket
import Printer
import datetime
from Db import Db


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

    def cancelOrder(self, session, index):
        """Cancel passed session."""
        question = "SEGURO QUE QUIERES CANCELAR ESTA ORDEN?"
        dialog = Dialogs.QuestionDialog(self, question)
        if dialog.exec_():
            session.cancelado = 1
            session.printTicket(cancel=True)

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

    def sessionIndex(self, session):
        """Return session index."""
        return self.sessions.index(session)

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
        self.ticket = None

        self.date = None
        self.hour = None

        self.paga = 0
        self.cambio = 0

        self.llevar = None
        self.np = None

        self.sexo = 0
        self.edad = 0

        self.cancelado = 0

        self.ID = None
        self.setID()

        self.initUi()

    def initUi(self):
        """Ui is created here.

        DO NOT USE 'x' AS A VARIABLE HERE AGAIN, IT WILL BREAK THE CODE
        """
        self.holder = Holder.Holder(parent=self)

        self.orderTotal = OrderTotal.OrderTotal(0, self)

        dBa = Db()

        categories = dBa.getCategories()
        itemsLayout = QStackedLayout()
        tabs = {}
        x = 0  # this is he only x that can be used in init

        payStyle = """
            QLabel {
                color: black;
                font-weight: bold;
                font-size: 25pt;
                font-family: Asap;
            };
            """

        llevaStyle = """
            QLabel {
                color: Black;
                font-weight: bold;
                font-size: 15pt;
                font-family: Asap;
            };
            """

        tinyStyle = """
            QRadioButton {
                color: Black;
                font-weight: bold;
                font-family: Asap;
                font-size: 15pt;
            };
            """

        self.payBtn = Buttons.StrokeBtn2(100, 60, 15, qRgb(226,224,33),
                                         "PAGAR", payStyle, self, sWidth=10,
                                         hExpand=True)
        self.payBtn.clicked.connect(self.pay)

        for category in categories:
            products = dBa.getProducts(category[0])
            setattr(self, "menu" + category[0], Menu.Menu(products,
                    category[1], self, hold=self.holder))
            itemsLayout.addWidget(getattr(self, "menu" + category[0]))
            tabs[category[0]] = (x, itemsLayout)
            x += 1
        tabsWidget = Menu.Tabs(tabs, parent=self)
        tabsLayout = QHBoxLayout()
        tabsLayout.addWidget(tabsWidget)

        self.inputField = TextInput.TextInput(parent=self)

        orderTopLayout = QHBoxLayout()
        orderTopLayout.addWidget(self.orderTotal)

        layoutC1 = QVBoxLayout()
        layoutC1.addLayout(orderTopLayout)
        layoutC1.addWidget(self.holder)
        layoutC1.addWidget(self.payBtn)

        layoutH1C1 = QHBoxLayout()
        layoutH1C1.addLayout(self.imgBtns())
        layoutH1C1.addLayout(layoutC1)

        layoutC2 = QVBoxLayout()
        layoutC2.addLayout(tabsLayout)
        layoutC2.addLayout(itemsLayout)
        layoutC2.addWidget(self.inputField)

        layout = QHBoxLayout()
        layout.addLayout(layoutH1C1)
        layout.addLayout(layoutC2)

        self.setLayout(layout)

    def imgBtns(self):
        """Image buttons generator and layout creator."""
        names = ["separate", "dcto", "iva", "close", "gear"]
        layout = QVBoxLayout()
        for name in names:
            setattr(self, "picBtn" + name,
                    Buttons.PicButton("Resources/s-" + name,
                                      "Resources/h-" + name,
                                      "Resources/c-" + name, self))
            layout.addWidget(getattr(self, "picBtn" + name))
        layout.addWidget(self.picBtngear)

        self.picBtnseparate.clicked.connect(self.separateItems)

        self.picBtndcto.clicked.connect(self.setDcto)

        self.picBtniva.clicked.connect(lambda: self.orderTotal.toggleTax())

        self.picBtnclose.clicked.connect(lambda:
                                         self.holder.getOrder().clean())

        return layout

    def pay(self):
        """Print, record, and delete order."""
        dialog = Dialogs.PayDialog(self, self.orderTotal.getTotal())

        if dialog.exec_():
            pass

    def setTime(self):
        """Fix order time to current."""
        if not self.date:
            self.date = datetime.date.today()
        if not self.hour:
            self.hour = datetime.datetime.now().time().strftime("%H:%M")

    def printTicket(self, cancel=False):
        """Simplified ticket printer."""
        if self.orderTotal.getTotal() > 0:
            self.setTime()
            ticket = Ticket.Ticket(self.collector(), self, cancel)
            # if ticket.exec_():
            #     pass
            printer = Printer.Print()
            printer.Print(ticket)
            printer = None
            ticket.setParent(None)
            db = Db()
            db.recordTicket(self.collector())
            self.parent.deleteSession(self, self.parent.sessionIndex(self))

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
                                       percentage=dcto[1], amount=dcto[2])
            if dialog.exec_():
                pass

    def setID(self):
        """Set an id for the session."""
        sessions = self.parent.sessions
        db = Db()
        if not sessions:
            self.ID = db.getFolio() + 1
        else:
            self.ID = sessions[len(sessions) - 1].getID() + 1

    def getID(self):
        """Return an id for the session."""
        return self.ID

    def getParent(self):
        """Return the order parent."""
        return self.parent

    def getTotal(self):
        """Return the order total."""
        return self.orderTotal.getTotal()

    def collector(self):
        """Collect and return all data to be recorded on the database."""
        items = {"factura": self.orderTotal.getInvoice(),
                 "descuento": self.orderTotal.getDcto()[0],
                 "descuentoa": self.orderTotal.getDcto()[1],
                 "descuentop": self.orderTotal.getDcto()[2]
                 }

        for key, value in items.items():
            if not value or value is False:
                setattr(self, key, 0)
            else:
                if value is True:
                    value = 1
                setattr(self, key, value)

        data = {
            "folio": self.getID(),
            "factura": self.factura,
            "total": self.orderTotal.getTotal(),
            "subtotal": self.orderTotal.getSubtotal(),
            "iva": self.orderTotal.getVat(),
            "descuento": self.descuento,
            "descuentoa": self.descuentoa,
            "descuentop": self.descuentop,
            "paga": self.paga,
            "cambio": self.cambio,
            "cancelado": self.cancelado,
            "productos": self.holder.getOrder().getItems(),
            "fecha": self.date,
            "hora": self.hour,
            "rfc": "SOVE920621",
            "telefono": "8717823328",
            "email": "edgar21dejunio@gmail.com",
            "nombre2": "EDGAR SOLIS VIZCARRA"
        }
        return data
