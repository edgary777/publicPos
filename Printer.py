from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from escpos.printer import Usb
from PIL import Image
import io


class Print(object):
    """Print a Qdialog object."""

    def __init__(self):
        """Init."""
        pass

    def dialogToImage(self, dialog, simplified=None):
        """Print the passed dialog."""
        painter = QPainter()
        p = dialog.palette()
        p.setColor(dialog.backgroundRole(), Qt.white)
        dialog.setPalette(p)
        pixmap = QImage()
        painter.begin(pixmap)


        rect = QRect(0, dialog.width(), 0, dialog.height())

        dialog.render(pixmap)

        painter.end()

        img = pixmap
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        img.save(buffer, "PNG")

        strio = io.BytesIO()
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        pil_im = Image.open(strio)

        self.printer(pil_im)

    def printer(self, pixmap):
        """I."""
        """ Seiko Epson Corp. Receipt Printer (EPSON TM-T20) """

        p = Usb(0x04b8, 0x0e03, 0)
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        # p.text("Hello World\n")
        p.image(pixmap)
        # p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
        p.cut()
        # pr = escpos.escpos.Escpos()
        # pr = escpos.printer.Usb()
        # pr.image(pixmap)
        # # pr = escpos.printer().usb(0x04b8, 0x0e03, 0)
        # pr.cut()
