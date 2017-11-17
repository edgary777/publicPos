import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import Menu
import TextInput
import Holder


class MainWindow(QWidget):
    """Main window widget."""

    def __init__(self):
        """Init."""
        super().__init__()

        self.initUi()

    def initUi(self):
        """Ui Setup."""
        holder = Holder.Holder(parent=self)

        lonches = """Jamón,Carnes Frias,Choriqueso,Campirana,Pechuga,Bistec,
                     Cubana,Pierna,Pibil,Adobada,Arrachera,Torréon,
                     Vegetariana"""

        bebidas = """Coca,Coca Light,Sprite,Fanta,Fanta Fresa,Fresca,Manzanita,
                     Agua,Naranjada,Limonada,ValleFrut,N Durazno,
                     N Guayaba,N Manzana,N Mango,J Manzana"""

        menuLonches = Menu.Menu(lonches, parent=self, hold=holder)
        menuBebidas = Menu.Menu(bebidas, parent=self, hold=holder)

        itemsLayout = QStackedLayout()
        itemsLayout.addWidget(menuLonches)
        itemsLayout.addWidget(menuBebidas)

        tabs = {"Lonches": (0, itemsLayout), "Bebidas": (1, itemsLayout)}
        tabsWidget = Menu.Tabs(tabs, parent=self)
        tabsLayout = QHBoxLayout()
        tabsLayout.addWidget(tabsWidget)

        inputField = TextInput.TextInput()


        layoutC1 = QVBoxLayout()
        layoutC1.addWidget(holder)

        layoutC2 = QVBoxLayout()
        layoutC2.addLayout(tabsLayout)
        layoutC2.addLayout(itemsLayout)
        layoutC2.addWidget(inputField)

        layout = QHBoxLayout()
        layout.addLayout(layoutC1)
        layout.addLayout(layoutC2)

        self.setLayout(layout)

    def paintEvent(self, event):
        """Set window background color."""
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)


app = QApplication(sys.argv)
window = MainWindow()
window.showMaximized()
sys.exit(app.exec_())
