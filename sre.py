import speech_recognition as sr

# Configurar el reconocimiento de voz
r = sr.Recognizer()
r.pause_threshold = 0.5
r.phrase_threshold = 0.3
r.non_speaking_duration = 0.2
r.energy_threshold = 300

# Definir las palabras clave
grabar = "luna"
parar = "tierra"

# Variable de control
recording = False

# Inicializar el micrófono
mic = sr.Microphone()

# Bucle de reconocimiento de voz
with mic as fuente:
    r.adjust_for_ambient_noise(fuente)

    while True:
        try:
            sonido = r.listen(fuente)
            palabras = r.recognize_google(sonido, language="es-ES")
            if grabar in palabras and not recording:
                recording = True
                #print("Comenzando a grabar...")

            if parar in palabras and recording:
                recording = False
                #print("Deteniendo la grabación...")

            #if recording:
                #print(palabras)

        
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            break


           