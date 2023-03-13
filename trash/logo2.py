import zmq
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

context = zmq.Context()
socket_rec = context.socket(zmq.SUB)
socket_rec.connect("tcp://127.0.0.1:7777")
socket_rec.setsockopt_string(zmq.SUBSCRIBE, "")

while True:

    try:

        trigger = socket_rec.recv_string()

        if trigger == 'logo':

            class Luna(QtWidgets.QWidget):
                def __init__(self):
                    super().__init__()

                    # Cargamos la imagen de la luna
                    self.luna = QtGui.QPixmap(r"img\crescent-moon-moon-svgrepo-com.svg")

                    # Configuramos la ventana principal
                    self.setWindowTitle("Luna")
                    self.setGeometry(35, 35, 70, 70)
                    self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
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

            if __name__ == "__main__":
                app = QtWidgets.QApplication(sys.argv)
                luna = Luna()
                luna.show()
                sys.exit(app.exec_())
        
    except:
        continue
                