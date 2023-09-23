from openpyxl import Workbook
from openpyxl.styles.borders import Border, Side
from openpyxl import Workbook

thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))

def write_attribution(excel_workbook, attribution : list[int]):
    output_sheet = excel_workbook.create_sheet("Output")
    
    output_sheet['A1'] = 'Atribuição de técnicos a projetos'
    output_sheet['A2'] = 'Tarefas'
    output_sheet['A3'] = 'Técnicos atribuídos'
    print("Attri")
    print(type(attribution))
    print(attribution)
    for task in range(len(attribution)):
        output_sheet.cell(row=2, column=task+2).value = task
        output_sheet.cell(row=3, column=task+2).value = attribution[task][0]
        output_sheet.cell(row=2, column=task+2).border = thin_border
        output_sheet.cell(row=3, column=task+2).border = thin_border


# The output to be written is a list of ints, saying what technician do what job.
def write_output(output : list[int], excel_path : str):
 
    print("Starting writing output")
    output_excel = Workbook()
    
    write_attribution(excel_workbook=output_excel, attribution=output)

    # Delete default sheet
    std=output_excel.get_sheet_by_name('Sheet')
    output_excel.remove_sheet(std)
    
    output_excel.save(excel_path)
