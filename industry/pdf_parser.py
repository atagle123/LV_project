from tabula import read_pdf


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


class PDF_tables(BasePDFclass):
    """Class that exctract all the tables of the pdf"""
    
    def __init__(self, pdf_path):
        super().__init__(pdf_path)
        self.text_extractor=Text_PDF_extractor()
        self.image_exctractor=Image_PDF_extractor()

    def extract_tables(self,pages="all"):
        #df_images=self.image_exctractor.extract_tables(pages=pages)
        df_text=self.text_extractor.extract_tables(self.pdf_path,pages=pages)
        print(df_text)
        #hacer un merge de las dos listas...
        # ojo que en el merge es probable que se repitan las dos tablas
        self.df_list=df_text
        print(f"Extracted {len(self.df_list)} tables")

    def search_concept(self,concept): # quizas hacer uno de si es el titulo o no...
        """ Search for a concept in the dataframes, if given, returns a list of dataframes with the given concept
            quizas pasar todo a minuscula...  o a regex
        """ 
        match_list=[]
        for df in self.df_list:
            is_string_present = df.isin([concept]).any().any()
            if is_string_present:
                match_list.append(df)
        return(match_list)
    
    # quzias hacer un string match-> column or row match-> df_list_match -> match list of concepts to a dataframe, its usefull to define q good way to exctrat the desired table

    def preprocess_data(self,function): "quizas implementar funciones propias por empresa..."
    
    def download_table(self,path,table_name): # ver como seleccionar una tabla para descargar... 
        raise NotImplementedError




if __name__=="__main__":
    pdf_path="C:/Users/ataglem/Desktop/LV_project/Análisis_Razonado92434000_202212.pdf"
    pdf_tables_instance=PDF_tables(pdf_path)
    pdf_tables_instance.extract_tables()
    df=pdf_tables_instance.search_concept("Activos Corrientes")
    #print("df",df)
    print("tables concept",len(df))
    for i in df:
        pass
       # print(i)