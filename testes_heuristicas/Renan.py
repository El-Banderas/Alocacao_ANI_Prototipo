import pandas as pd
import numpy as np


def convert_input(df_aptitudes, num_tasks, machine_quantity):
    rows = []
    for task in range(num_tasks):
        costs_machines_this_works = []
        for machine in range(machine_quantity):
            this_aptitude = df_aptitudes.iloc[task, machine]
            this_cost = (1 / this_aptitude) 
            costs_machines_this_works.append( this_cost)
        rows.append(costs_machines_this_works)
    return  pd.DataFrame(rows)
    


def Renan_heuristic(df_expected_task_time, df_task_performance , num_tasks, machine_quantity):
    df_task_performance = convert_input(df_aptitudes=df_task_performance, num_tasks=num_tasks, machine_quantity=machine_quantity)
    # Calculate the median of task performance
    median = df_task_performance.median().median()
    # Initialize an empty DataFrame to store activity allocation
    df_allocation = pd.DataFrame(columns=['Machine', 'Activity'])

    # Initialize a series to track the load of each machine
    machine_loads = pd.Series(index=range(machine_quantity), data=0)

    # Initialize a list to store activity allocation
    allocation_list = []

    # Loop to allocate activities
    for _ in range(num_tasks):
        # Calculate the difference between the median and the current performance of all machines
        load_difference = (df_task_performance - median).abs()

        # Find the activity with the smallest difference
        activity_to_allocate = load_difference.stack().idxmin()

        # Find the machine with the lowest actual load
        lowest_load_machine = machine_loads.idxmin()

        # Allocate the activity to the chosen machine
        allocation_list.append({
            'Machine': lowest_load_machine,
            # Fix here to get the correct index
            'Activity': activity_to_allocate[0]
        })

        # Update the load of the chosen machine
        machine_loads[lowest_load_machine] += df_task_performance.at[activity_to_allocate[0],lowest_load_machine]

        # Remove the allocated activity from the task performance DataFrame
        df_task_performance = df_task_performance.drop(
            activity_to_allocate[0], axis=0)

        # Recalculate the median after allocation
        median = df_task_performance.median().median()

    # Create a DataFrame from the list of activity allocations
    df_allocation = pd.DataFrame(allocation_list)

    #print('Activity Allocation:')
    #print(df_allocation)

    solution = []

    for ind in df_allocation.index:
        #print(df['Name'][ind], df['Stream'][ind])
        solution.insert(df_allocation['Activity'][ind], df_allocation['Machine'][ind])

    # Calculate the total load of the machines
    total_machine_load = machine_loads.sum()

    # Print the total load of the machines
    '''
    print("Total Machine Load:")
    for machine_idx, load in machine_loads.items():
        # Use {:.5f} to format as a real number with 5 decimal places
        print(f"Machine {machine_idx}: {load:.5f}")

    # Use {:.5f} to format as a real number with 5 decimal places
    print(f"Total Load: {total_machine_load:.5f}")
    print(solution)

    print('Fim')
    '''
    return solution