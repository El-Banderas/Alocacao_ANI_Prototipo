from input.input import Input
from solver.CarolUpdateRemainingCost import carolina_heuristicaURC
from solver.Carolina_Unrelated import carolina_heuristica
from solver.Gui_heuristica import gui_heuristica
import pandas as pd
import numpy as np

'''
This methods calculates the initial heuristic for the attribution. 
The two methods are:
works: list of durations of each work. 
aptitudes_matrix: matrix that correlates the cost of workers to complete the task. It follows the same structure as the excel file.
                  Each line/row represents one technique and the columns are the tasks.
'''
def heuristic_test(works : list[int], aptitudes_matrix : list[list[int]]):
    print("Error")
    print(aptitudes_matrix)
    df_expected_task_time = pd.DataFrame(works)
    num_tasks = len(works)
    # Create allocation recorder for solution interpretation
    solution = np.full((num_tasks, 1), -1)
    df_solution = pd.DataFrame(solution)

    # Define the number of machines or workers
    machine_quantity = len(aptitudes_matrix)


    df_aptitude_between_task_machine = pd.DataFrame(aptitudes_matrix)


    # Calculate task time per machine

    df_reciprocral_aptitude_between_task_machine = 1 / df_aptitude_between_task_machine

    df_task_time_per_machine = df_reciprocral_aptitude_between_task_machine.multiply(
        df_expected_task_time.squeeze(), axis=0
    )

    # Calculate ideal load value
    load_per_machine = np.zeros((1, machine_quantity))
    df_load_per_machine = pd.DataFrame(load_per_machine)

    Load_Objective = df_load_per_machine.max().max()

    net_gain = np.full((num_tasks, machine_quantity), np.nan)
    df_net_gain = pd.DataFrame(net_gain)

    df_filter_list = pd.DataFrame({"Task": [-2] * num_tasks})

    # --------------------------------------------------------#

    for j in range(num_tasks):
        for r in range(num_tasks):
            for c in range(machine_quantity):
                df_net_gain.iat[r, c] = (
                    Load_Objective
                    - df_load_per_machine.iat[0, c]
                    - df_task_time_per_machine.iat[r, c]
                )

        df_net_gain_string = df_net_gain.stack().reset_index()
        df_net_gain_string.columns = ["Task", "Machine", "NetGain"]

        # Filter out before sorting the tasks already allocated so they can't be selected later on.
        df_net_gain_string = df_net_gain_string[
            ~df_net_gain_string["Task"].isin(df_filter_list["Task"])
        ]

        df_net_gain_string_sorted = df_net_gain_string.sort_values(
            by="NetGain", ascending=False
        )

        df_net_gain_string_sorted = df_net_gain_string_sorted.reset_index(drop=True)

        df_load_per_machine.iat[
            0, df_net_gain_string_sorted.iat[0, 1]
        ] += df_task_time_per_machine.iat[
            df_net_gain_string_sorted.iat[0, 0], df_net_gain_string_sorted.iat[0, 1]
        ]

        df_solution.iat[
            df_net_gain_string_sorted.iat[0, 0], 0
        ] = df_net_gain_string_sorted.iat[0, 1]

        df_filter_list.iat[j, 0] = df_net_gain_string_sorted.iat[0, 0]

        Load_Objective = df_load_per_machine.max().max()


    '''
    print(df_solution)
    print(df_load_per_machine)
    print(Load_Objective)
    '''
    return df_solution.values



def main_solver(input : Input):
    print("Starting heuristic")
    #attribution = heuristic_test(works=input.excel_information.duration_tasks, aptitudes_matrix=input.excel_information.compatibilities)
    num_techs = input.excel_information.num_technician+1
    current_total_occupations = [0] * num_techs
    df_aptitudes = pd.DataFrame(input.excel_information.compatibilities)
    durations_tasks = map(lambda proj : proj.cost, input.excel_information.tasks)
    if input.excel_information.compatibilities == []:
        return None
    
    df_task_time = pd.DataFrame(durations_tasks)
    attribution1 = carolina_heuristicaURC(df_aptitude_between_task_machine =df_aptitudes, num_tasks=input.excel_information.num_projects , machine_quantity=input.excel_information.num_technician , previous_costs=current_total_occupations)
    #attribution2 = gui_heuristica(df_aptitude_between_task_machine=df_aptitudes, df_expected_task_time=df_task_time, num_tasks=input.excel_information.num_projects+1 , machine_quantity=input.excel_information.num_technician+1 )
    #print("ATR1")
    #print(attribution1)
    #print("ATR2")
    #print(attribution2)
    return attribution1