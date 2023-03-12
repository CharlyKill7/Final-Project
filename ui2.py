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
            self.luna = QtGui.QPixmap(r"img\crescent-moon-moon-svgrepo-com.svg")
        else:
            self.luna = QtGui.QPixmap(r"img\luna_inactiva.png")
        self.luna_label.setPixmap(self.luna)
        
    def show_message(self, message):
        # Imprimimos el mensaje en el widget de texto de la terminal
        self.terminal_output.append(message)
        
class Luna(QtCore.QObject):
    def __init__(self, ip="127.0.0.1", port=7777):
        super().__init__()
        self.ip = ip
        self.port = port
        self.activo = True
        
        # Creamos el contexto y el socket de ZeroMQ
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        self.socket.connect(f"tcp://{self.ip}:{self.port}")
        
        # Creamos la aplicación de PyQt y la ventana principal
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        # Conectamos las señales
        self.ui.set_luna(self.activo)
        self.socket_thread = threading.Thread(target=self.recibir_mensajes)
        self.socket_thread.start()
        
        # Mostramos la ventana principal y ejecutamos el loop de eventos de PyQt
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def recibir_mensajes(self):
        while True:
            # Esperamos un mensaje y lo decodificamos
            message = self.socket.recv().decode()
            
            # Actualizamos el estado del sistema
            if message == "activo":
                self.activo = True
            else:
                self.activo = False
                
            # Actualizamos la imagen de la luna
            self.ui.set_luna(self.activo)
            
            # Mostramos el mensaje en la terminal
            self.ui.show_message(message)

if __name__ == "__main__":
    luna = Luna()
    luna.app.exec_()