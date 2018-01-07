import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


class Ticket(QDialog):
    """Ticket widget."""

    def __init__(self, data, parent, simplified=None):
        """Init."""
        super().__init__(parent)

        self.simplified = simplified

        self.parseData(data)

        self.setFixedWidth(250)

        if self.simplified:
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

        dateID = QGridLayout()

        styleBig = """
            QLabel {
                color: black;
                font-weight: bold;
                font-size: 25pt;
                font-family: Asap;
            };"""
        styleSmall = """
            QLabel {
                color: black;
                font-weight: bold;
                font-size: 15pt;
                font-family: Asap;
            };"""

        folioLabel = QLabel("FOLIO")
        folioLabel.setAlignment(Qt.AlignCenter)
        folioLabel.setStyleSheet(styleBig)
        dateID.addWidget(folioLabel, 0, 0)

        folio = QLabel(str(self.folio))
        folio.setAlignment(Qt.AlignCenter)
        folio.setStyleSheet(styleBig)
        dateID.addWidget(folio, 0, 1)

        date = QLabel(str(self.date))
        date.setAlignment(Qt.AlignCenter)
        date.setStyleSheet(styleSmall)
        dateID.addWidget(date, 1, 0)

        hour = QLabel(str(self.hour))
        hour.setAlignment(Qt.AlignCenter)
        hour.setStyleSheet(styleSmall)
        dateID.addWidget(hour, 1, 1)

        header.addLayout(dateID)

        return header

    def ticketContent(self):
        """Ticket content is created here."""
        content = QGridLayout()

        titles = {"Name": "Descripción", "Price": "P. Unit.", "Quant": "Cant.",
                  "Total": "Total"}

        x = 0
        for key, value in titles.items():
            setattr(self, key, QLabel(value))
            item = getattr(self, key)
            item.setAlignment(Qt.AlignCenter)
            content.addWidget(item, 0, x)
            x += 1

        y = 1
        for product in self.products:
            x = 0
            for key, value in titles.items():
                val = getattr(product, "get" + key)()
                setattr(self, key, QLabel(str(val)))
                if x == 0:
                    getattr(self, key).setAlignment(Qt.AlignLeft)
                else:
                    getattr(self, key).setAlignment(Qt.AlignCenter)
                content.addWidget(getattr(self, key), y, x)
                x += 1
            y += 1

        print(self.total)

        if self.factura:
            content.addWidget(QLabel("SUBTOTAL"), y + 1, 2)
            content.addWidget(QLabel(str(self.subtotal)), y + 1, 3)
            content.addWidget(QLabel("IVA"), y + 2, 2)
            content.addWidget(QLabel(str(self.iva)), y + 2, 3)
            content.addWidget(QLabel("TOTAL"), y + 3, 2)
            content.addWidget(QLabel(str(round(self.total * 1.16, 2))), y + 3, 3)
        else:
            content.addWidget(QLabel("TOTAL"), y + 1, 2)
            content.addWidget(QLabel(str(self.total)), y + 1, 3)

        return content

    def ticketFooter(self):
        """Ticket footer is created here."""
        return None

    def simplifiedTicket(self):
        """Simplified visualization is created here."""
        pass

    def parseData(self, data):
        """Parse and organize the data for the ticket."""
        self.image = """Resources/logo.png"""
        self.title = """SUPER LONCHES DE TORREON"""

        self.address = QLabel("""CUAUHTEMOC 217A SUR, ZONA CENTRO, CP 34000, DURANGO, DURANGO""")
        self.address.setWordWrap(True)
        self.address.setAlignment(Qt.AlignCenter)

        self.regimenFiscal = QLabel("""REGIMEN DE INCORPORACIÓN FISCAL""")
        self.regimenFiscal.setWordWrap(True)
        self.regimenFiscal.setAlignment(Qt.AlignCenter)

        self.RFC = QLabel("""VICM6405157F1""")
        self.RFC.setWordWrap(True)
        self.RFC.setAlignment(Qt.AlignCenter)

        self.name = QLabel("""MARICELA VIZCARRA CAMPOS""")
        self.name.setWordWrap(True)
        self.name.setAlignment(Qt.AlignCenter)

        self.tel = QLabel("""(618) 829-62-18""")
        self.tel.setWordWrap(True)
        self.tel.setAlignment(Qt.AlignCenter)

        self.date = datetime.date.today()
        self.hour = datetime.datetime.now().time().strftime("%H:%M")

        self.folio = data["folio"]
        self.nombre = data["nombre"]
        self.takeOut = data["llevar"]  # AQUÍ[FALSE] / LLEVAR[TRUE]
        self.status = data["pagado"]  # PAG[TRUE] / LLEVA[FALSE]
        self.notes = data["notas"]
        self.factura = data["factura"]
        self.total = data["total"]
        self.subtotal = data["subtotal"]
        self.iva = data["iva"]
        self.dcto = data["descuento"]
        self.cancelado = data["cancelado"]
        self.products = data["productos"]

    def paintEvent(self, event):
        """Set window background color."""
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)


# app = QApplication(sys.argv)
# window = Ticket()
# window.show()
# window.Print()
# sys.exit(app.exec_())
