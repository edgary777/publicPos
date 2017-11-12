import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Buttons

class MainWindow(QWidget):
    """Main window widget."""

    def __init__(self):
        """Init."""
        super().__init__()

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        style = """
            QLabel {
                color: black;
                font-weight: bold;
                font-size: 17pt;
            };
        """
        self.btn = Buttons.MenuBtn(150, 90, 10, Qt.red, "Choriqueso", style)
        layout = QVBoxLayout()
        layout.addWidget(self.btn)
        self.setLayout(layout)


app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
sys.exit(app.exec_())
