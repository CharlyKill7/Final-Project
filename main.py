import speech_recognition as sr
import time
import zmq
import threading
import logging

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

time.sleep(1)

def enviar_mensaje(mensaje):
    global enviando_mensaje
    
    # Bloquear el hilo para evitar que se envíen varios mensajes al mismo tiempo
    with lock:
        socket_pub.send(mensaje.encode())
        enviando_mensaje = False   # establecer enviando_mensaje en False después de enviar el mensaje

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
                socket_pub.send_string('logo')
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
                    threading.Thread(target=enviar_mensaje, args=(mensaje,)).start()

                if result.split()[0] == 'consulta':
                    print('chat msg')
                    mensaje = result
                    enviando_mensaje = True
                    threading.Thread(target=enviar_mensaje, args=(mensaje,)).start()   
                
                # Esperar a que se complete el envío del mensaje actual antes de continuar
                while enviando_mensaje:
                    time.sleep(0.1)
                
                # establecer enviando_mensaje en False después de esperar el mensaje actual
                enviando_mensaje = False
            print('3')
            
    except Exception as e:
        print("Ocurrió un error:", e)
        logging.error(f"Ocurrió un error: {e}")
        time.sleep(0.1)
        continue

