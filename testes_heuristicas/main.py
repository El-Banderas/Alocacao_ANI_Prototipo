import pandas as pd
import numpy as np
from statistics import mean 

from Gui_heuristica import gui_heuristica
from Carolina_Unrelated import carolina_heuristica
from Renan import Renan_heuristic

# Tests variables
num_interations = 10

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

def calculate_std(solution : list[int], df_expected_time, df_aptitude):
    costs_per_machine = [0] * machine_quantity
    for current_task in range(len(solution)):
        task_length = df_expected_time.loc[current_task]
        this_machine = solution[current_task]
        this_aptitude = df_aptitude.iat[current_task, this_machine ]
        costs_per_machine[this_machine] = costs_per_machine[this_machine] + (task_length / this_aptitude  )

    return np.std(costs_per_machine)
  
def zip_list_of_lists(solution : list[int]):
    return [element for nestedlist in solution for element in nestedlist]

def main():
    results = {"Gui" : [], "Carolina" : [], "Renan" : []}
    for interation in range(num_interations):
        (df_task_time, df_aptitudes) = generate_input()
        #(df_task_time, df_aptitudes) = carol_input()
        solution_Carol = carolina_heuristica(df_task_time=df_task_time, df_aptitudes=df_aptitudes, num_tasks=num_tasks, machine_quantity=machine_quantity)
        results["Carolina"].append(calculate_std(solution=solution_Carol, df_expected_time=df_task_time, df_aptitude=df_aptitudes))

        solution_Gui = gui_heuristica(df_expected_task_time=df_task_time, df_aptitude_between_task_machine=df_aptitudes, num_tasks=num_tasks, machine_quantity=machine_quantity)
        solution_Gui = zip_list_of_lists(solution=solution_Gui)
        results["Gui"].append(calculate_std(solution=solution_Gui, df_expected_time=df_task_time, df_aptitude=df_aptitudes))

        solution_Renan = Renan_heuristic(df_expected_task_time=df_task_time, df_task_performance =df_aptitudes, num_tasks=num_tasks, machine_quantity=machine_quantity)
        results["Renan"].append(calculate_std(solution=solution_Renan, df_expected_time=df_task_time, df_aptitude=df_aptitudes))
        #print(std_gui)
        #results["Gui"].append(std_gui)
    print("Results")
    print(results)
    for x, y in results.items():
        if len(y) > 0:
            print(x , ": ", mean(y))


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