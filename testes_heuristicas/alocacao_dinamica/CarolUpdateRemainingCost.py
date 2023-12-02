import random
import numpy as np
import sys
import pandas as pd
import statistics


class Machine:
    def __init__(self, machine_id : int, df_aptitude_between_task_machine, previous_cost : int):
        self.machine_id = machine_id
        self.attributed_tasks = []
        # We store the costs of tasks in this macine
        self.initial_random_tasks = df_aptitude_between_task_machine[machine_id]
        self.total_current_tasks = previous_cost
        #for i in range(num_tasks):
        self.total_remaining_tasks = df_aptitude_between_task_machine[machine_id].sum()
    

    # The cost is the vaue in the matrix
    # And we store here to save time accessing the aptitude matrix
    def add_task(self,task_id : int, cost : int):
        pair_task_id_cost = (task_id, cost)
        self.attributed_tasks.append(pair_task_id_cost)
        self.total_current_tasks += cost
        #self.total_remaining_tasks -= cost
    # We need to receive the already received tasks so we don't consider them again when checking 
    def get_more_heavy_task(self, already_attributed_tasks : list[int]):
        # More expensive task here
        task_id = -1
        task_cost = 0
        for i in range(len(self.initial_random_tasks)):
            if i not in already_attributed_tasks and self.initial_random_tasks[i] > task_cost:
                #print("Change ", self.initial_random_tasks[i] , " < ", task_cost) 
                #print(i)
                task_id = i
                task_cost = self.initial_random_tasks[i] 
            
        #self.total_remaining_tasks = self.total_remaining_tasks - task_cost
        return task_id 



def get_more_remaining_machine(machines : list[Machine]):
    #for i in range(len(machines)):
    #    print("Remaining: ", machines[i].total_remaining_tasks)
    # Store the machine with more jobs, and quantity
    return max(machines, key = lambda machine : machine.total_remaining_tasks)

# Returns the machine that will contain the task
def find_best_fit_for_task(machines : list[Machine], df_aptitude_between_task_machine, n_machines, task_id):
    min_cost =  sys.maxsize
    min_ind = -1
    for current_machine in range(n_machines):
        if_this_machine_does_it = df_aptitude_between_task_machine.iat[task_id, current_machine] + machines[current_machine].total_current_tasks
        if if_this_machine_does_it <= min_cost:
            # If they got the same cost, we need to compare the total cost to choose
            if if_this_machine_does_it == min_cost:
                if machines[current_machine].total_current_tasks < machines[min_ind].total_current_tasks:
                    min_cost = if_this_machine_does_it
                    min_ind = current_machine
            # If is minimum, we just store the minimum cost
            else:
                min_cost =  if_this_machine_does_it #df_aptitude_between_task_machine.iat[task_id, current_machine]
                min_ind = current_machine
    machines[min_ind].add_task(task_id, df_aptitude_between_task_machine.iat[task_id, min_ind])
    return min_ind
    
def get_load_per_machine(machines : list[Machine], df_expected_task_time):
    machines_costs = []
    for machine in machines:
        total_cost_this_machine = 0
        for (task_id_this_machine, cost_aptitude) in machine.attributed_tasks:
            cost_task = df_expected_task_time.loc[task_id_this_machine].values[0]
            this_cost = cost_task * cost_aptitude
            total_cost_this_machine += this_cost
        machines_costs.append(total_cost_this_machine)
    return machines_costs

def convert_input(df_aptitudes, df_task_time, num_tasks, machine_quantity):
    rows = []
    for task in range(num_tasks):
        this_task_cost = df_task_time.iloc[task]
        costs_machines_this_works = []
        for machine in range(machine_quantity):
            this_aptitude = df_aptitudes.iat[task, machine]
            this_cost = (1 / this_aptitude) * this_task_cost
            costs_machines_this_works.append( this_cost.values[0])
        rows.append(costs_machines_this_works)
    return  pd.DataFrame(rows)
    
def update_remaining_costs(task_id : int, machines : list[Machine], df_aptitudes):
    for machine in machines:
        cost_this_machine = df_aptitudes.iat[task_id, machine.machine_id] 
        #cost_task = df_expected_task_time.loc[task_id_this_machine].values[0]
        #this_cost = cost_task * cost_aptitude
        machine.total_remaining_tasks = machine.total_remaining_tasks - cost_this_machine
 
# Update Remaing Cost
# First matrix joins costs tasks and aptitudes
def carolina_heuristicaURC(df_aptitude_between_task_machine , num_tasks, machine_quantity, previous_costs : list[int]):
    
    # Because input starts by 1
    #machine_quantity = machine_quantity-1
    #num_tasks = num_tasks - 1
    #df_aptitude_between_task_machine = convert_input(df_aptitudes, df_task_time, num_tasks, machine_quantity)
    #df_aptitude_between_task_machine = pd.DataFrame(df_aptitudes)


    # Create random attribution for all machines
    machines = []
    for i in range(machine_quantity):
        machines.append(Machine(machine_id=i,  df_aptitude_between_task_machine=df_aptitude_between_task_machine, previous_cost=previous_costs[i]))
    
    already_attributed_tasks = set()
    solution = [-1] * num_tasks 
    while len(already_attributed_tasks) < num_tasks:
        # Machine with more remaining work
        this_machine = get_more_remaining_machine(machines=machines)
        # Get and remove the more heavy task of that machine
        task_id = this_machine.get_more_heavy_task(already_attributed_tasks=already_attributed_tasks)
        already_attributed_tasks.add(task_id)
        attributed_machine = find_best_fit_for_task(machines=machines, df_aptitude_between_task_machine=df_aptitude_between_task_machine, n_machines=machine_quantity, task_id=task_id)
        update_remaining_costs(task_id=task_id, machines=machines, df_aptitudes=df_aptitude_between_task_machine)
        #print("Iteration [machine_id / task_id / dest_machine]: ", this_machine.machine_id +1 , " : ", task_id +1, " -> ", attributed_machine+1)
        #print("Iteration [machine_id / task_id / dest_machine]: ", this_machine.machine_id  , " : ", task_id , " -> ", attributed_machine)
        solution[task_id] =  attributed_machine
    #load_per_machine = get_load_per_machine(machines=machines, df_expected_task_time=df_expected_task_time)
    #print(load_per_machine)
    return solution
        