from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import zmq
import threading

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 400)
        
        # Cargamos la imagen de la luna
        self.luna = QtGui.QPixmap(r"img\crescent-moon-moon-svgrepo-com.svg")
        self.luna_label = QtWidgets.QLabel(MainWindow)
        self.luna_label.setPixmap(self.luna)
        self.luna_label.setGeometry(QtCore.QRect(0, 0, 50, 50))
        
        # Agregamos un widget de texto para imprimir los mensajes de la terminal
        self.terminal_output = QtWidgets.QTextEdit(MainWindow)
        self.terminal_output.setGeometry(QtCore.QRect(50, 50, 350, 300))
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Luna"))

    def set_luna(self, activo=True):
        # Actualizamos la imagen de la luna segun si el sistema esta activo o no
        if activo:
            self.luna = QtGui.QPixmap("luna.png")
        else:
            self.luna = QtGui.QPixmap("luna_inactiva.png")
        self.luna_label.setPixmap(self.luna)
        
    def show_terminal_output(self, output):
        # Actualizamos el widget de texto con la salida de la terminal
        self.terminal_output.setText(output)
        
    def show_msg_enviado(self):
        # Mostramos un mensaje de enviado con exito
        QtWidgets.QMessageBox.information(self, "Mensaje enviado", "Mensaje enviado con éxito")

class LunaUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.context = zmq.Context()
        self.socket_sub = self.context.socket(zmq.SUB)
        self.socket_sub.connect("tcp://127.0.0.1:7777")
        self.socket_sub.subscribe("")
        self.socket_thread = threading.Thread(target=self.recibir_mensajes)
        self.socket_thread.start()
    
    def recibir_mensajes(self):
        while True:
            try:
                mensaje = self.socket_sub.recv_string()
                print(mensaje)
                self.show_terminal_output(mensaje)
                self.show_msg_enviado()
                
            except Exception as e:
                print("Ocurrió un error al recibir un mensaje:", e)
                continue


# Inicializamos la aplicación de PyQt
app = QtWidgets.QApplication([])

# Creamos la ventana principal
ui = LunaUI()

# Mostramos la ventana principal
ui.show()

# Ejecutamos el event loop principal de PyQt
sys.exit(app.exec_())
