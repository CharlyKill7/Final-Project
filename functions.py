

def procesar_mensaje(message0):

    message = str(message0)

    raw = message.split('"')[-2]

    words = raw.split()

    mode = words[0]

    indext = words.index('texto')

    text = ' '.join(words[indext+1:])

    name = ' '.join(words[1:indext])

    return mode, text, name

def procesar_mensaje2(message):

    words = message.split()
    mode = words[0]
    text = ''
    name = ''

    if 'texto' in words:
        index_texto = words.index('texto')
    if index_texto < len(words) - 1:
        text = ' '.join(words[index_texto+1:])
    if index_texto > 1:
        name = ' '.join(words[1:index_texto])
        
    return mode, text, name


def get_barra(x):

    if "}" in x and x[x.rfind("}")+1:].strip() != '':

        posicion = x.rfind("}")
        barra = x[posicion+1:].strip()

        return barra

def get_barra2(x):
    if isinstance(x, dict) and 'alternative' in x:
        alternatives = x['alternative']
        if alternatives:
            return alternatives[0]['transcript']
    return None

  







