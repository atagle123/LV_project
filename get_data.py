import bcchapi
import os
from utils.json_utils import get_json

##### Get data #####

class Data:
    '''
        Class to get data from bccentral API
    '''
    def __init__(self,data_dir="data"):
        self.siete = bcchapi.Siete(file="credentials.txt") # tiene que ser string # file="credenciales.txt" hacer mas seguro el logging con variables de ambiente
        self.data_directory=data_dir
        if not os.path.exists( self.data_directory):
              os.makedirs( self.data_directory)

    def get_data_from_json(self,json_file="serie.json"):
        """
        Function to to get the parameters from the json file and make request to the API
        
        """
        args=get_json(json_file)
        self.name=args["nombres"]   # que pasa si no pongo nombres?? quizas buscarlos
        self.data=self.siete.cuadro(**args)
        return(self.data)
    
    def get_data_from_args(self,args):
        """
        Function to to get the data from a dict of args

        """
        self.name=args["nombres"]   # que pasa si no pongo nombres?? quizas buscarlos
        self.data=self.siete.cuadro(**args)
        return(self.data)



    def download_data(self,format="csv",filename=None):
        """
        Function to download the data to csv or excel
        """
        if filename is None:
            filename=str(self.name)
        if format=="excel":
            self.data.to_excel(os.path.join(self.data_directory, f"{filename}.xlsx"))
        else:
            self.data.to_csv(os.path.join(self.data_directory, f"{filename}.csv"))
        print("Data downloaded")

    
    def search_data(self, search_string):
        """
        Function to search the data
        """
        return(self.siete.buscar(search_string))

    #def create_filename(self):