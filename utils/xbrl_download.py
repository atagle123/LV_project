import requests
import os
import zipfile


def get_data_xbrl_to_dir(url,filename,dir="XBRL_files"):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
   
    response = requests.get(url,headers=headers)
    response.raise_for_status()

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(f'{dir}/{filename}.zip', 'wb') as f:  # hacer un os path join
        f.write(response.content)


def unzip_xbrl_file(file_path, dir="XBRL_files"):

    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(dir)


def find_xbrl_name():
    for ruta_directorio, _, archivos in os.walk(directorio):
        for archivo in archivos:
            if archivo.endswith('.xbrl'):
                # Imprimir el path completo del archivo
                path_completo = os.path.join(ruta_directorio, archivo)
                print("Path completo del archivo XBRL:", path_completo)
    return(path_completo)