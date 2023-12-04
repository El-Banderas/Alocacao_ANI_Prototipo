
import xlwings as xw 

def convert_int_char(col : int):
    return chr(col+64)

def split_cell_position(cell_position : str):
    return cell_position.split("/")

def get_sheet_by_name(excel, sheetname : str):
    if sheetname in excel.sheet_names:
        return excel.sheets[sheetname]
    else:
        raise Exception(f"[READ EXCEL] Invalid excel, missing {sheetname} sheet")

def get_value_by_index(sheet, index_row : int, index_col :int): 
    letter_col = convert_int_char(col=index_col)
    #print(f"From {letter_col}{index_row} get: ",sheet.range(f"{letter_col}{index_row}").value )
    return sheet.range(f"{letter_col}{index_row}").value

def set_value_by_index(sheet, index_row : int, index_col :int, value): 
    letter_col = convert_int_char(col=index_col)
    sheet.range(f"{letter_col}{index_row}").value = value
    #print("Write value to sheet")

def convert_cell_name_to_indexs(cell_name : str):
    column_index_start = ord(cell_name[0].lower())-96 
    row_index_start = int(cell_name[1:]) 
    return (row_index_start, column_index_start)

def write_attribution(id_project : int, tecn_allocated : int, configuration : dict, sheet):
    cell_id_project = configuration["id"]
    (row_index_start, column_index_start) = convert_cell_name_to_indexs(cell_id_project) 
    # Get row of project to write allocation info
    while get_value_by_index(sheet=sheet, index_row=row_index_start, index_col=column_index_start) != id_project:
        row_index_start +=1
    (row_analise,col_analise ) = convert_cell_name_to_indexs(cell_name=configuration["analise"])
    row_analise=row_index_start
    if get_value_by_index(sheet=sheet, index_row=row_analise, index_col=col_analise) == None:
        set_value_by_index(sheet=sheet, index_row=row_analise, index_col=col_analise, value=tecn_allocated)
    else:
        (row_manager,col_manager ) = convert_cell_name_to_indexs(cell_name=configuration["gestor"])
        row_manager=row_index_start
        set_value_by_index(sheet=sheet, index_row=row_manager, index_col=col_manager, value=tecn_allocated)

# The output to be written is a list of ints, saying what technician do what job.
def write_output( excel_path : str, output : list[int],excel_input_info):
    excelFile = xw.Book(excel_path)
    sheet = get_sheet_by_name(excel=excelFile, sheetname=excel_input_info.configuration["write_allocation"]["sheetname"])
    for idx, proj_id in enumerate(excel_input_info.projects_handled):
        write_attribution(id_project=proj_id, tecn_allocated=output[idx],configuration=excel_input_info.configuration["write_allocation"], sheet=sheet) 

    print("BYE!")
    #ws = excelFile.sheets("Projetos") 
    #ws.range("A1").value = "geeks"
    excelFile.save()
    exit(0)
    # output_excel  = load_workbook(filename = excel_path)
    output_excel = Workbook()
    
    write_attribution(excel_workbook=output_excel, attribution=output)

    # Delete default sheet
    
    output_excel.save(excel_path)
