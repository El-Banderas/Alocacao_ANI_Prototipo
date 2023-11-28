import random
import numpy as np
import sys
import pandas as pd
import statistics
from Carolina_Unrelated import carolina_heuristica
from CarolUpdateRemainingCost import carolina_heuristicaURC

df_aptitude_between_task_machine_matrix = [ 
[7,20,12,3,	11,	16],
[10,8,6,22,8,20],
[10,17,3,15,	5,	18],
[13,6,20,20,	16,	10],
[6,14,17,5,	16,	9],
[16,10,16,21,10,13],
[12,5,14,2,3,4],
[11,7,16,20,19,	13],
[20,14,	4,12,2,11],
[14,13,14,22,5,21]
    ]

for i in range(len(df_aptitude_between_task_machine_matrix)):
    for ii in range(len(df_aptitude_between_task_machine_matrix[0])):
        df_aptitude_between_task_machine_matrix[i][ii] = 1/df_aptitude_between_task_machine_matrix[i][ii]

def costs_per_machine(solution : list[int], df_expected_time, df_aptitude):
    costs_per_machine = [0] * machine_quantity
    for current_task in range(len(solution)):
        task_length = df_expected_time.loc[current_task]
        this_machine = solution[current_task]
        this_aptitude = df_aptitude.iat[current_task, this_machine ]
        costs_per_machine[this_machine] = costs_per_machine[this_machine] + (task_length / this_aptitude  )
    return costs_per_machine
 
num_tasks = len(df_aptitude_between_task_machine_matrix)
num_techs = len(df_aptitude_between_task_machine_matrix[0])
df_aptitude_between_task_machine = pd.DataFrame(df_aptitude_between_task_machine_matrix)
lenghts = df = pd.DataFrame([1 for _ in range(num_tasks)])
previous_costs = df = [0] * num_techs
#alocation = carolina_heuristica(df_aptitudes=df_aptitude_between_task_machine, df_task_time=lenghts, num_tasks=num_tasks, machine_quantity=num_techs, previous_costs=previous_costs)
alocation = carolina_heuristicaURC(df_aptitudes=df_aptitude_between_task_machine, df_task_time=lenghts, num_tasks=num_tasks, machine_quantity=num_techs, previous_costs=previous_costs)
print("Alocation")
print(alocation)
defined_alocation = [4,3,3,6,4,2,5,1,5,5]
defined_alocation_clean = list(map(lambda x: x-1, defined_alocation))
print(list(map(lambda x : x, defined_alocation)))
assert(defined_alocation_clean == alocation)

machine_quantity = num_techs

custosPorMaq = costs_per_machine(solution=alocation, df_expected_time=lenghts, df_aptitude=df_aptitude_between_task_machine)
custosPorMaq = list(map(lambda x : x.values[0], custosPorMaq))
print("Custos maq: ", custosPorMaq)
assert(custosPorMaq == [11,	10,	9,	8,	10,	10])

############  2º part ######################

df_aptitude_between_task_machine_matrix2 = [ 
[6,	14,	17,	5,	16,	9],
[7,	20,	12,	3,	11,16],
[12,	5,	14,	2,	3,	4]
]
for i in range(len(df_aptitude_between_task_machine_matrix2)):
    for ii in range(len(df_aptitude_between_task_machine_matrix2[0])):
        df_aptitude_between_task_machine_matrix2[i][ii] = 1/df_aptitude_between_task_machine_matrix2[i][ii]

num_tasks = len(df_aptitude_between_task_machine_matrix2)
df_aptitude_between_task_machine2 = pd.DataFrame(df_aptitude_between_task_machine_matrix2)
lenghts = df = pd.DataFrame([1 for _ in range(num_tasks)])
alocation = carolina_heuristica(df_aptitudes=df_aptitude_between_task_machine2, df_task_time=lenghts, num_tasks=num_tasks, machine_quantity=num_techs, previous_costs=custosPorMaq)
print("Alocation")
print(alocation)