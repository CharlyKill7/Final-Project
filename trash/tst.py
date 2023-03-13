import speech_recognition as sr

# Crea un objeto de reconocimiento de voz
r = sr.Recognizer()

while True:
# Utiliza el micrófono como fuente de entrada
    with sr.Microphone() as source:
        # Ajusta el nivel de ruido de fondo para eliminar el ruido no deseado
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # Intenta reconocer lo que se dijo
    try:
        text = r.recognize_google(audio, language="es-ES")
        print(text)
        print(type(text))
    except sr.UnknownValueError:
        print("No se pudo reconocer lo que dijiste.")
    except sr.RequestError as e:
        print(f"No se pudo solicitar resultados de Google Speech Recognition service; {e}")

        break