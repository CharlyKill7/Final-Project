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
event_mensaje_enviado = threading.Event()

time.sleep(1)

def enviar_mensaje(mensaje):
    try:
        socket_pub.send(mensaje.encode())
    except Exception as e:
        print(f"Ocurrió un error al enviar el mensaje: {e}")
        logging.error(f"Ocurrió un error al enviar el mensaje: {e}")
    event_mensaje_enviado.set()   # señalar que el mensaje se ha enviado

while True:
    try:
        # Leer un fragmento de audio
        with mic as fuente:
            r.adjust_for_ambient_noise(fuente)
            sound = r.listen(fuente)
            result = r.recognize_google(sound, language="es-ES")
            print('1')

            try:
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
                        event_mensaje_enviado.clear()   # borrar la señal
                        threading.Thread(target=enviar_mensaje, args=(mensaje,)).start()

                    if result.split()[0] == 'consulta':
                        print('chat msg')
                        mensaje = result
                        event_mensaje_enviado.clear()   # borrar la señal
                        threading.Thread(target=enviar_mensaje, args=(mensaje,)).start()

                    # Esperar a que se envíe el mensaje actual antes de continuar
                    event_mensaje_enviado.wait()

                print('3')

            except Exception as e:
                print("Ocurrió un error al procesar el mensaje:", e)
                logging.error(f"Ocurrió un error al procesar el mensaje: {e}")

        time.sleep(0.1)

    except sr.RequestError as e:
        print("No se pudo completar la solicitud:", e)
        logging.error(f"No se pudo completar la solicitud: {e}")
        time.sleep(0.1)

