from utils import read_json







def get_rut(industry_name,folderpath="industry/empresas.json"):
    """
    Get RUT from the json file in the given path by industry name

    Args:
        industry_name (str): industry name
        folderpath (str): path to the json file
    
    Returns:
        str: RUT
    
    """
    json_data=read_json(folderpath)
    rut=json_data[industry_name]
    return(rut)


def build_website_link_from_industry(industry_name):
        """ Build specific website link from industry name to the scrapper to work

        Args:
            industry_name (str): industry name

        Returns:
            list: website links

        """
        default_folder_path="industry/empresas.json"
        rut=get_rut(industry_name,folderpath=default_folder_path)
        print(f"RUT:{rut}")
        
        Empresa = [f'https://www.cmfchile.cl/portal/principal/613/w3-search.php?keywords={industry_name}#fiscalizados',f"//td[text()={rut}]","./following-sibling::td/a"] # esto puede estar sujeto a cambios de la CMF
        return(Empresa)

