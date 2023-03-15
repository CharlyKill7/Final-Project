import speech_recognition as sr
import time
import zmq
import threading
import logging


logging.basicConfig(filename='log_main.txt', level=logging.DEBUG)

context = zmq.Context()
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://127.0.0.1:7777")

r = sr.Recognizer()

r.pause_threshold = 0.8
r.phrase_threshold = 0.25
r.non_speaking_duration = 0.5
r.energy_threshold = 8000

mic = sr.Microphone(device_index=1)

clave = "luna"
clave_stop = "tierra"

# Variables de control
grabando = False
enviando_mensaje = False
lock = threading.Lock()

print('Main Ready')
print('----------')
print('¡Bienvenido a LUNA!')

def enviar_mensaje(mensaje):
    global enviando_mensaje
    
    # Bloquear el hilo para evitar que se envíen varios mensajes al mismo tiempo
    with lock:
        socket_pub.send(mensaje.encode())
        enviando_mensaje = False   

while True:
    try:
        print('----------')
        # Leer un fragmento de audio
        with mic as fuente:
            print('Ajustando sonido ambiente...')
            r.adjust_for_ambient_noise(fuente)
            print('Sonido ajustado')
            sound = r.listen(fuente, phrase_time_limit=10)
            #print(sound)
            result = r.recognize_google(sound, language="es-ES")
            #print('1')
            
            if not grabando and clave in result.lower():
                print('----------')
                print("LUNA activada. ¿Qué necesitas?")
                #print('2')
                grabando = True
                socket_pub.send_string('logo')
                
            elif grabando and clave_stop in result.lower():
                grabando = False
                socket_pub.send_string('no_logo')
                print("Entrando en modo de espera")
                
            if grabando and result != 'luna':
                print(result)
                                
                if result.split()[0] == 'whatsapp':
                    print('Mensaje de WhatsApp en curso...')
                    mensaje = result
                    enviando_mensaje = True
                    threading.Thread(target=enviar_mensaje, args=(mensaje,)).start()
                    #print('2.1')

                elif result.split()[0] == 'consulta':
                    print('Consulta en curso...')
                    mensaje = result
                    enviando_mensaje = True
                    threading.Thread(target=enviar_mensaje, args=(mensaje,)).start() 
                    #print('2.2')  
                
                elif result.split()[0].lower() == 'youtube':
                    print('Abriendo Youtube...')
                    mensaje = result
                    enviando_mensaje = True
                    threading.Thread(target=enviar_mensaje, args=(mensaje,)).start() 
                    #print('2.3')  

                else:
                    continue
                
                # Esperar a que se complete el envío del mensaje actual antes de continuar
                while enviando_mensaje:
                    time.sleep(0.1)
                
                # establecer enviando_mensaje en False después de esperar el mensaje actual
                enviando_mensaje = False
            #print('3')
            
    except Exception as e:
        print("Ocurrió un error:", e)
        logging.error(f"Ocurrió un error: {e}")
        time.sleep(0.1)
        continue
