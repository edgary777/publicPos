from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class DctDialog(QDialog):
    """Pop-Up window to set a discount for an order."""

    def __init__(self, total, parent, percentage=None, amount=None, code=None):
        """Init."""
        super().__init__(parent, Qt.FramelessWindowHint |
                         Qt.WindowSystemMenuHint)

        self.parent = parent
        self.total = total
        self.newTotal = total
        self.percentage = percentage
        self.amount = amount
        self.code = code

        self.initUi()

        self.newTotalUpdate()

    def initUi(self):
        """UI setup."""
        self.newTotalLabel = QLabel(str(self.total))
        btnOk = QPushButton("Aceptar")
        btnOk.clicked.connect(self.returnDcto)
        btnCancel = QPushButton("Cancelar")
        btnCancel.clicked.connect(self.reject)

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(btnOk)
        btnLayout.addWidget(btnCancel)

        layout = QVBoxLayout()
        layout.addStretch()

        items = {"percentage": "%:", "amount": "Cantidad:", "code": "Cupón:"}

        for key, value in items.items():
            setattr(self, key + "Layout", QHBoxLayout())
            setattr(self, key + "Input", QLineEdit())
            if getattr(self, key):
                getattr(self, key + "Input").setText(str(getattr(self, key)))
            setattr(self, key + "Label", QLabel(value))
            getattr(self, key + "Label").setAlignment(Qt.AlignRight)
            getattr(self, key + "Layout").addWidget(getattr(self, key +
                                                            "Label"))
            getattr(self, key + "Layout").addWidget(getattr(self, key +
                                                            "Input"))
            layout.addLayout(getattr(self, key + "Layout"))

        self.percentageInput.textChanged.connect(lambda:
                                                 self.setPercentageDcto(
                                                 self.percentageInput.text()
                                                 ))

        validator = QIntValidator(0, 100, self)
        validator2 = QIntValidator(0, int(self.total), self)
        self.percentageInput.setValidator(validator)
        self.amountInput.setValidator(validator2)

        self.amountInput.textChanged.connect(lambda:
                                             self.setAmountDcto(
                                             self.amountInput.text()))

        layout.addStretch()
        layout.addWidget(self.newTotalLabel)
        layout.addLayout(btnLayout)

        self.setLayout(layout)

        # self.setFixedWidth(300)
        # self.setFixedHeight(300)

    def setAmountDcto(self, dcto):
        """Set discount amount."""
        try:
            dcto = float(dcto)
            if dcto and dcto > 0:
                self.amount = dcto
            else:
                self.amount = None
            self.newTotalUpdate()
        except ValueError:
            self.amount = None
            self.newTotalUpdate()

    def setPercentageDcto(self, dcto):
        """Set discount percentage."""
        try:
            dcto = float(dcto)
            if dcto and dcto > 0:
                self.percentage = dcto
            else:
                self.percentage = None
            self.newTotalUpdate()
        except ValueError:
            self.percentage = None
            self.newTotalUpdate()

    def setCodeDcto(self, code):
        """Search and apply a code discount.

        The search returns a list with 2 items, the first item is the type of
        discount, the second item is the amount of discount.
        """
        pass

    def newTotalUpdate(self):
        """Update total with new discounts."""
        self.newTotal = self.total
        if self.percentage or self.amount:
            if self.amount:
                self.newTotal = self.newTotal - self.amount

            if self.percentage and self.percentage > 0:
                self.newTotal = self.newTotal - (self.newTotal *
                                                 (self.percentage / 100))
        else:
            self.newTotal = self.total

        self.newTotal = round(self.newTotal, 2)

        self.newTotalLabel.setText(str(self.newTotal))

    def returnDcto(self):
        """Update the order with the discount."""
        if self.newTotal != self.total:
            dcto = [None, None, None, None]
            dcto[0] = 1 - (self.newTotal / self.total)
            dcto[1] = self.percentage
            dcto[2] = self.amount
            dcto[3] = self.code
        else:
            dcto = [0, None, None, None]
        self.parent.orderTotal.updateDcto(dcto)
        self.accept()


class PopOrderDialog(QDialog):
    """Dialog to hold PopOrderWidget."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent, Qt.FramelessWindowHint |
                         Qt.WindowSystemMenuHint)

        self.parent = parent

        self.setFixedSize(300, 300)

        self.initUi()

    def initUi(self):
        """Ui is created here."""
        self.pop = PopOrderWidget(self)

        layout = QVBoxLayout()

        area = QScrollArea()
        area.setWidgetResizable(True)

        area.setWidget(self.pop)

        btnOk = QPushButton("OK")
        btnCancel = QPushButton("Cancelar")

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(btnOk)
        btnLayout.addWidget(btnCancel)

        layout.addWidget(area)
        layout.addLayout(btnLayout)

        self.setLayout(layout)

    def getParent(self):
        """Return parent."""
        return self.parent


class PopOrderWidget(QWidget):
    """Widget to select items to pop from one order to another one."""

    def __init__(self, parent):
        """Init."""
        super().__init__(parent)

        self.parent = parent
        self.order = self.parent.getParent().holder.getOrder()
        self.items = self.order.getItems()

        self.initUi()

    def initUi(self):
        """UI setup."""
        layout = QVBoxLayout()
        x = 0
        for item in self.items:
            name = item.getName()
            x1 = str(x)
            setattr(self, "layout" + x1, QHBoxLayout())
            setattr(self, "quant" + x1, QSpinBox())
            getattr(self, "quant" + x1).setRange(0, item.getQuant())
            setattr(self, "label" + x1, QLabel(name))
            getattr(self, "layout" + x1).addWidget(getattr(self, "quant" + x1))
            getattr(self, "layout" + x1).addWidget(getattr(self, "label" + x1))
            layout.addLayout(getattr(self, "layout" + x1))
            x += 1

        layout.addStretch()

        self.setLayout(layout)
