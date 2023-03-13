import speech_recognition as sr
import time
import zmq
import threading
import logging
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication

class LunaControl(QObject):
    show_luna_signal = pyqtSignal()
    hide_luna_signal = pyqtSignal()

class Luna(QtWidgets.QWidget):
    def __init__(self, luna_control):
        super().__init__()

        # Cargamos la imagen de la luna
        self.luna = QtGui.QPixmap(r"img\crescent-moon-moon-svgrepo-com.svg")

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

        self.luna_control = luna_control

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

class LunaThread(threading.Thread):
    def __init__(self, luna_control):
        threading.Thread.__init__(self)
        self.luna_control = luna_control

    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        luna = Luna(self.luna_control)
        self.luna_control.show_luna_signal.connect(luna.show)
        self.luna_control.hide_luna_signal.connect(luna.hide)
        sys.exit(app.exec_())

if __name__ == "__main__":
    luna_control = LunaControl()
    luna_thread = LunaThread(luna_control)
    luna_thread.start()

logging.basicConfig(filename='log.txt', level=logging.DEBUG)

context = zmq.Context()
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://127.0.0.1:7777")

# Configurar el dispositivo de audio
r = sr.Recognizer()
r.pause_threshold = 1
r.phrase_threshold = 0.25
r.non_speaking_duration = 1
r.energy_threshold = 1500

mic = sr.Microphone()

# Definir las palabras clave
clave = "luna"
clave_stop = "tierra"

# Variables de control
grabando = False
enviando_mensaje = False
lock = threading.Lock()

# Definir función para enviar mensajes por Whatsapp
def enviar_whatsapp(mensaje):
    global enviando_mensaje
    
    # Bloquear el hilo para evitar que se envíen varios mensajes al mismo tiempo
    with lock:
        socket_pub.send(mensaje.encode())
        enviando_mensaje = False   # establecer enviando_mensaje en False después de enviar el mensaje

    os.system(f"python wapp.py '{mensaje}'")

# Definir función para enviar mensajes por chat
def enviar_chat(mensaje):
    global enviando_mensaje
    
    # Bloquear el hilo para evitar que se envíen varios mensajes al mismo tiempo
    with lock:
        socket_pub.send(mensaje.encode())
        enviando_mensaje = False   # establecer enviando_mensaje en False después de enviar el mensaje

    os.system(f"python chat2.py '{mensaje}'")

time.sleep(7)

while True:
    try:
        # Leer un fragmento de audio
        with mic as fuente:
            r.adjust_for_ambient_noise(fuente)
            sound = r.listen(fuente)
            result = r.recognize_google(sound, language="es-ES")
            print('1')

        if not grabando and clave in result.lower():
            print('2')
            grabando = True
            print("Grabando...")
            
        elif grabando and clave_stop in result.lower():
            grabando = False
            print("Deteniendo...")
            
        if grabando:
            print(result)
            
            if result.split()[0] == 'whatsapp':
                print('wap msg')
                mensaje = result
                enviando_mensaje = True
                threading.Thread(target=enviar_whatsapp, args=(mensaje,)).start()

            if result.split()[0] == 'consulta':
                print('chat msg')
                mensaje = result
                enviando_mensaje = True
                threading.Thread(target=enviar_chat, args=(mensaje,)).start()   
            
            # Esperar a que se complete el envío del mensaje actual antes de continuar
            while enviando_mensaje:
                time.sleep(0.1)
            
            # establecer enviando_mensaje en False después de esperar el mensaje actual
            enviando_mensaje = False
        
        time.sleep(0.2)
        print('3')
        
    except Exception as e:
        print("Ocurrió un error:", e)
        logging.error(f"Ocurrió un error: {e}")
        time.sleep(0.2)
        continue

