import speech_recognition as sr
import time
import zmq
import threading
import logging
import os
from PyQt5 import QtWidgets, QtCore
import sys

from classes import Luna

r = sr.Recognizer()
r.pause_threshold = 1
r.phrase_threshold = 0.25
r.non_speaking_duration = 1
r.energy_threshold = 1500

mic = sr.Microphone()

clave = "luna"
clave_stop = "tierra"

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

def enviar_chat(mensaje):
    global enviando_mensaje
    
    with lock:
        socket_pub.send(mensaje.encode())
        enviando_mensaje = False   # establecer enviando_mensaje en False después de enviar el mensaje

    os.system(f"python chat2.py '{mensaje}'")

logging.basicConfig(filename='log.txt', level=logging.DEBUG)

context = zmq.Context()
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://127.0.0.1:7777")

time.sleep(1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    luna = Luna()
    luna.show()
    
    # Iniciar el ciclo principal de la aplicación en segundo plano
    QtCore.QTimer.singleShot(0, app.exec_)

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

            # Hacer que la luna desaparezca
            luna.cambiar_visibilidad(False)
            
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
