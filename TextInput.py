from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize


class TextInput(QWidget):
    """Input field.

    Meant to write customer specifications.
    """

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.field = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.field)

        self.setLayout(layout)
        self.setStyleSheet("""border: 2px solid;
                              border-radius: 20px;
                              background-color: palette(base);
                              font-weight: Bold;
                              font-size: 15pt;
                              font-family: Asap;""")

    def returnText(self):
        """Return the text in the field."""
        return self.field.toPlainText()

    def minimumSizeHint(self):
        """Minimum size hint."""
        return QSize(20, 20)


class TextInputSmall(QWidget):
    """Input field.

    Meant to write customer specifications.
    """

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.field = QTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.field)

        self.setLayout(layout)
        self.setStyleSheet("""border: 2px solid;
                              border-radius: 10px;
                              background-color: palette(base);
                              font-weight: Bold;
                              font-size: 15pt;
                              font-family: Asap;""")

    def returnText(self):
        """Return the text in the field."""
        return self.field.toPlainText()

    def minimumSizeHint(self):
        """Minimum size hint."""
        return QSize(20, 20)
