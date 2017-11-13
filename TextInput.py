from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TextInput(QWidget):
    def __init__(self):
        super().__init__()

        field = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(field)

        self.setLayout(layout)
        self.setStyleSheet("""border: 2px solid; border-radius:20px;
                              background-color: palette(base);
                              font-weight: Bold; font-size: 15pt;
                              font-family: Asap;""")

    def minimumSizeHint(self):
        return QSize(150, 150)
