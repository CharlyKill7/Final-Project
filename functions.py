def procesar_mensaje(message):

    raw = message.split('"')[-2]

    words = raw.split()

    mode = words[0]

    indext = words.index('texto')

    text = ' '.join(words[indext+1:])

    name = ' '.join(words[1:indext])

    return mode, text, name







