# LUNA - Asistente Virtual por voz

## Índice

1. [Descripción](#descripción)
2. [Archivos](#archivos)
3. [Ejecución](#ejecución)


<a name="descripción"/>

## Descripción del proyecto

Este proyecto nace de las ganas de seguir aprendiendo. Tras mis primeros dos meses programando, necesitaba poner a prueba las habilidades que he adquirido en el bootcamp de Ironhack, y también ir un poco más allá. Atraído por la parte más "ingeniera" de los datos, he decidido explorar nuevas formas de usar Python para crear un pequeño Asistente Virtual por voz. LUNA, ese sátelite que, aunque no siempre veamos siempre está, pretende ser un programa en segundo plano que siempre está escuchando. 

Cuando escucha la palabra 'luna', se activa. En ese momento está preparada para ejecutar cualquiera de las tres funciones básicas que tiene:

- Consultas al Chat GPT: el comando de voz "consulta" + la consulta que deseas realizar.
- Envío de mensajes por WhatsApp: el comando de voz "whastapp" + "nombre de contacto" + "texto" + "mensaje a enviar".
- Música o vídeo en YouTube: el comando de voz "youtube" + el título del vídeo que buscas.

Tanto el envío de WhatsApp como Youtube se ejecutan en ventanas en segundo plano, mientras que la consulta al chat GPT es respondida mediante una ventana emergente con la respuesta, lista para ser copiada. 

Cuando escucha la palabra 'tierra', LUNA se esconde y, aunque no deja de oír hasta el cierre completo del programa, desactiva la escucha activa hasta que vuelva a oir "luna".

Así funciona, a grandes rasgos, LUNA - Asistente Virtual por voz.

 
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

Aunque el enfoque más adecuado sería intentar minimizar el error, probando desde lo más simple a lo más complejo, lo que aquí pretendimos fue probar varios tipos de encoders, sin dejar de mirar, obviamente, la mejor opción en cada caso. Aunque One Hot Encoding suele funcionar bien, decidí utilizarlo sólo para las columnas cuyos valores no tuvieran una relación jerarquica con respecto de la variable objetivo. Éstas fueron remote_ratio y employment_type.

<br>
<br>
<br>

<div style="text-align: center;">
  <img src="https://github.com/CharlyKill7/LUNA/blob/main/img/luna.png" alt="luna_logo" style="width:45%;" style="display: inline-block;">
</div>
