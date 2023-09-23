from input.read_excel import read_excel
import json

# Paths are relative to main file
path_configuration_excel = 'configuration/excel.json'

'''
In this class we get all the information, from excel and maybe OutSystems.
'''
class Input:
  def __init__(self):
    self.excel_information = None

def read_json(path_file : str):
    f = open(path_file)
    
    data = json.load(f)
    
    f.close()

    return data

def read_input(path_excel : str):
    excel_configuration = read_json(path_file=path_configuration_excel)
    input = Input()
    input.excel_information = read_excel(path_excel_input=path_excel, configuration=excel_configuration)
    return input