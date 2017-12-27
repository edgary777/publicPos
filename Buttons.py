from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MenuBtn(QAbstractButton):
    """
    Menu Button.

    Color can be any qcolor argument (e.g. Qt.red, qRgb(), etc...)

    style is a stylesheet as 'QLabel { color : color;'
    """

    def __init__(self, width, height, rounded, color, data, style,
                 parent, holder, product=None):
        """Init.

        product is meant to be the product ID and it is to be emmited
        as a signal when the button is clicked so the ticket knows
        which item it is.
        """
        super().__init__(parent)

        self.widths = width
        self.heights = height
        self.rounded = rounded
        col = [int(color.strip()) for color in color.split(',')]
        self.color = QColor(qRgb(col[0], col[1], col[2]))
        self.data = data
        self.text = style
        self.holder = holder

        # If this is activated the buttons will grow with the screen
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        label = QLabel(self.data[1])
        label.setStyleSheet(style)
        label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        # self.setFixedSize(self.width, self.height)

    def mousePressEvent(self, QMouseEvent):
        """Reimplement mouse events."""
        if QMouseEvent.button() == Qt.LeftButton:
            print(self.data)
            li = [self.data[1], 1, self.data[2]]
            order = self.holder.getOrder()
            order.addItem(li)
        elif QMouseEvent.button() == Qt.RightButton:
            pass

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

    ActiveId = None

    def __init__(self, width, height, rounded, color1, color2, label, style,
                 parent, index=None, obj=None):
        """Init."""
        super().__init__(parent)

        self.widths = width
        self.heights = height
        self.rounded = rounded
        self.label = label
        self.text = style
        self.index = index
        self.obj = obj

        if self.label == self.obj.activeSession:
            self.color = QColor(color2)
        else:
            self.color = QColor(color1)

        # If this is activated the buttons will grow with the screen
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

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
            self.obj.deleteSession(session, self.index)

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


class PicButton(QAbstractButton):
    """Creates an image button with static, hovered, and clicked states.

    Functionality is mostly the same as QPushButton.
    """

    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent):
        """Init."""
        super().__init__(parent)
        self.pixmap = QPixmap(pixmap)
        self.pixmap_hover = QPixmap(pixmap_hover)
        self.pixmap_pressed = QPixmap(pixmap_pressed)

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        """Paint Event."""
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        """Enter event."""
        self.update()

    def leaveEvent(self, event):
        """Leave event."""
        self.update()

    def sizeHint(self):
        """Size hint."""
        return self.pixmap.size()
