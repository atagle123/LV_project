import bcchapi
import numpy as np
import matplotlib.pyplot as plt
import json 
import os
import seaborn as sns

json_series_file ="series.json" # donde estan las series
json_plot_file ="plotting.json" # donde estan los plot de las series

##### Funciones para leer archivos json #####

def read_json(file):
    with open(file,encoding="utf8") as f: # VER LOS ENCODINGS DE LOS ARCHIVOS  Latin-1, UTF-8
        data = json.load(f)
    return data

def get_json(file):
    data=read_json(file)
    return data


##### Get data #####

class Data:
    '''
        Function to get one dataframe of data from bccentral API
    '''
    def __init__(self,data_dir):
        self.siete = bcchapi.Siete(file="credentials.txt") # tiene que ser string # file="credenciales.txt" hacer mas seguro el logging con variables de ambiente
        self.data_directory=data_dir
        if not os.path.exists( self.data_directory):
              os.makedirs( self.data_directory)

    def get_data(self):
        args=get_json(json_series_file)
        self.data=self.siete.cuadro(**args)
        return(self.data)

    def download_data(self,format="csv",filename=""):
        if format=="excel":
            self.data.to_csv(os.path.join(self.data_directory, filename))
        else:
            self.data.to_csv(os.path.join(self.data_directory, filename))
        print("Data downloaded")
