## Filtrador de Contratos de Empréstito (PySECOP)

El programa, hecho en Python, se conecta a dos bases de datos (SECOP I y II) proveídas por Datos Abiertos y aplica una serie de peticiones (requests) en SoQL (Socrata Query Language) para obtener contratos de empréstito según la delimitación territorial por departamentos (ver archivo departamentos.txt) y por intervalo de tiempo.

## Dependencias externas

Aparte de usar librerías nativas de Python, también se emplea la siguiente lista de librerías externas:

* Pandas
* Tkcalendar

Adicionalmente, para el empaquetado del programa se empleó la libreria PyInstaller.

## Empaquetado del Programa

Para crear un ejecutable a partir del archivo Python empleando PyInstaller se deben seguir las siguientes instrucciones:

* En la misma carpeta donde se encuentra PySECOP.py, abrir un terminal.
* Escribir en el terminal lo siguiente pyinstaller --onefile --windowed --hidden-import babel.numbers PySECOP.py
* Tras esperar al proceso de empaquetado se crearán dos carpetas: dist (donde se encuentra el ejecutable) y build.
* El archivo ejecutable puede moverse a cualquier lugar, siempre que se encuentre junto al archivo de departamentos.txt.
* Tras lo anterior ya se puede usar el programa.

## Uso de departamentos.txt

El archivo “departamentos.txt” contiene la lista de departamentos en los que el programa debe consultar la lista de contratos de empréstito, tanto en SECOP I y II. 

El archivo la lista de departamentos se escribe de una forma específica, siguiendo una serie de reglas: 

    Los nombres de los departamentos siempre deben escribirse en mayúsculas. 

    No se permiten caracteres especiales (tildes, la ñ, etc.) sino que deben ser reemplazados por un guion bajo, Ej: Atlántico -> ATL_NTICO. 

    Solo puede escribirse una sola palabra, por ejemplo, si se desea buscar contratos de empréstito en el departamento del Norte de Santander en la lista solo puede escribirse “NORTE” y no “NORTE DE SANTANDER” o en el caso de San Andrés, Providencia y Santa Catalina escoger una palabra distintiva del nombre que no se comparta con otro departamento, como PROVIDENCIA O CATALINA. 
