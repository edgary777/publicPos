import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Menu, TextInput


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

        bebidas = """Coca,Coca Light,Sprite,Fanta,Fanta Fresa,Fresca,Manzanita,
                     Agua,Naranjada,Limonada,ValleFrut,N Durazno,
                     N Guayaba,N Manzana,N Mango,J Manzana"""

        tabs = """Lonches,Bebidas,Extras"""

        menuLonches = Menu.Menu(lonches)
        menuBebidas = Menu.Menu(bebidas)
        tabsWidget = Menu.Tabs(tabs)

        itemsLayout = QStackedLayout()
        itemsLayout.addWidget(menuLonches)
        itemsLayout.addWidget(menuBebidas)

        tabsLayout = QHBoxLayout()
        tabsLayout.addWidget(tabsWidget)

        inputField = TextInput.TextInput()

        layout = QVBoxLayout()
        layout.addLayout(tabsLayout)
        layout.addLayout(itemsLayout)
        layout.addWidget(inputField)
        self.setLayout(layout)

    def paintEvent(self, event):
        """Set window background color"""
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)


app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
sys.exit(app.exec_())
