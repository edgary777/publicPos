import sys
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

    def simplifiedTicket(self):
        """Simplified visualization is created here."""
        layout = QVBoxLayout()

        header = self.simplifiedHeader()
        content = self.simplifiedContent()
        footer = self.simplifiedFooter()

        if header:
            layout.addLayout(header)
        else:
            layout.addSpacing(100)
        layout.addLayout(content)
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
                if isinstance(val, float):
                    val = "$" + str(val)
                setattr(self, key, QLabel(str(val)))
                if x == 0:
                    getattr(self, key).setAlignment(Qt.AlignLeft)
                else:
                    getattr(self, key).setAlignment(Qt.AlignCenter)
                content.addWidget(getattr(self, key), y, x)
                x += 1
            y += 1

        if self.factura:
            z = 1
            if self.dcto:
                total = self.total
                dcto = round(self.subtotal * self.dcto, 2)
                content.addWidget(QLabel("DCTO"), y + z, 2)
                content.addWidget(QLabel("$" + str(dcto)), y + z, 3)
                z += 1
            else:
                total = self.total
            content.addWidget(QLabel("SUBTOTAL"), y + z, 2)
            content.addWidget(QLabel("$" + str(self.subtotal)), y + z, 3)
            z += 1
            content.addWidget(QLabel("IVA"), y + z, 2)
            content.addWidget(QLabel("$" + str(self.iva)), y + z, 3)
            z += 1
            content.addWidget(QLabel("TOTAL"), y + z, 2)
            content.addWidget(QLabel("$" + str(total)), y + z, 3)
        else:
            z = 1
            if self.dcto:
                total = self.total
                dcto = round(self.subtotal * self.dcto, 2)
                content.addWidget(QLabel("DCTO"), y + z, 2)
                content.addWidget(QLabel("$" + str(dcto)), y + z, 3)
                z += 1
            else:
                total = self.total
            content.addWidget(QLabel("TOTAL"), y + z, 2)
            content.addWidget(QLabel("$" + str(total)), y + z, 3)

        return content

    def ticketFooter(self):
        """Ticket footer is created here."""
        return None

    def simplifiedHeader(self):
        """Simplified header is created here."""
        header = QVBoxLayout()

        style = """
        QLabel {
            color: black;
            font-weight: bold;
            font-size: 20pt;
            font-family: Asap;
        };"""

        if self.nombre:
            nombre = QLabel(str(self.nombre))
            nombre.setWordWrap(True)
            nombre.setAlignment(Qt.AlignCenter)
            nombre.setStyleSheet(style)
            header.addWidget(nombre)

        if self.nombre and self.notes:
            line = QLabel("______________")
            line.setAlignment(Qt.AlignCenter)
            line.setStyleSheet(style)
            header.addWidget(line)

        if self.notes:
            notas = QLabel(str(self.notes))
            notas.setWordWrap(True)
            notas.setAlignment(Qt.AlignCenter)
            notas.setStyleSheet(style)
            header.addWidget(notas)

        if self.nombre or self.notes:
            return header
        else:
            return None

    def simplifiedContent(self):
        """Simplified ticket content is created here."""
        content = QGridLayout()

        titles = {"Quant": "Cant.", "Name": "Descripción"}

        styleProducts = """
        QLabel {
            color: black;
            font-weight: bold;
            font-size: 18pt;
            font-family: Asap;
        };"""

        styleTotal = """
        QLabel {
            color: black;
            font-weight: bold;
            font-size: 18pt;
            font-family: Asap;
            text-decoration: underline;
        };"""

        styleHour = """
        QLabel {
            color: black;
            font-weight: bold;
            font-size: 18pt;
            font-family: Asap;
        };"""

        y = 1
        for product in self.products:
            x = 0
            for key, value in titles.items():
                val = getattr(product, "get" + key)()
                setattr(self, key, QLabel(str(val)))
                getattr(self, key).setStyleSheet(styleProducts)
                if x == 0:
                    getattr(self, key).setAlignment(Qt.AlignCenter)
                else:
                    getattr(self, key).setAlignment(Qt.AlignLeft)
                content.addWidget(getattr(self, key), y, x)
                x += 1
            y += 1

        if self.factura:
            total = QLabel("$" + str(self.total))
            total.setAlignment(Qt.AlignCenter)
            total.setStyleSheet(styleTotal)
            content.addWidget(total, y + 1, 1)
        else:
            total = QLabel("$" + str(self.total))
            total.setAlignment(Qt.AlignCenter)
            total.setStyleSheet(styleTotal)
            content.addWidget(total, y + 1, 1)

        hour = QLabel(str(self.hour))

        hour.setStyleSheet(styleHour)
        hour.setAlignment(Qt.AlignCenter)

        content.addWidget(hour, y + 1, 0)

        return content

    def simplifiedFooter(self):
        """Simplified footer is created here."""
        footer = QVBoxLayout()

        style = """
        QLabel {
            color: black;
            font-weight: bold;
            font-size: 35pt;
            font-family: Asap;
        };"""

        folio = QLabel(str(self.folio))
        folio.setAlignment(Qt.AlignCenter)
        folio.setStyleSheet(style)

        footer.addWidget(folio)

        return footer

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

        self.date = data["fecha"]
        self.hour = data["hora"]

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
