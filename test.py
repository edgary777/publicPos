from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtWidgets import *
from escpos.printer import Usb
from PIL import Image
import io
import Dialogs
import sys


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

        pixmap = QImage(dialog.width(), dialog.height(), QImage.Format_Grayscale8)
        # pixmap.fill(Qt.transparent)

        painter.begin(pixmap)
        dialog.render(painter)
        painter.end()

        # pixmap.save("hi.png", "PNG")

        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        pixmap.save(buffer, "PNG")

        strio = io.BytesIO()
        # strio.write(buffer.data)
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        pil_im = Image.open(strio)

        print(pil_im)

        # self.printer(pil_im)

    def printer(self, pixmap):
        """I."""
        """ Seiko Epson Corp. Receipt Printer (EPSON TM-T20) """

        p = Usb(0x04b8, 0x0e03, 0)
        p.image(pixmap)
        # p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
        p.cut()
        # pr = escpos.escpos.Escpos()
        # pr = escpos.printer.Usb()
        # pr.image(pixmap)
        # # pr = escpos.printer().usb(0x04b8, 0x0e03, 0)
        # pr.cut()

app = QApplication(sys.argv)

dialog = Dialogs.QuestionDialog("hola")

printer = Print()
printer.dialogToImage(dialog)

sys.exit(app.exec_())
