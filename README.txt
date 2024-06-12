cosas por hacer:



- ver tema de cuales columnas sirven para que concepto y tmb que fechas utilizar...:
iteracion sobre empresas - fechas - conceptos
ver para eventualmente juntar excels o dataframes por conceptos y años ... 

cosas que faltan importantes:
- revisar unnamed cols en dataframe ver para saber cuales son los conceptos para hacer el parsing
- ver el tema de seleccionar las fechas y los conceptos 
- cambiar prints por logger
- falta ver formato d enumeros en excel
- falta ver distintos campos utiles para cada codigo, eventualmente va a haber que hacer un multi index column quizas


ideas:
quizas hacer una clase que vaya buscando e iterando sobre todos los conceptos y descargando los archivos correspondientes
dos opciones:

-armar a mano las fallas
-extraer datos de pdf
-ir armando iterativamente las cosas... puede ser buena opcion para q funcione (quizas en la cmf lo hacen asi)
- notar que falabella las columnas esan bien (aunq no dicen la fecha q corresponden) pero besalco no, es probable qu idea descrita anteriormente tenga sentido y que el reporte sea solo
para ese trimestre en particular, entonces habria que ir sumando los otros trimestres para ir obteniendo los mismos resultados.

para el quarter 12 son las eerr de todo el año, pero se se selecciona un trimestre son las de ese treimestre, habria que sumar, ver si es necesario tenerlo para cada quarter.

problema error en los datos ? porque ocurre

posible problema: cambiar nombre a archivono solo por concepto, si no tmb por las columnas
posible problema 2: si queremos a prtiori cualquier info, va a haber que hacer un multi columns names

problema 3 distintas compañias reportan diferentes valores en el xbrl dependiendo el nombre

- IR SUMANDO ITERATIVAMENTE A LO LARGO DEL AÑO PARA VER SI S EOBTIENEN LOS MISMOS RESULTADOS DE LA CMF, los quarter son los resultados parciales, pero cuando se selecciona el 12 es el total del año

ideas:
usar html parser o pdf parser para obtener los resultados
usar el html parser para la info importante... si no ir al pdf, y si no ir al xbrl... 

ojo: es porbable que xbrl sea solo consistente con utilizar 12 como mes osea final de año.