from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Ticket(QWidget):
    """Ticket widget."""

    def __init__(self, data, parent, simplified=None):
        """Init."""
        super().__init__(parent)

        self.parseData(data)

        if simplified:
            self.simplifiedTicket()
        else:
            self.ticket()

    def ticket(self):
        """Ticket visualization is created here."""
        pass

    def simplifiedTicket(self):
        """Order visualization is created here."""
        pass

    def parseData(self, data):
        """Parse and organize the data for the ticket."""
        self.image = None
        self.title = None

        self.address = None
        self.regimenFiscal = None
        self.RFC = None
        self.name = None
        self.tel = None

        self.folio = None
        self.date = None
        self.hour = None

        self.products = None

        self.factura = None

        self.total = None
        self.subtotal = None
        self.dcto = None
        self.iva = None

        self.notes = None

        self.status = None  # PAG / LLEVA

        self.takeOut = None  # AQUÍ / LLEVAR
