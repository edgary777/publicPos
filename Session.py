from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Menu
import TextInput
import Holder


class Session(QWidget):
    """Object meant to hold orders.

    To enable multi-sessions, each order must be a Session object, all sessions
    objects need to be in either a QStackedLayout or QStackedWidget to be able
    to switch between them.
    """

    def __init__(self):
        """Init."""
        super().__init__()

        self.initUi()

    def initUi(self):
        """Ui is created here"""
        pass
