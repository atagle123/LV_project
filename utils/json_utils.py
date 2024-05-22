import json





##### Funciones para leer archivos json #####

def read_json(file):
    with open(file,encoding="utf8") as f: # VER LOS ENCODINGS DE LOS ARCHIVOS  Latin-1, UTF-8
        data = json.load(f)
    return data

def get_json(file):
    data=read_json(file)
    return data