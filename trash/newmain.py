import speech_recognition as sr
import time
import zmq
import threading
import logging
import os
from PyQt5 import QtWidgets, QtCore, QtGui
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
last_sent_message = None  # Inicializar la variable

# Definir función para enviar mensajes por Whatsapp
# Definir función para enviar mensajes por Whatsapp
def enviar_whatsapp(mensaje):
    global enviando_mensaje
    global last_sent_message 
    
    # Verificar si el mensaje actual es igual al último mensaje enviado
    if mensaje == last_sent_message:
        return
    
    # Verificar si ya se está enviando un mensaje
    if enviando_mensaje:
        return
    
    # Bloquear el hilo para evitar que se envíen varios mensajes al mismo tiempo
    with lock:
        enviando_mensaje = True
        try:
            socket_pub.send(mensaje.encode())
        finally:
            enviando_mensaje = False
        
    os.system(f"python wapp.py '{mensaje}'")
    
    # Actualizar la variable last_sent_message
    last_sent_message = mensaje

def enviar_chat(mensaje):
    global enviando_mensaje
    
    with lock:
        enviando_mensaje = True
        try:
            socket_pub.send(mensaje.encode())
        finally:
            enviando_mensaje = False
        
    os.system(f"python chat2.py '{mensaje}'")

logging.basicConfig(filename='log.txt', level=logging.DEBUG)

context = zmq.Context()
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://127.0.0.1:7777")

time.sleep(1)

class MyThread(QtCore.QThread):
    def run(self):
        global grabando
        luna = Luna()
        luna.show()

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
                    enviando_mensaje = False  # Inicializar enviando_mensaje en False cuando se activa la grabación
                    print("Grabando...")

                    # Hacer que la luna desaparezca
                    #luna.cambiar_visibilidad(False)
                    
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

                    elif result.split()[0] == 'consulta':
                        print('chat msg')
                        mensaje = result
                        enviando_mensaje = True
                        threading.Thread(target=enviar_chat, args=(mensaje,)).start()   
                    
                    # Esperar a que se complete el envío del mensaje actual antes de continuar
                    start_time = time.time()
                    while enviando_mensaje:
                        if time.time() - start_time > 5: # si han pasado más de 10 segundos
                            enviando_mensaje = False
                        time.sleep(0.1)
                    
                    # establecer enviando_mensaje en False después de esperar el mensaje actual
                    enviando_mensaje = False
                
                time.sleep(0.2)
                print('3')
                
            except Exception as e:
                print("Ocurrió un error:", e)
                logging.error(f"Ocurrió un error: {e}")
                enviando_mensaje = False  # Establecer enviando_mensaje en False en caso de error
                time.sleep(0.2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    luna = Luna()
    luna.show()
    
    # Iniciar el ciclo principal de la aplicación en segundo plano
    QtCore.QTimer.singleShot(0, app.exec_)
    
    # Crear y ejecutar el hilo
    thread = MyThread()
    thread.start()
    
    # Salir del programa cuando se cierra la ventana de la aplicación
    sys.exit(app.exec_())
