from input.read_excel import read_excel
from input.read_names import read_names
import json

# Paths are relative to main file
path_configuration_excel = 'configuration/excel.json'
path_excel_names = './input/Nomes.xlsx'

'''
In this class we get all the information, from excel and maybe OutSystems.
'''
class Input:
  def __init__(self):
    self.excel_information = None
    self.names_translations = {}

def read_json(path_file : str):
    f = open(path_file)
    
    data = json.load(f)
    
    f.close()

    return data

def read_input(path_excel : str):
    excel_configuration = read_json(path_file=path_configuration_excel)
    input = Input()
    input.excel_information = read_excel(path_excel_input=path_excel, configuration=excel_configuration)
    (tecns_translation, proj_translations) = read_names(path_excel_input=path_excel_names)
    input.names_translations["tecns"] = tecns_translation
    input.names_translations["projs"] = proj_translations
    return input