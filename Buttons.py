from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MenuBtn(QAbstractButton):
    """
    Menu Button.

    Color can be any qcolor argument (e.g. Qt.red, qRgb(), etc...)

    style is a stylesheet as 'QLabel { color : color;'
    """

    def __init__(self, width, height, rounded, color, label, style,
                 parent, product=None, holder=None):
        """Init.

        product is meant to be the product ID and it is to be emmited
        as a signal when the button is clicked so the ticket knows
        which item it is.
        """
        super().__init__(parent)

        self.widths = width
        self.heights = height
        self.rounded = rounded
        self.color = QColor(color)
        self.label = label
        self.text = style
        self.holder = holder

        # If this is activated the buttons will grow with the screen
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        """The text passed as label is later transformed into a QLabel object
        so this is a copy to be able to use it afterwards"""
        labelText = label

        # self.clicked.connect(lambda: print(labelText))
        order = self.holder.getOrder()
        li = [labelText, 1, 50]
        if self.holder:
            self.clicked.connect(lambda: order.addItem(li))

        label = QLabel(self.label)
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # self.setFixedSize(self.width, self.height)

    def paintEvent(self, event):
        """Paint Event."""
        # If the mouse is over the button make the color lighter
        color = self.color.lighter(130) if self.underMouse() else self.color

        # If the button is being pressed then make it darker
        if self.isDown():
            color = self.color.darker(110)

        # Set up the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create the path for the figure
        path = QPainterPath()
        path.addRoundedRect(QRectF(0.0, 0.0, self.width(), self.height()),
                            self.rounded, self.rounded)

        # Fill the paths with color
        painter.fillPath(path, color)

    def minimumSizeHint(self):
        """Set the minimum size hint."""
        return QSize(self.widths, self.heights)


class StrokeBtn(QAbstractButton):
    """
    Stroke Button.

    Color can be any qcolor argument (e.g. Qt.red, qRgb(), etc...)

    style is a stylesheet as 'QLabel { color : color;'
    """

    def __init__(self, width, height, rounded, color, label, style,
                 parent, index=None, obj=None):
        """Init."""
        super().__init__(parent)

        self.widths = width
        self.heights = height
        self.rounded = rounded
        self.color = QColor(color)
        self.label = label
        self.text = style
        self.index = index
        self.obj = obj

        # If this is activated the buttons will grow with the screen
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        """The text passed as label is later transformed into a QLabel object
        so this is a copy to be able to use it afterwards"""
        labelText = label

        self.clicked.connect(lambda: self.obj.setCurrentIndex(self.index))

        label = QLabel(self.label)
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # self.setFixedSize(self.width, self.height)

    def paintEvent(self, event):
        """Paint Event."""
        # If the mouse is over the button make the color lighter
        color = self.color.lighter(130) if self.underMouse() else self.color

        # If the button is being pressed then make it darker
        if self.isDown():
            color = self.color.darker(110)

        # Set up the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create the path for the big figure
        path = QPainterPath()
        path.addRoundedRect(QRectF(0.0, 0.0, self.width(), self.height()),
                            self.rounded, self.rounded)

        # Calculate the percentage ratio to get a 10 px margin
        ratioX = (1 - ((10 / self.width()) * 2))
        ratioY = (1 - ((10 / self.height()) * 2))

        # calculate the distance the shape has to be moved to be centered
        x = (self.width() - (self.width() * ratioX)) / 2
        y = (self.height() - (self.height() * ratioY)) / 2

        # Create the path for the small figure
        path2 = QPainterPath()
        path2.addRoundedRect(QRectF(x, y, self.width() * ratioX,
                             self.height() * ratioY), self.rounded * ratioY,
                             self.rounded * ratioY)

        # Fill the paths with color
        painter.fillPath(path, color)
        painter.fillPath(path2, Qt.white)

    def minimumSizeHint(self):
        """Set the minimum size hint."""
        return QSize(self.widths, self.heights)


class SessionBtn(QAbstractButton):
    """
    Session Button.

    Button to switch between the sessions

    Color can be any qcolor argument (e.g. Qt.red, qRgb(), etc...)

    style is a stylesheet as 'QLabel { color : color;'
    """

    def __init__(self, width, height, rounded, color, label, style,
                 parent, index=None, obj=None):
        """Init."""
        super().__init__(parent)

        self.widths = width
        self.heights = height
        self.rounded = rounded
        self.color = QColor(color)
        self.label = label
        self.text = style
        self.index = index
        self.obj = obj

        # If this is activated the buttons will grow with the screen
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.clicked.connect(lambda: self.obj.switchSession(self.index))

        label = QLabel(str(self.label))
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # self.setFixedSize(self.width, self.height)

    def mousePressEvent(self, QMouseEvent):
        """Reimplement mouse events."""
        if QMouseEvent.button() == Qt.LeftButton:
            self.obj.switchSession(self.index)
        elif QMouseEvent.button() == Qt.RightButton:
            session = self.obj.sessions[self.index]
            self.obj.deleteSession(session)

    def paintEvent(self, event):
        """Paint Event."""
        # If the mouse is over the button make the color lighter
        color = self.color.lighter(130) if self.underMouse() else self.color

        # If the button is being pressed then make it darker
        if self.isDown():
            color = self.color.darker(110)

        # Set up the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create the path for the big figure
        path = QPainterPath()
        path.addRoundedRect(QRectF(0.0, 0.0, self.width(), self.height()),
                            self.rounded, self.rounded)

        # Calculate the percentage ratio to get a 10 px margin
        ratioX = (1 - ((10 / self.width()) * 2))
        ratioY = (1 - ((10 / self.height()) * 2))

        # calculate the distance the shape has to be moved to be centered
        x = (self.width() - (self.width() * ratioX)) / 2
        y = (self.height() - (self.height() * ratioY)) / 2

        # Create the path for the small figure
        path2 = QPainterPath()
        path2.addRoundedRect(QRectF(x, y, self.width() * ratioX,
                             self.height() * ratioY), self.rounded * ratioY,
                             self.rounded * ratioY)

        # Fill the paths with color
        painter.fillPath(path, color)
        painter.fillPath(path2, Qt.white)

    def minimumSizeHint(self):
        """Set the minimum size hint."""
        return QSize(self.widths, self.heights)


class NewSessionBtn(QAbstractButton):
    """
    New Session Button.

    Adds a new session to the MultiSession

    Color can be any qcolor argument (e.g. Qt.red, qRgb(), etc...)

    style is a stylesheet as 'QLabel { color : color;'
    """

    def __init__(self, width, height, rounded, color, style,
                 parent, obj):
        """Init.

        product is meant to be the product ID and it is to be emmited
        as a signal when the button is clicked so the ticket knows
        which item it is.
        """
        super().__init__(parent)

        self.widths = width
        self.heights = height
        self.rounded = rounded
        self.color = QColor(color)
        self.text = style
        self.obj = obj
        self.label = "+"

        # If this is activated the buttons will grow with the screen
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.clicked.connect(lambda: obj.createSession())

        label = QLabel(self.label)
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # self.setFixedSize(self.width, self.height)

    def paintEvent(self, event):
        """Paint Event."""
        # If the mouse is over the button make the color lighter
        color = self.color.lighter(130) if self.underMouse() else self.color

        # If the button is being pressed then make it darker
        if self.isDown():
            color = self.color.darker(110)

        # Set up the painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create the path for the figure
        path = QPainterPath()
        path.addRoundedRect(QRectF(0.0, 0.0, self.width(), self.height()),
                            self.rounded, self.rounded)

        # Fill the paths with color
        painter.fillPath(path, color)

    def minimumSizeHint(self):
        """Set the minimum size hint."""
        return QSize(self.widths, self.heights)
