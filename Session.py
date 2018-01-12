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
import datetime
import Printer
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
            session.printBoth()

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

        self.llevaBtn = Buttons.StrokeBtn2(100, 60, 15, qRgb(33,46,226),
                                           "L?", llevaStyle, self, sWidth=10)
        self.llevaBtn.clicked.connect(self.toggleLleva)

        self.npBtn = Buttons.StrokeBtn2(100, 60, 15, qRgb(33,46,226),
                                           "P?", llevaStyle, self, sWidth=10)
        self.npBtn.clicked.connect(self.toggleNp)

        sexAgeLayout = QHBoxLayout()

        sexAgeLayout.addStretch()
        sexM = QRadioButton("M")
        sexH = QRadioButton("H")
        self.sexo = QButtonGroup(self)
        self.sexBtns = [sexM, sexH]
        z = 0
        for btn in self.sexBtns:
            btn.setStyleSheet(tinyStyle)
            self.sexo.addButton(btn, x)
            sexAgeLayout.addWidget(btn)
            z += 1

        sexAgeLayout.addSpacing(20)

        age1 = QRadioButton("1")
        age2 = QRadioButton("2")
        age3 = QRadioButton("3")
        age4 = QRadioButton("4")
        self.edad = QButtonGroup(self)
        self.ageBtns = [age1, age2, age3, age4]
        z = 1
        for btn in self.ageBtns:
            btn.setStyleSheet(tinyStyle)
            self.edad.addButton(btn, x)
            sexAgeLayout.addWidget(btn)
            z += 1
        sexAgeLayout.addStretch()

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
        self.nameField = TextInput.TextInputSmall(parent=self)
        self.nameField.setFixedHeight(55)

        nameLayout = QVBoxLayout()
        nameLayout.setSpacing(0)
        nameLayout.addWidget(self.nameField)
        nameLayout.addLayout(sexAgeLayout)

        orderTopLayout = QHBoxLayout()
        orderTopLayout.addLayout(nameLayout)
        orderTopLayout.addWidget(self.orderTotal)

        layoutC11 = QHBoxLayout()
        layoutC11.addWidget(self.npBtn)
        layoutC11.addWidget(self.llevaBtn)
        layoutC11.addWidget(self.payBtn)

        layoutC1 = QVBoxLayout()
        layoutC1.addLayout(orderTopLayout)
        layoutC1.addWidget(self.holder)
        layoutC1.addLayout(layoutC11)

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

        self.picBtnseparate.clicked.connect(self.separateItems)

        self.picBtnprint.clicked.connect(self.printBoth)

        self.picBtndcto.clicked.connect(self.setDcto)

        self.picBtniva.clicked.connect(lambda: self.orderTotal.toggleTax())

        self.picBtnclose.clicked.connect(lambda:
                                         self.holder.getOrder().clean())

        return layout

    def pay(self):
        """Print, record, and delete order."""
        if self.llevar is not None:
            dialog = Dialogs.PayDialog(self, self.orderTotal.getTotal())

            if dialog.exec_():
                pass

    def toggleLleva(self):
        """Print, record, and delete order."""
        if self.llevar is False or self.llevar is True:
            self.llevar = not self.llevar
        else:
            self.llevar = False

        if self.llevar is False:
            self.llevaBtn.setText("AQUI")
        else:
            self.llevaBtn.setText("LLEVAR")

    def toggleNp(self):
        """Print, record, and delete order."""
        if self.np is False or self.np is True:
            self.np = not self.np
        else:
            self.np = False

        if self.np is False:
            self.npBtn.setText("NP")
        else:
            self.npBtn.setText("PAG")

    def getSex(self):
        """Return customer sex.

        0 is Mujer -- 1 is Hombre
        """
        sexo = self.sexo.checkedId()
        return 0 if sexo < 0 else sexo

    def getAge(self):
        """Return customer age."""
        edad = self.edad.checkedId()
        return 0 if edad < 0 else edad

    def setTime(self):
        """Fix order time to current."""
        if not self.date:
            self.date = datetime.date.today()
        if not self.hour:
            self.hour = datetime.datetime.now().time().strftime("%H:%M")

    def printBoth(self, forceBoth=False):
        """Print simple and complete tickes."""
        # If the session has no set date the order hasn't been printed
        # before, so we print both, otherwise we just print the ticket.
        if self.orderTotal.getTotal() == 0:
            self.parent.deleteSession(self, self.parent.sessionIndex(self))
        if not self.date or forceBoth is True:
            self.printSimplified()
        self.printTicket()

    def printTicket(self):
        """Simplified ticket printer."""
        if self.orderTotal.getTotal() > 0:
            self.setTime()
            ticket = Ticket.Ticket(self.collector(), self)
            # if ticket.exec_():
            #     pass
            printer = Printer.Print()
            printer.dialogToImage(ticket)
            printer = None
            ticket.setParent(None)
            db = Db()
            db.recordTicket(self.collector())
            self.parent.deleteSession(self, self.parent.sessionIndex(self))

    def printSimplified(self):
        """Simplified ticket printer."""
        if self.orderTotal.getTotal() > 0:
            self.setTime()
            ticket = Ticket.Ticket(self.collector(), self, simplified=True)
            # if ticket.exec_():
            #     pass
            printer = Printer.Print()
            printer.dialogToImage(ticket, simplified=True)
            printer = None
            ticket.setParent(None)

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

    def collector(self):
        """Collect and return all data to be recorded on the database."""
        items = {"factura": self.orderTotal.getInvoice(),
                 "descuento": self.orderTotal.getDcto()[0],
                 "descuentoa": self.orderTotal.getDcto()[1],
                 "descuentop": self.orderTotal.getDcto()[2],
                 "Np": self.np,
                 "Llevar": self.llevar}

        for key, value in items.items():
            if not value or value is False:
                setattr(self, key, 0)
            else:
                if value is True:
                    value = 1
                setattr(self, key, value)

        data = {
            "folio": self.getID(),
            "nombre": self.nameField.getText(),
            "llevar": self.Llevar,  # Capitalized because different
            "pagado": self.Np,  # Capitalized because different
            "sexo": self.getSex(),
            "edad": self.getAge(),
            "notas": self.inputField.getText(),
            "factura": self.factura,
            "total": self.orderTotal.getTotal(),
            "subtotal": self.orderTotal.getSubtotal(),
            "iva": self.orderTotal.getVat(),
            "descuento": self.descuento,
            "descuentoa": self.descuentoa,
            "descuentop": self.descuentop,
            "cupon": self.orderTotal.getDcto()[3],
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
