from tabula import read_pdf
import os
import pandas as pd

"""
scraps and download analisis razonados y estados financieros en pdf
parse pdfs into tables, 
clean and preprocess tables 
function to get specific tables (quizas hacer esto antes)
return data and download to excel, csv, etc

eventually compare data with the xbrl source

"""
class BasePDFclass:
    def __init__(self,pdf_path):
        self.pdf_path = pdf_path
    
    def extract_tables(self):
        """ Método a implementar que entregue todas las tablas en formato de una ista de dataframes
        """
        raise NotImplementedError

class Image_PDF_extractor():
    def __init__(self):
        pass

    def exctract_tables(self):
        pass



class Text_PDF_extractor():
    def __init__(self):
        pass
    def extract_tables(self,pdf_path,pages="all"):
        df = read_pdf(pdf_path,pages=pages)
        return(df)


from tabula import read_pdf
import pandas as pd
import os

class BasePDFclass:
    def __init__(self,pdf_path):
        self.pdf_path = pdf_path
    
    def extract_tables(self):
        """ Método a implementar que entregue todas las tablas en formato de una ista de dataframes
        """
        raise NotImplementedError

class Image_PDF_extractor():
    def __init__(self):
        pass

    def exctract_tables(self):
        pass



class Text_PDF_extractor():
    def __init__(self):
        pass
    def extract_tables(self,pdf_path,pages="all"):
        df = read_pdf(pdf_path,pages=pages)
        return(df)


class PDF_tables(BasePDFclass):
    """Class that exctract all the tables of the pdf"""
    
    def __init__(self, pdf_path):
        super().__init__(pdf_path)
        self.text_extractor=Text_PDF_extractor()
        self.image_exctractor=Image_PDF_extractor()

        current_dir = os.getcwd()
        self.csv_path=os.path.join(current_dir, "data","industrydata","pdf","csv")
        self.excel_path=os.path.join(current_dir, "data", "industrydata", "pdf", "excel")

        os.makedirs(self.excel_path, exist_ok=True)
        os.makedirs(self.csv_path, exist_ok=True)



    def extract_tables(self,pages="all"):
        #df_images=self.image_exctractor.extract_tables(pages=pages)
        df_text=self.text_extractor.extract_tables(self.pdf_path,pages=pages)
        #hacer un merge de las dos listas...
        # ojo que en el merge es probable que se repitan las dos tablas
        self.df_list=df_text
        print(f"Extracted {len(self.df_list)} tables")

    def search_concept(self,concept=None): # quizas hacer uno de si es el titulo o no...
        """ Search for a concept in the dataframes, if given, returns a list of dataframes with the given concept
            quizas pasar todo a minuscula...  o a regex
        """ 
        if concept==None:
            return(self.df_list)
        
        match_list=[]
        for df in self.df_list:

            df_lower = df.map(lambda x: x.lower() if isinstance(x, str) else x) # uses lower case to match

            is_string_present = df_lower.isin([concept]).any().any()
            if is_string_present:
                match_list.append(df)
        return(match_list)
    
    def preprocess_data(self,df_list,function=None):
        "quizas implementar funciones propias por empresa..."

        for i,df in enumerate(df_list):

            df = df.apply(lambda x: x.astype(str).str.replace('.', ''))
            df = df.apply(lambda x: x.astype(str).str.replace('(', ''))
            df = df.apply(lambda x: x.astype(str).str.replace(')', ''))
            df.dropna(how="all",inplace=True)
            df = df.map(lambda x: x.lower() if isinstance(x, str) else x)
            df_list[i]=df

        return(df_list)
    
    def tables_to_excel(self,filename,concept=None):
        
        match_list=self.search_concept(concept=concept)
        df_preprocess_list=self.preprocess_data(match_list)

        filepath=os.path.join(self.excel_path, f"{filename}.xlsx")

        with pd.ExcelWriter(filepath) as writer:
            for  i,df in enumerate(df_preprocess_list):
                df.to_excel(writer,sheet_name=f"sheetname_{i}")
        pass
    
    def download_table(self,path,table_name): # ver como seleccionar una tabla para descargar... 
        raise NotImplementedError



    #class  clase para busca los links y descargar los analisis razonados o los pdf ... 


if __name__=="__main__":
    pdf_path="C:/Users/ataglem/Desktop/LV_project/Análisis_Razonado92434000_202212.pdf"
    pdf_tables_instance=PDF_tables(pdf_path)
    pdf_tables_instance.extract_tables()
    #df=pdf_tables_instance.search_concept("activos corrientes")
    pdf_tables_instance.tables_to_excel(filename="besalco_razonados")
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import numpy as np
    from industry.scrapping import Cmf_scrapper
    cmf=Cmf_scrapper
