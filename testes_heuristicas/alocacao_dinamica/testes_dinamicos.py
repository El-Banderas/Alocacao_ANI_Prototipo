from configExcel import *
import openpyxl 

# load excel with its path 
wrkbk = openpyxl.load_workbook("excel_vitor.xlsx", data_only=True) 

sh = wrkbk["Candidaturas"] 

projetos_organizados_por_meses = {}

def create_job(row):
    pass

# iterate through excel and display data 
for row in sh.iter_rows(min_row=3, min_col=1): 
    print("Row")
    month_this_line = row[pos_mes].value
    month_this_line = row[pos_id].value
    print( row[pos_id].value,  " - ", row[pos_mes].value)
    if month_this_line in projetos_organizados_por_meses:
        projetos_organizados_por_meses[month_this_line].append(pos_id)
    else:
        projetos_organizados_por_meses[month_this_line] = [pos_id]


	#for cell in row: 
	#	print(cell.value, end=" ") 
	#print() 
