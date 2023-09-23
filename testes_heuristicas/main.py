import pandas as pd
import numpy as np

from Gui_heuristica import gui_heuristica

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

def main():
    results = {"Gui" : [], "Carolina" : [], "Renan" : []}
    for interation in range(num_interations):
        (df_task_time, df_aptitudes) = generate_input()
        std_gui = gui_heuristica(df_expected_task_time=df_task_time, df_aptitude_between_task_machine=df_aptitudes, num_tasks=num_tasks, machine_quantity=machine_quantity)
        print(std_gui)
        results["Gui"].append(std_gui)
    print("Results")
    print(results)

main()