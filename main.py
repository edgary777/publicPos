import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Menu


class MainWindow(QWidget):
    """Main window widget."""

    def __init__(self):
        """Init."""
        super().__init__()

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        lonches = """Jamón,Carnes Frias,Choriqueso,Campirana,Pechuga,Bistec,
                     Cubana,Pierna,Pibil,Adobada,Arrachera,Torréon,
                     Vegetariana"""

        menu = Menu.Menu(lonches)
        layout = QHBoxLayout()
        layout.addWidget(menu)
        self.setLayout(layout)


app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
sys.exit(app.exec_())
