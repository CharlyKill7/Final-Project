from PyQt5 import QtCore, QtGui, QtWidgets

class Luna(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Cargamos la imagen de la luna
        self.luna = QtGui.QPixmap(r"img\crescent-moon-moon-svgrepo-com.svg")
        
        # Establecer la propiedad WA_StyledBackground en True
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # Configuramos la ventana principal
        screen_rect = QtWidgets.QApplication.desktop().availableGeometry()
        self.setWindowTitle("Luna")
        self.setGeometry(
            screen_rect.width() - 100,
            screen_rect.height() - 100,
            100,
            100
        )
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self.luna)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def cambiar_visibilidad(self, condicion):
        if condicion:
            self.show()
        else:
            self.hide()