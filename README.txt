cosas por hacer:



- modularizar scrapping y hacer variable a año, empresa quarter, etc... con el fin de iterar sobre todo 
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

problema error en los datos ? porque ocurre

posible problema: cambiar nombre a archivono solo por concepto, si no tmb por las columnas
posible problema 2: si queremos a prtiori cualquier info, va a haber que hacer un multi columns names
