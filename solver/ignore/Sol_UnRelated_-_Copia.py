import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Define the interval of time tasks require for completion
min_task_length = 300
max_task_length = 700

# Define the number tasks
num_tasks = 25
# Create a DataFrame with random values of task length
expected_task_time = np.random.uniform(
    min_task_length, max_task_length, size=(num_tasks, 1)
)
df_expected_task_time = pd.DataFrame(expected_task_time)


# Create allocation recorder for solution interpretation
solution = np.full((num_tasks, 1), -1)
df_solution = pd.DataFrame(solution)

# Define the number of machines or workers
machine_quantity = 5

# Create aptitude matrix.
max_aptitude = 1.2
min_aptitude = 0.7

aptitude_between_task_machine = np.random.uniform(
    min_aptitude, max_aptitude, size=(num_tasks, machine_quantity)
)
df_aptitude_between_task_machine = pd.DataFrame(aptitude_between_task_machine)


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


print(df_solution)
print(df_load_per_machine)
print(Load_Objective)


gantt = np.zeros((num_tasks, 3))

df_gantt = pd.DataFrame(gantt)

df_gantt.columns = ["Task", "Machine", "Time"]

for r in range(num_tasks):
    df_gantt.iat[r, 0] = r
    df_gantt.iat[r, 1] = df_solution.iat[r, 0]
    df_gantt.iat[r, 2] = df_task_time_per_machine.iat[r, df_solution.iat[r, 0]]

print(df_gantt)


# Create a DataFrame to store the Gantt chart data
gantt_data = []

# Initialize current time for each machine
current_time = [0] * machine_quantity

# Assign tasks to machines and update the Gantt chart data
for task in range(num_tasks):
    machine = df_task_time_per_machine.iloc[
        task
    ].idxmin()  # Find the machine with the shortest time
    task_time = df_task_time_per_machine.iloc[task, machine]
    gantt_data.append(
        [task, machine, current_time[machine], current_time[machine] + task_time]
    )
    current_time[machine] += task_time

# Create a DataFrame for the Gantt chart
df_gantt = pd.DataFrame(
    gantt_data, columns=["Task", "Machine", "Start Time", "End Time"]
)

# Plot the Gantt chart
fig, ax = plt.subplots(figsize=(10, 6))

# Define colors for tasks
colors = plt.cm.get_cmap("tab20", num_tasks)

# Plot Gantt bars
for task, color in zip(range(num_tasks), colors.colors):
    task_data = df_gantt[df_gantt["Task"] == task]
    for i, row in task_data.iterrows():
        ax.barh(
            y=row["Machine"],
            left=row["Start Time"],
            width=row["End Time"] - row["Start Time"],
            height=0.5,
            color=color,
            label=f"Task {int(row['Task'])}",
        )

# Customize the plot
ax.set_xlabel("Time")
ax.set_ylabel("Machine")
ax.set_yticks(range(machine_quantity))
ax.set_yticklabels([f"Machine {i}" for i in range(machine_quantity)])
ax.set_title("Stacked Gantt Chart")
ax.legend(title="Tasks")

plt.show()
