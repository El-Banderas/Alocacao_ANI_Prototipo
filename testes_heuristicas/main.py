import pandas as pd
import numpy as np
from statistics import mean 

from Gui_heuristica import gui_heuristica
from Carolina_Unrelated import carolina_heuristica
from Renan import Renan_heuristic
from Write_output import write_output
import functools

# Tests variables
num_interations = 30

# Input variables
min_task_length = 300
max_task_length = 700
machine_quantity = 5

def generate_input(num_tasks : int):

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

def calculate_that_column(costs_per_machine : dict):
    costs_clean = []
    for cost_one_machine in costs_per_machine:
        costs_clean.append(cost_one_machine.values[0])

    #costs_per_machine = list(map(lambda n : n.values[0], costs_per_machine))
    costs_per_machine = costs_clean
    max_cost = max(costs_per_machine)
    min_cost = min(costs_per_machine)
    return max_cost-min_cost
    

def calculate_std(solution : list[int], df_expected_time, df_aptitude):
    costs_per_machine = [0] * machine_quantity
    for current_task in range(len(solution)):
        task_length = df_expected_time.loc[current_task]
        this_machine = solution[current_task]
        this_aptitude = df_aptitude.iat[current_task, this_machine ]
        costs_per_machine[this_machine] = costs_per_machine[this_machine] + (task_length / this_aptitude  )
    amplitude = calculate_that_column(costs_per_machine=costs_per_machine)
    return (np.std(costs_per_machine), sum(costs_per_machine[0]), amplitude)
  
def zip_list_of_lists(solution : list[int]):
    return [element for nestedlist in solution for element in nestedlist]

def main_num_tasks(num_tasks):
    results_std = {"Gui" : [], "Carolina" : [], "Renan" : []}
    results_total_cost = {"Gui" : [], "Carolina" : [], "Renan" : []}
    results_differences = {"Gui" : [], "Carolina" : [], "Renan" : []}
    results_attributions = {"Gui" : [], "Carolina" : [], "Renan" : []}
    input = []
    for interation in range(num_interations):
        (df_task_time, df_aptitudes) = generate_input(num_tasks=num_tasks)
        pair = (df_task_time, df_aptitudes)
        input.append(pair)
        #(df_task_time, df_aptitudes) = carol_input()
        solution_Carol = carolina_heuristica(df_task_time=df_task_time, df_aptitudes=df_aptitudes, num_tasks=num_tasks, machine_quantity=machine_quantity)
        (std, total_cost , differences) = calculate_std(solution=solution_Carol, df_expected_time=df_task_time, df_aptitude=df_aptitudes)
        results_std["Carolina"].append(std)
        results_total_cost["Carolina"].append(total_cost)
        results_differences["Carolina"].append(differences)
        results_attributions["Carolina"].append(solution_Carol)

        solution_Gui = gui_heuristica(df_expected_task_time=df_task_time, df_aptitude_between_task_machine=df_aptitudes, num_tasks=num_tasks, machine_quantity=machine_quantity)
        solution_Gui = zip_list_of_lists(solution=solution_Gui)
        (std, total_cost, differences ) = calculate_std(solution=solution_Gui, df_expected_time=df_task_time, df_aptitude=df_aptitudes)
        results_std["Gui"].append(std)
        results_differences["Gui"].append(differences)
        results_total_cost["Gui"].append(total_cost)
        results_attributions["Gui"].append(solution_Gui)

        solution_Renan = Renan_heuristic(df_expected_task_time=df_task_time, df_task_performance =df_aptitudes, num_tasks=num_tasks, machine_quantity=machine_quantity)
        (std, total_cost, differences ) = calculate_std(solution=solution_Renan, df_expected_time=df_task_time, df_aptitude=df_aptitudes)
        results_differences["Renan"].append(differences)
        results_total_cost["Renan"].append(total_cost)
        results_std["Renan"].append(std)
        results_attributions["Renan"].append(solution_Renan)
        #print(std_gui)
        #results["Gui"].append(std_gui)
    return (results_std, results_total_cost, results_differences, input, results_attributions)


def main():
    pair_small = main_num_tasks(num_tasks=25)
    pair_medium = main_num_tasks(num_tasks=50)
    pair_large = main_num_tasks(num_tasks=100)
    write_output(pair_small=pair_small, pair_medium=pair_medium, pair_large=pair_large, iteration=num_interations )
    #write_output(pair_small=pair_small, pair_medium=None, pair_large=None, iteration=num_interations )


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