# LUNA - Asistente Virtual por voz

## Índice

1. [Descripción](#descripción)
2. [Archivos](#archivos)
3. [Ejecución](#encoding)
4. [Modelos](#modelos)
5. [Conclusiones](#conclusion)


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

2. 



<br>
<br>

<img src="https://github.com/CharlyKill7/Salary-Machine-Learning/blob/main/img/tra_1.png" style="width:70%;"/>

<br>
<br>

Decidimos tratar estos valores uno a uno, procurando dar todo el sentido posible a los datos. En el caso de job_title, en 'draft' hicimos unas cuantas pruebas, buscando los puestos más similares en el resto de columnas y asignando el job_title más oportuno en cada caso. Por otro lado, para las otras dos columnas, buscamos en internet los paises más parecidos en cuanto a salarios para el sector IT/Data, y sustituimos en consecuencia por el caso más adecuado de cuantos están en los datos de entrenamiento.

<br>

<img src="https://github.com/CharlyKill7/Salary-Machine-Learning/blob/main/img/tra_2.png" style="width:70%;"/>

<br>
<br>

Hasta aquí el proceso de transformación "clásica".

<br>
<br>

 <a name="encoding"/>
 
## Encoding

Aunque el enfoque más adecuado sería intentar minimizar el error, probando desde lo más simple a lo más complejo, lo que aquí pretendimos fue probar varios tipos de encoders, sin dejar de mirar, obviamente, la mejor opción en cada caso. Aunque One Hot Encoding suele funcionar bien, decidí utilizarlo sólo para las columnas cuyos valores no tuvieran una relación jerarquica con respecto de la variable objetivo. Éstas fueron remote_ratio y employment_type.

<br>

<img src="https://github.com/CharlyKill7/Salary-Machine-Learning/blob/main/img/one_hot.png" style="width:70%;"/>

<br>

Después, decidimos tratar las columnas con pocos valores únicos que pudieran tener una relación jerarquica. Así, work_year, que sigue un orden temporal, company_size, que sigue un orden de tamaños y experience_level, que sigue un orden de experiencia, fueron codificadas con Ordinal Encoder. Como en todos los encodings, vamos haciendo los cambios tanto en train como en test.

<br>

<img src="https://github.com/CharlyKill7/Salary-Machine-Learning/blob/main/img/ordinal.png" style="width:70%;"/>

<br>
<br>
Finalmente, las columnas restantes (job_title, employee_residence y company_location), al tener muchos valores únicos y tener una relación jerárquica en relación al salario, decidimos codificarlas usando Target Encoder, que asigna un código númerico complejo a cada valor en función de su relación con la variable objetivo.

<br>
<br>
<img src="https://github.com/CharlyKill7/Salary-Machine-Learning/blob/main/img/target.png" style="width:70%;"/>

<br>
<br>

<a name="modelos"/>

## Modelos

Una vez transformadas en numéricas todas las columnas, iniciamos el proceso de Machine Learning. A pesar de conocer H20, PyCaret o LazyRegressor, decidimos intentar un grid searching algo más personalizado, y fuimos añadiendo modelos poco a poco, empezando por sus posibles parámetros. El resultado final fue algo así:

<br>

<img src="https://github.com/CharlyKill7/Salary-Machine-Learning/blob/main/img/params.png" style="width:70%;"/>

<br>
<br>
	
Justo después introdujimos los modelos:

<br>

<img src="https://github.com/CharlyKill7/Salary-Machine-Learning/blob/main/img/models.png" style="width:55%;"/>

<br>
<br>

Loopeamos por ellos e imprimimos en pantalla los mejores cinco:

<br>

<img src="https://github.com/CharlyKill7/Salary-Machine-Learning/blob/main/img/top_mod.png" style="width:60%;"/>

<br>
<br>
	
Para mostrar, finalmente, el RMSE de cada uno de ellos:

<br>

<img src="https://github.com/CharlyKill7/Salary-Machine-Learning/blob/main/img/rmse.png" style="width:60%;"/>

<br>

Como se puede observar, el mejor modelo resultó ser el ExtraTreesRegressor, aunque XGBRegressor imprimió un RMSE menor. Sin embargo, su score era más bajo, así que opté por utilizar ambos y lanzar la predicción en Kaggle, obteniendo un mejor RMSE en el testeo oficial, pasando de 47k a 39k. 

<br>
<br>		
<a name="conclusion"/>

## Conclusiones

Todo lo expuesto anteriormente es la síntesis de un proceso más largo y farragoso. En el repo pueden encontrarse un par de notebooks más dondé probé muchas combinaciones de encodings, transformaciones y modelos. Aunque son demasiadas para exponerlas aquí, sí me gustaría comentar una constatación bastante significativa que descubrí durante el proceso:

<strong>Las mejores puntuaciones las obtuve cuando eliminé todas las columnas menos 'experience_level', 'job_title' y 'employee_residence'.</strong>
	
Esto invita a pensar que más datos a veces meten más ruido que explicación en los modelos de Machine Learning. Por eso, la principal conclusión que extraigo de este proyecto es que para hacer Machine Learning lo ideal es ir de lo simple a lo complejo, pasando por un millón de pruebas, cada una con su error.	



<img src="https://github.com/CharlyKill7/LUNA/blob/main/img/luna.png" style="width:45%;"/>
