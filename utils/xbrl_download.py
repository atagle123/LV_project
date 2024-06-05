import requests
import os
import zipfile

def get_data_xbrl_to_path(url,path,filename):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
   
    response = requests.get(url,headers=headers)
    response.raise_for_status()

    os.makedirs(path, exist_ok=True)

    file_path=os.path.join(path,f"{filename}.zip")


    with open(file_path, 'wb') as f:
        f.write(response.content)


def unzip_xbrl_file(path,filename):

    os.makedirs(path, exist_ok=True)

    file_path=os.path.join(path,filename)

    with zipfile.ZipFile(f'{file_path}.zip', 'r') as zip_ref:
        zip_ref.extractall(file_path)


def find_xbrl_path(path,filename):

    directorio=os.path.join(path,filename)

    for ruta_directorio, _, archivos in os.walk(directorio):
        for archivo in archivos:
            if archivo.endswith('.xbrl'):
                # Imprimir el path completo del archivo
                path_completo = os.path.join(ruta_directorio, archivo)
                print("Path completo del archivo XBRL:", path_completo)
    
    return(os.path.join(os.getcwd(),path_completo))
