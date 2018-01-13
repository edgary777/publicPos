from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from escpos.printer import Usb
from PIL import Image
import io
import Dialogs


class Print(object):
    """Print a Qdialog object."""

    def __init__(self):
        """Init."""
        pass

    def Print(self, dialog, simplified=None, other=None):
        """Print."""
        self.printLinux(dialog, simplified=simplified)
        # try:
        #     self.printLinux(dialog)
        # except:
        #     self.PrintWindows(dialog, simplified=None, other=None)
        # else:
        #     pass

    def PrintWindows(self, dialog, simplified=None, other=None):
        """Print the passed dialog."""
        printer = QPrinter(QPrinter.HighResolution)
        if simplified:
            printer.setDocName("COMANDA")
        elif other:
            printer.setDocName(str(other))
        else:
            printer.setDocName("TICKET")
        painter = QPainter()
        p = dialog.palette()
        p.setColor(dialog.backgroundRole(), Qt.white)
        dialog.setPalette(p)
        painter.begin(printer)

        xscale = printer.pageRect().width() / dialog.width()
        yscale = printer.pageRect().height() / dialog.height()
        scale = min(xscale, yscale)

        painter.translate(printer.paperRect().x() + printer.pageRect().width() / 2,
                          dialog.height() * 1.39)  # dont know why but 1.39 works

        painter.scale(scale, scale)

        painter.translate(-1 * dialog.width() / 2, -1 * dialog.height() / 2)
        dialog.render(painter)
        painter.end()

    def printLinux(self, dialog, simplified):
        """Print the passed dialog.

        Linux doesn't have raspberry pi drivers for the printer, so if running
        on a raspberry pi print with this method
        """
        painter = QPainter()

        p = dialog.palette()
        p.setColor(dialog.backgroundRole(), Qt.white)

        dialog.setPalette(p)

        width = dialog.getSize()[0]

        height = dialog.getSize()[1]

        if not simplified:
            height += 10

        pixmap = QImage(width, height, QImage.Format_Grayscale8)
        # pixmap.fill(Qt.transparent)

        painter.begin(pixmap)
        dialog.render(painter)
        painter.end()

        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        pixmap.save(buffer, "PNG")
        pixmap.save("Hi.png", "PNG")

        strio = io.BytesIO()
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        pil_im = Image.open(strio)

        buffer = None

        p = Usb(0x04b8, 0x0e03, 0)
        p.image(pil_lm, impl="graphics", center=True, fragment_height=2000)
        p.image(pil_lm, impl="bitImageColumn", center=True, fragment_height=2000)
        p.image(pil_im, impl="bitImageRaster", center=True, fragment_height=2000)
        p.cut()
