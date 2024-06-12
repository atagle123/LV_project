from tabula import read_pdf


"""
scraps and download analisis razonados y estados financieros en pdf
parse pdfs into tables, 
clean and preprocess tables 
function to get specific tables (quizas hacer esto antes)
return data and download to excel, csv, etc

eventually compare data with the xbrl source

"""



class PDF_tables:
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
df_temp = read_pdf('Análisis_Razonado92434000_202212 (1).pdf',pages='all')