import random
import numpy as np

# Definir o número de máquinas e tarefas
num_machines = 3
num_tasks = 5

# Definir os intervalos de tempos das tarefas e níveis de aptidão
min_task_length = 180
max_task_length = 570
min_aptitude_index = 0.5
max_aptitude_index = 1.5

# Gerar tempos de tarefas aleatórios
task_time = [np.random.randint(min_task_length, max_task_length) for _ in range(num_tasks)]

# Criar matriz de níveis de aptidão aleatórios
aptitude_index_matrix = [[np.random.uniform(min_aptitude_index, max_aptitude_index) for _ in range(num_machines)] for _ in range(num_tasks)]


#################### A partir daqui é diferente
# A execution time matrix é calculada a partir dos outros dados

# Criar matriz de tempos de execução das tarefas nas máquinas resultante (para cálculo da carga restante)
execution_time_matrix = [[0 for _ in range(num_machines)] for _ in range(num_tasks)]

for i in range(num_tasks):
        for j in range(num_machines):
            execution_time_matrix[i][j] = task_time[i] * aptitude_index_matrix[i][j]


# Inicializar a matriz de tempos de execução real das tarefas nas máquinas
real_execution_time_matrix = np.zeros((num_tasks, num_machines))

# Inicializar a lista de carga atual das máquinas
current_load_per_machine = [0] * num_machines

# Gerar cargas restantes iniciais das máquinas
remaining_load_per_machine = [sum(execution_time_matrix[i]) for i in range(num_machines)]

# Inicializar a lista de tarefas não alocadas
unmapped_tasks = list(range(num_tasks))
random.shuffle(unmapped_tasks)

# Inicializar registo das alocações por máquina
allocation_record = {machine: [] for machine in range(num_machines)}

# Repetir até que todas as tarefas estejam alocadas
while unmapped_tasks:
    # Escolher a máquina com a carga restante mais alta
    machine_to_use = max(range(num_machines), key=lambda machine: remaining_load_per_machine[machine])

    # Ordenar tarefas pela priorização de maior tempo de processamento (LPT) na máquina selecionada
    print("TT")
    machine_to_use_loads = execution_time_matrix[machine_to_use]
    machine_to_use_loads.sort(reverse=True)
    print(machine_to_use_loads)
    unmapped_tasks.sort(key=lambda task: -machine_to_use_loads[task])

    # Escolher a primeira tarefa da lista ordenada
    selected_task = unmapped_tasks.pop(0)

    print("Selected task")
    print(selected_task)
    # Escolher a máquina que minimize a carga de trabalho atual
    target_machine = min(range(num_machines), key=lambda machine: current_load_per_machine[machine])

    # Registar a alocação da tarefa à máquina selecionada
    allocation_record[target_machine].append(selected_task)

    # Alocar a tarefa à máquina selecionada e atualizar a carga de trabalho
    real_execution_time_matrix[selected_task, target_machine] = task_time[selected_task] * aptitude_index_matrix[selected_task][target_machine]
    current_load_per_machine[target_machine] += real_execution_time_matrix[selected_task, target_machine]

# Carga final por máquina
final_load_per_machine = [current_load_per_machine[i] for i in range(num_machines)]

# Calcular carga máxima/mínima
max_load = max(current_load_per_machine)
min_load = min(current_load_per_machine)

print(max_load)
print(min_load)

# Calcular o desvio padrão entre as diferentes cargas
sd_load = np.std(current_load_per_machine)

print(sd_load)

# Imprimir solução (alocações por máquina)
for machine, tasks in allocation_record.items():
    print(f"Solution {machine}: {tasks}")