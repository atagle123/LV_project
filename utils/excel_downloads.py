import requests
import os

def download_excel_file(url,name="excel_file"):
    """ Download an Excel file from a given URL with a given name.

    Args:
        url (str): The URL of the Excel file to download
        name (str): The name to give the downloaded file
    """
    response = requests.get(url)
    response.raise_for_status()

    if not os.path.exists("download_excels"):
        os.makedirs("download_excels")
    
    with open(f'download_excels/{name}.xlsx', 'wb') as f:
        f.write(response.content)
    pass



