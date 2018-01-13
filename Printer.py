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

    def printLinux(self, dialog, simplified=None):
        """Print the passed dialog.

        Linux doesn't have raspberry pi drivers for the printer, so if running
        on a raspberry pi print with this method
        """
        painter = QPainter()

        p = dialog.palette()
        p.setColor(dialog.backgroundRole(), Qt.white)

        dialog.setPalette(p)

        pixmap = QPixmap(dialog.width(), dialog.height())
        pixmap = QImage(pixmap.toImage())

        painter.begin(pixmap)
        dialog.render(pixmap)
        painter.end()

        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        pixmap.save(buffer, "PNG")

        strio = io.BytesIO()
        strio.write(buffer.data)
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        pil_im = Image.open(strio)

        p = Usb(0x04b8, 0x0e03, 0)
        p.image(pil_im)
        p.cut()
