from input.read_excel import read_excel
import json

# Paths are relative to main file
path_input_excel = './input/input.xlsx'
path_configuration_excel = 'configuration/excel.json'

class Input:
  def __init__(self, num_tecnicos, num_projetos):
    self.num_tecnicos = num_tecnicos
    self.num_projetos = num_projetos
'''
p1 = Person("John", 36)

print(p1.name)
print(p1.age) 
'''
def read_json(path_file : str):
    f = open(path_file)
    
    data = json.load(f)
    
    f.close()

    return data

def read_input():
    excel_configuration = read_json(path_file=path_configuration_excel)
    read_excel(path_excel_input=path_input_excel, configuration=excel_configuration)
    return