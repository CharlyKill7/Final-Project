# LUNA: Asistente Virtual por voz

<img src="https://github.com/CharlyKill7/LUNA/blob/main/img/luna.png" style="width:60%;"/>

## Índice

1. [Descripción](#descripción)
2. [Archivos](#archivos)
3. [Ejecución](#encoding)
4. [Modelos](#modelos)
5. [Conclusiones](#conclusion)


<a name="descripción"/>

## Descripción del proyecto

Este proyecto es una competición de Kaggle, donde habrá que utilizar Machine Learning para predecir el salario dentro del sector Data, a partir de unos .csv que contienen datos como el puesto, el país de residencia o el tipo de contrato, entre otros. 

### Restricciones:
- No está permitido eliminar filas en los datos de testeo o prueba.

### Dataset:
- <em>salaries_data.csv</em>: contiene el conjunto de datos de entrenamiento.
- <em>testeo.csv</em>: contiene el conjunto de datos de prueba.
- <em>muestra.csv</em>: ejemplo de formato de la predicción para su carga en Kaggle.

### Objetivo:
 
Nuestro objetivo será aplicar y mejorar modelos de Machine Learning, probando varias transformaciones, encodings, hiperparámetros y modelos, con el fin de obtener el menos RMSE que sea posible.

 
 <a name="transformacion"/>
 
## Tranformación

Logicamente, lo primero fue realizar un análisis exploratorio de los datos, comprobando los valores nulos, el tipo de objeto de cada columna, las dimensiones del Dataframe, etc. Este proceso se llevó a cabo en el notebook 'draft', aunque muchas de las pruebas fueron borradas sobre la marcha. También se unificó en una sola columna el salario, quedándonos con salary_in_usd y renombrándola.

Tras esto, tomamos la precaución de comprobar si había valores en los datos de prueba que no estuvieran en el entrenamiento. Descubrimos así tres columnas con valores distintos: employee_residence, company_location y job_title.

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
