from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class VentanaTexto(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # Configuramos la ventana principal
        self.setWindowTitle("Ventana de texto")
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowTransparentForInput
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Configuramos el layout y añadimos el campo de texto
        layout = QtWidgets.QVBoxLayout(self)
        self.texto = QtWidgets.QPlainTextEdit()
        layout.addWidget(self.texto)

        # Ajustamos el tamaño de la ventana y la posición
        self.setGeometry(0, 0, 400, 300)
        screen = QtWidgets.QApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
        self.move(screen_rect.right() - self.width(), screen_rect.bottom() - self.height())

def main():
    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaTexto()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
