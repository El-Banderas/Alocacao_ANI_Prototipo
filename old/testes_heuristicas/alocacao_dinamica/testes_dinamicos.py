from configExcel import *
import pandas as pd
import openpyxl 
from CarolUpdateRemainingCost import carolina_heuristicaURC
from Gui_heuristica import gui_heuristica
import itertools
import statistics 

######################################### READ EXCEL ################################################
# load excel with its path 
wrkbk = openpyxl.load_workbook("ZéPaulo.xlsx", data_only=True) 

sh_projs = wrkbk["Output AS-IS"] 

projetos_organizados_por_meses = {}

# ID -> Cost anal
costs_anal = {}
# ID -> Cost accomp
costs_accomp = {}

# Key -> Proj id , value -> tecn_anal
projetos_alocacoes = {}

# iterate through excel and display data 
for row in sh_projs.iter_rows(min_row=2): 
    month_anal = row[pos_init_date].value.strftime("%m/%d/%Y")
    month_accomp = row[pos_accomp_date].value.strftime("%m/%d/%Y")
    # Matrix row in costs starts in 0, index in this sheet begins in 1
    row_proj = row[pos_id].value 
    costs_anal[row_proj] = row[pos_cost_an].value
    costs_accomp[row_proj] = row[pos_cost_accomp].value
    if month_anal in projetos_organizados_por_meses:
        projetos_organizados_por_meses[month_anal].append(f"A{row_proj}")
    else:
        projetos_organizados_por_meses[month_anal] = [f"A{row_proj}"]
    if month_accomp in projetos_organizados_por_meses:
        projetos_organizados_por_meses[month_accomp].append(f"B{row_proj}")
    else:
        projetos_organizados_por_meses[month_accomp] = [f"B{row_proj}"]
    
matrix_aptitude = []



print("Meses")
print(projetos_organizados_por_meses)
print(costs_anal)
print(costs_accomp)
exit(0)
sh_matrix = wrkbk["Matriz Total"] 
print("\n\n\nMatriz total")
matrix_aptitude = []
for row in sh_matrix.iter_rows(min_row=3, min_col=2): 
    if row[0].value != None:
        this_row = []
        for tecn in range(1,6):
            this_value = row[tecn].value
            this_row.append(this_value)        
        matrix_aptitude.append(this_row)

months_init_projs = list(projetos_organizados_por_meses.keys())
months_init_projs.sort()

######################################### HEURISTIC STUFF ################################################

num_techs = len(matrix_aptitude[0])
previous_costs_carol = [0] * num_techs
previous_costs_gui = [0] * num_techs

# Join current costs to the previous ones
def add_current_to_previous_costs(alocation : list[int],this_matrix_costs : list[list[int]], previous_costs : list[int] ):
    for proj, tech in enumerate(alocation):
        previous_costs[tech] += this_matrix_costs[proj][tech]
        print(f"Add {tech}: {this_matrix_costs[proj][tech]}")
    print(previous_costs)
    return previous_costs

def invert_mtx(mtx : list[list[int]]):
    inv_mtx = []
    for line in mtx:
        new_line = []
        for cell in line:
            new_value = 1 / cell
            new_line.append(new_value)
        inv_mtx.append(new_line)
    return inv_mtx

n_months = 0
# Check all projects by month
for month in months_init_projs:
    n_months = n_months + 1
    
    print("Alocation month: ", month)
    # Get projects this month
    projs_rows_begin_this_month = projetos_organizados_por_meses[month]
    this_matrix = []
    # Construct matrix of aptitudes between projects of this month and techs
    for proj in projs_rows_begin_this_month:
        this_matrix.append(matrix_aptitude[proj])
    num_projs = len(this_matrix)
    this_matrix_pd = pd.DataFrame(this_matrix)
    # Do the alocations for two heuristics
    alocation = carolina_heuristicaURC(df_aptitude_between_task_machine=this_matrix_pd, num_tasks=num_projs, machine_quantity=num_techs, previous_costs=previous_costs_carol)
    print("Carolina")
    previous_costs_carol = add_current_to_previous_costs(alocation=alocation, this_matrix_costs=this_matrix, previous_costs=previous_costs_carol)
    # In case the matrix should be inverted (if heuristic interprets the matrix other way). But it's commented
    # this_matrix_pd = pd.DataFrame(invert_mtx(this_matrix))
    alocation = gui_heuristica(df_task_time_per_machine=this_matrix_pd, load_per_machine=previous_costs_gui, num_tasks=num_projs, machine_quantity=num_techs)
    # To join list of lists
    alocation_clean = list(itertools.chain.from_iterable(alocation))
    print("GUI")
    previous_costs_gui = add_current_to_previous_costs(alocation=alocation_clean, this_matrix_costs=this_matrix, previous_costs=previous_costs_gui)

def print_stuff(total_costs : list[int]):
    print(total_costs)
    print("STD: ",statistics.pstdev(total_costs) )
    print("Amp: ",max(total_costs) - min(total_costs) )

print("Carol")
print_stuff(total_costs=previous_costs_carol)
print("Gui")
print_stuff(total_costs=previous_costs_gui)

print("Num months: ", n_months)