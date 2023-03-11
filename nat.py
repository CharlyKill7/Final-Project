import speech_recognition as sr
import time
import zmq

from functions import get_barra

context = zmq.Context()
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://127.0.0.1:7777")

# Configurar el dispositivo de audio
r = sr.Recognizer()
r.pause_threshold = 1
r.phrase_threshold = 0.25
r.non_speaking_duration = 1
r.energy_threshold = 600

mic = sr.Microphone()

# Definir las palabras clave
clave = "luna"
clave_stop = "tierra"

# Variables de control
grabando = False

time.sleep(8)
    
while True:
    # Leer un fragmento de audio
    with mic as fuente:
        r.adjust_for_ambient_noise(fuente)
        sound = r.listen(fuente)
        try:
            result = r.recognize_google(sound, language="es-ES")
            if not grabando and clave in result.lower():
                grabando = True
                print("Grabando...")
            elif grabando and clave_stop in result.lower():
                grabando = False
                print("Deteniendo...")
            if grabando:
                print(result)
                socket_pub.send_string(result)
        except sr.UnknownValueError:
            pass

