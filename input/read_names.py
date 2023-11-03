
from openpyxl import load_workbook

def read_translation(sheetname : str, workbook):
    res_list : list(str) = []
    tecs_names = workbook.get_sheet_by_name(sheetname)
    for row in tecs_names.iter_rows():
        tecn_id = row[0].value
        tecn_name = row[1].value
        try:
            res_list.insert(int(tecn_id), tecn_name)
        except:
            pass
    return res_list

def read_names(path_excel_input : str):
    excelFile = load_workbook(filename = path_excel_input, data_only=True)
    translation_tecns = read_translation(sheetname="Técnicos", workbook=excelFile)
    translation_projs = read_translation(sheetname="Projetos", workbook=excelFile)
    return (translation_tecns, translation_projs)
