import random
import numpy as np
import sys
import pandas as pd
import statistics

class Machine:
    def __init__(self, machine_id : int):
        self.machine_id = machine_id
        self.attributed_tasks = []
        # We store tuples composed by task_id and cost
        self.initial_random_tasks = []
        self.total_current_tasks = 0
        self.total_remaining_tasks = 0
    
    def add_task_remaining(self, task_id, cost):
        pair_task_id_cost = (task_id, cost)
        self.initial_random_tasks.append(pair_task_id_cost)
        self.total_remaining_tasks += cost

    # The cost is the vaue in the matrix
    # And we store here to save time accessing the aptitude matrix
    def add_task(self,task_id : int, cost : int):
        pair_task_id_cost = (task_id, cost)
        self.attributed_tasks.append(pair_task_id_cost)
        self.total_current_tasks += cost
    

def get_more_remaining_machine(machines : list[Machine]):
    # Store the machine with more jobs, and quantity
    return max(machines, key = lambda machine : machine.total_remaining_tasks)

def get_more_heavy_task(machine : Machine):
    pair_heavy_task = max(machine.initial_random_tasks, key = lambda pair : pair[1])
    machine.initial_random_tasks.remove(pair_heavy_task)
    (task_id, cost) = pair_heavy_task
    print("COST")
    print(cost)
    machine.total_remaining_tasks = machine.total_remaining_tasks - cost
    return task_id 

# Returns the machine that will contain the task
def find_best_fit_for_task(machines : list[Machine], df_aptitude_between_task_machine, n_machines, task_id):
    min_cost =  sys.maxsize
    min_ind = -1
    for current_machine in range(n_machines):
        if df_aptitude_between_task_machine.iat[task_id, current_machine] < min_cost:
            min_cost =  df_aptitude_between_task_machine.iat[task_id, current_machine]
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




def carolina_heuristica(df_expected_task_time, df_aptitude_between_task_machine, num_tasks, machine_quantity):
    # Create random attribution for all machines
    machines = []
    for i in range(machine_quantity):
       machines.append(Machine(machine_id=i+1))
    # Assign tasks to machines, following a simple order.
    for task_id in range(num_tasks):
        this_machine_id = task_id % machine_quantity
        # To calculate the cost, we don't have to consider the size of task, only the aptitude
        # Because the cost of task is constant for all, so it's unecessary computation
        # But when we compare with other heuristics, we have to consider that.
        cost = df_aptitude_between_task_machine.iat[task_id, this_machine_id]
        machines[this_machine_id].add_task_remaining(task_id, cost)
    

    already_attributed_tasks = set()
    solution = []
    while len(already_attributed_tasks) < num_tasks:
        # Machine with more remaining work
        this_machine = get_more_remaining_machine(machines=machines)
        # Get and remove the more heavy task of that machine
        task_id = get_more_heavy_task(machine=this_machine)
        already_attributed_tasks.add(task_id)
        attributed_machine = find_best_fit_for_task(machines=machines, df_aptitude_between_task_machine=df_aptitude_between_task_machine, n_machines=machine_quantity, task_id=task_id)
        print("Iteration [machine_id / task_id / dest_machine]: ", this_machine.machine_id , " : ", task_id +1, " -> ", attributed_machine-1)
        solution.insert(task_id, attributed_machine)
    load_per_machine = get_load_per_machine(machines=machines, df_expected_task_time=df_expected_task_time)
    print("Solution Carol")
    print(solution)
    print(load_per_machine)
    return np.std(load_per_machine)
        
 