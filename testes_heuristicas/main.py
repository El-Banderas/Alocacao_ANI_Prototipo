import pandas as pd
import numpy as np

from Gui_heuristica import gui_heuristica
from Carolina_Unrelated import carolina_heuristica

# Tests variables
num_interations = 1

# Input variables
min_task_length = 300
max_task_length = 700
num_tasks = 25
machine_quantity = 5

def generate_input():

    # Define the number tasks
    # Create a DataFrame with random values of task length
    expected_task_time = np.random.uniform(
        min_task_length, max_task_length, size=(num_tasks, 1)
    )
    df_expected_task_time = pd.DataFrame(expected_task_time)
    
    # Create aptitude matrix.
    max_aptitude = 1.2
    min_aptitude = 0.7

    aptitude_between_task_machine = np.random.uniform(
        min_aptitude, max_aptitude, size=(num_tasks, machine_quantity)
    )
    df_aptitude_between_task_machine = pd.DataFrame(aptitude_between_task_machine)

    return (df_expected_task_time, df_aptitude_between_task_machine)

def carol_input():
    df_expected_task_time = [10 for i in range(0, num_tasks)]
    df_aptitude_between_task_machine = [ [7,20	,12,3,	11,	16],
                                    [10,8,6	,22,8,20],
[10,17,	3,	15,	5,	18],
[13,	6	,20,	20,	16,	10],
[6,14	,17,	5,	16,	9],
[16,10,16,21,10,13],
[12,5,14,2,3,4],
[11,7,16,20,19,	13],
[20,14,	4,12,2,11],
[14,13,14,22,5,21]
    ]
    return (pd.DataFrame(df_expected_task_time), pd.DataFrame(df_aptitude_between_task_machine))
    
def main():
    results = {"Gui" : [], "Carolina" : []}
    for interation in range(num_interations):
        #(df_task_time, df_aptitudes) = generate_input()
        (df_task_time, df_aptitudes) = carol_input()
        std_carol = carolina_heuristica(df_expected_task_time=df_task_time, df_aptitude_between_task_machine=df_aptitudes, num_tasks=10, machine_quantity=6)
        results["Carolina"].append(std_carol)
        #std_gui = gui_heuristica(df_expected_task_time=df_task_time, df_aptitude_between_task_machine=df_aptitudes, num_tasks=10, machine_quantity=6)
        #print(std_gui)
        #results["Gui"].append(std_gui)
    print("Results")
    print(results)

main()
'''
(t1, t2) = generate_input()
print("Tamanhos 1")
print(t1.size)
print(t2.size)

(t1, t2) = carol_input()
print("Tamanhos 2")
print(t1.size)
print(t2.size)
'''