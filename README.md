# LUNA - Asistente Virtual por voz

## Índice

1. [Descripción](#descripción)
2. [Archivos](#archivos)
3. [Ejecución](#ejecución)


<a name="descripción"/>

## Descripción del proyecto

Este proyecto nace de las ganas de seguir aprendiendo. Tras mis primeros dos meses programando, necesitaba poner a prueba las habilidades que he adquirido en el bootcamp de Ironhack, y también ir un poco más allá. Atraído por la parte más "ingeniera" de los datos, he decidido explorar nuevas formas de usar Python para crear un pequeño Asistente Virtual por voz. LUNA, ese sátelite que, aunque no siempre veamos siempre está, pretende ser un programa en segundo plano que siempre está escuchando.

Cuando oye la palabra 'LUNA', se activa. En ese momento está lista para ejecutar cualquiera de las tres funciones básicas que tiene:

- Consultas al Chat GPT: comando de voz "consulta" + la consulta que deseas realizar.
- Envío de mensajes por WhatsApp: comando de voz "whastapp" + "nombre de contacto" + "texto" + "mensaje a enviar".
- Música o vídeo en YouTube: comando de voz "youtube" + el título del vídeo que buscas.

Tanto el envío de WhatsApp como Youtube se ejecutan en ventanas en segundo plano, mientras que la consulta al chat GPT es respondida mediante una ventana emergente con la respuesta en forma de texto, lista para ser copiada. 

Cuando escucha la palabra 'tierra', LUNA se esconde y, aunque no deja de oír hasta el cierre completo del programa, desactiva la escucha activa hasta que vuelva a oir "LUNA".

Así funciona, a grandes rasgos, mi pequeño asistente por voz.

 
 <a name="archivos"/>
 
## Archivos

1. Archivos principales (ubicados en la carpeta principal LUNA):

- <strong>main.py</strong>: script para el reconocimiento de voz y trasncripción.
- <strong>logo.py</strong>: script para mostrar el logo cuando LUNA se activa.
- <strong>wap.py</strong>: script para el envío de mensajes de WhatsApp.
- <strong>you.py</strong>: script para abrir YouTube y poner un vídeo.
- <strong>chat.py</strong>: script para llamar a la API de OpenAI y usar Chat GPT.
- <strong>gui.py</strong>: script para la ventana emergente con la respuesta. 

2. Carpetas accesorias:

- <strong>notebooks</strong>: contiene diferentes notebooks para pruebas: zmq, chat, micro, PySimpleGUI, pips, etc.
- <strong>img</strong>: contiene dos posibles logos en varios formatos (.png, .ico, .svg).
- <strong>driver</strong>: contiene la extensión AdBlocker para la librería selenium.

3. Otros archivos:

- <strong>functions.py</strong>: script con funciones.
- <strong>LUNA.txt</strong>: script para la creación del archivo ejecutable .bat.
- <strong>LUNA.bat</strong>: archivo ejecutable principal.
- <strong>LUNA.lnk</strong>: acceso directo al archivo .bat, el ejecutable principal (para colocar donde se requiera).
- <strong>desktop.ini</strong>: archivo necesario para la creación del acceso directo.


 <a name="ejecucion"/>
 
## Ejecución

Para poner en marcha LUNA, se deben seguir los siguientes pasos:

- Crea un entorno virtual nuevo para el proyeto (opcional).
- Descarga este repositorio en local.
- Corre el archivo 'pips.ipynb' para instalar las librerías necesarias (en caso de no tenerlas ya instaladas).
- Especifica las rutas de guardado de cookies (opciones de Selenium) en 'you.py' y 'wap.py'.
- Asegúrate de que los puertos especificados para los sockets de ZeroMQ están libres o, en caso contrario, especifica uno nuevo (en todos los archivos principales).
- Ejecuta los seis archivos principales a la vez, cada uno con su propia terminal.

En caso de querer hacer un único ejecutable:
- Desde la terminal, navega hasta la carpeta de proyecto y ejecuta el comando "pyinstaller archivo.py", donde "archivo.py" debe ser remplazado por 'main.py'.
- Repetir el proceso para los otros cinco archivos. Se crearán dos carpetas nuevas llamadas "build" y "dist", y dentro de ésta última se encuentran los archivos ejecutables creados ('main.exe', 'chat.exe', 'gui.exe', etc), cada uno en una carpeta con su nombre.
- Doble click en el ejecutable 'LUNA.bat'. En caso de no funcionar, consultar el archivo 'LUNA.txt' y comprobar si las rutas son correctas. En caso de que no lo sean, cambiarlas y después renombrar ese mismo archivo con extensión .bat, convirtiéndolo así en el ejecutable principal.
- Usar el acceso directo (el que tiene icono) donde se prefiera.

Y eso es todo.

Ojalá disfrutéis usando LUNA tanto como yo desarrollándola. ¡Gracias!

<br>
<br>
<br>

<img src="https://github.com/CharlyKill7/LUNA/blob/main/img/luna.png" alt="luna_logo" style="width: 15%; height: auto;">

