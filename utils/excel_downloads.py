import requests
import os

def download_excel_file(url,path,filename="excel_file"):
    """ Download an Excel file from a given URL with a given name.

    Args:
        url (str): The URL of the Excel file to download
        path (str): Path to download the excel
        name (str): The name to give the downloaded file
    """
    response = requests.get(url)
    response.raise_for_status()

    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, f"{filename}.xlsx")
    
    with open(filepath, 'wb') as f:
        f.write(response.content)
    pass



