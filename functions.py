def procesar_mensaje(message):
    
    words = mensaje.split()

    mode = words[0]

    indext = words.index('texto')

    text = ' '.join(words[indext+1:])

    name = ' '.join(words[1:indext])

    return mode, text, name

