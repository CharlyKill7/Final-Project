from PyQt5 import QtCore, QtGui, QtWidgets

class VentanaTexto(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Configuramos la ventana principal
        self.setWindowTitle("Ventana de texto")
        self.setGeometry(100, 100, 400, 300)

        # Creamos los widgets
        self.texto_edit = QtWidgets.QTextEdit(self)
        self.texto_edit.setGeometry(10, 10, 380, 240)
        self.cerrar_btn = QtWidgets.QPushButton("Cerrar", self)
        self.cerrar_btn.setGeometry(290, 260, 100, 30)

        # Conectamos el botón a la señal clicked
        self.cerrar_btn.clicked.connect(self.close)

    def set_texto(self, texto):
        self.texto_edit.setText(texto)

def main():
    app = QtWidgets.QApplication([])
    ventana_texto = VentanaTexto()
    ventana_texto.show()
    app.exec_()

if __name__ == "__main__":
    main()
