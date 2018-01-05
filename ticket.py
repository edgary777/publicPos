import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


class Ticket(QWidget):
    """Ticket widget."""

    def __init__(self, data=None, parent=None, simplified=None):
        """Init."""
        super().__init__(parent)

        self.parseData(data)

        self.setFixedWidth(250)

        if simplified:
            self.simplifiedTicket()
        else:
            self.ticket()

    def ticket(self):
        """Ticket visualization is created here."""
        layout = QVBoxLayout()

        header = self.ticketHeader()
        content = self.ticketContent()
        footer = self.ticketFooter()

        layout.addLayout(header)
        layout.addLayout(content)

        if footer:
            layout.addLayout(footer)

        self.setLayout(layout)

    def ticketHeader(self):
        """Ticket header is created here."""
        header = QVBoxLayout()
        if self.image:
            label = QLabel()
            image = QPixmap(self.image)

            label.setPixmap(image.scaledToWidth(self.width() - 20, Qt.FastTransformation))
            label.setMargin(0)
            label.setAlignment(Qt.AlignCenter)

            header.setSpacing(0)
            header.addWidget(label)
        else:
            label = QLabel(self.title)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(self.width() - 20)
            label.setMargin(0)

            header.setSpacing(0)
            header.addWidget(label)

        header.addWidget(self.address)
        header.addWidget(self.regimenFiscal)
        header.addWidget(self.RFC)
        header.addWidget(self.name)
        header.addWidget(self.tel)
        header.addStretch()

        return header

    def ticketContent(self):
        """Ticket content is created here."""
        content = QGridLayout()

        titles = {"cant": "Cant.", "desc": "Descripción", "price": "P. Unit.",
                  "total": "Total"}

        x = 0
        for key, value in titles.items():
            setattr(self, key, QLabel(value))
            item = getattr(self, key)
            item.setAlignment(Qt.AlignCenter)
            content.addWidget(item, 0, x)
            x += 1

        return content

    def ticketFooter(self):
        """Ticket footer is created here."""
        return None

    def simplifiedTicket(self):
        """Order visualization is created here."""
        pass

    def parseData(self, data):
        """Parse and organize the data for the ticket."""
        self.image = """Resources/s-close.png"""
        self.title = """SUPER LONCHES DE TORREON"""

        self.address = QLabel("""CUAUHTEMOC 217A SUR, ZONA CENTRO, CP 34000, DURANGO, DURANGO, MEXICO""")
        self.address.setWordWrap(True)
        self.address.setAlignment(Qt.AlignCenter)

        self.regimenFiscal = QLabel("""REGIMEN DE INCORPORACIÓN FISCAL""")
        self.regimenFiscal.setWordWrap(True)
        self.regimenFiscal.setAlignment(Qt.AlignCenter)

        self.RFC = QLabel("""VICM640515DD3""")
        self.RFC.setWordWrap(True)
        self.RFC.setAlignment(Qt.AlignCenter)

        self.name = QLabel("""MARICELA VIZCARRA CAMPOS""")
        self.name.setWordWrap(True)
        self.name.setAlignment(Qt.AlignCenter)

        self.tel = QLabel("""(618) 829-62-18""")
        self.tel.setWordWrap(True)
        self.tel.setAlignment(Qt.AlignCenter)

        self.folio = None
        self.date = datetime.date.today()
        self.hour = datetime.datetime.now().time().strftime("%H:%M")

        self.products = None

        self.factura = None

        self.total = None
        self.subtotal = None
        self.dcto = None
        self.iva = None

        self.notes = None

        self.status = None  # PAG / LLEVA

        self.takeOut = None  # AQUÍ / LLEVAR

    def Print(self):
        """Print the widget."""
        printer = QPrinter(QPrinter.HighResolution)
        # pageSize = QPageSize(QSizeF(80, 80),
        # QPageSize.Millimeter, name="test2", matchPolicy=QPageSize.ExactMatch)
        # printer.setPageSize(pageSize)
        dialog = QPrintDialog(printer,self)
        if (dialog.exec_() != QDialog.Accepted):
            return
        painter = QPainter()
        painter.begin(printer)

        xscale = printer.pageRect().width() / self.width()
        yscale = printer.pageRect().height() / self.height()
        scale = min(xscale, yscale)

        painter.translate(printer.paperRect().x() + printer.pageRect().width() / 2,
                          self.height() * 1.39)  # dont know why but 1.39 works

        painter.scale(scale, scale)

        painter.translate(-1 * self.width() / 2, -1 * self.height() / 2)
        self.render(painter)
        painter.end()

    def paintEvent(self, event):
        """Set window background color."""
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)


app = QApplication(sys.argv)
window = Ticket()
window.show()
# window.Print()
sys.exit(app.exec_())
