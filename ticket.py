import sys
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

        self.setFixedWidth(200)

        if simplified:
            self.simplifiedTicket()
        else:
            self.ticket()

    def ticket(self):
        """Ticket visualization is created here."""
        topData = QVBoxLayout()
        if self.image:
            label = QLabel()
            image = QPixmap(self.image)

            label.setPixmap(image.scaledToWidth(180, Qt.FastTransformation))
            label.setMargin(0)
            label.setAlignment(Qt.AlignCenter)

            topData.setSpacing(0)
            topData.addWidget(label)
        else:
            label = QLabel(self.title)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(180)
            label.setMargin(0)

            topData.setSpacing(0)
            topData.addWidget(label)

        topData.addWidget(QLabel(self.address))
        self.setLayout(topData)

    def simplifiedTicket(self):
        """Order visualization is created here."""
        pass

    def parseData(self, data):
        """Parse and organize the data for the ticket."""
        self.image = """Resources/s-print.png"""
        self.title = """SUPER LONCHES DE TORREON"""

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

        # Apparently this sets the page size, so the second size in translate
        # is the one that changes the page length. to change it dinamically I
        # have to get the size of the widget and set it to it.

        painter.translate(printer.paperRect().x() + printer.pageRect().width()/2,
                          300)

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
# window.showMaximized()
window.Print()
sys.exit(app.exec_())
