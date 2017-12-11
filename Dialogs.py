from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class DctDialog(QDialog):
    """Pop-Up window to set a discount for an order."""

    def __init__(self, total, parent, percentage=None, amount=None, code=None):
        """Init."""
        super().__init__(parent)

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
        btnCancel = QPushButton("Cancelar")

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(btnOk)
        btnLayout.addWidget(btnCancel)

        layout = QVBoxLayout()
        layout.addStretch()

        items = {"percentage": "%:", "amount": "Cantidad:", "code": "Cupón:"}

        for key, value in items.items():
            setattr(self, key + "Layout", QHBoxLayout())
            setattr(self, key + "Input", QLineEdit())
            getattr(self, key + "Input").setPlaceholderText(getattr(self, key))
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
        self.amountInput.textChanged.connect(lambda:
                                                 self.setAmountDcto(
                                                 self.amountInput.text()
                                                 ))

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

            if self.percentage:
                self.newTotal = self.newTotal - (self.newTotal *
                                                 (self.percentage / 100))
        else:
            self.newTotal = self.total

        self.newTotalLabel.setText(str(self.newTotal))

    def returnDcto(self):
        """Update the order with the discount."""
        if self.newTotal != self.total:
            dcto = 1 - (self.newTotal / self.total)
        else:
            dcto = None
        self.parent.orderTotal.updateDcto(dcto)
