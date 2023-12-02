import pandas as pd
import numpy as np


# As últimas duas variáveis deviam ser lengths, mas como isto é para testes, não me apeteceu procurar
# Procurar como se calcula o comprimento de dataframes (eu não costumo usar dataframes).
def gui_heuristica(
    df_task_time_per_machine, load_per_machine, num_tasks, machine_quantity
):
    # Create allocation recorder for solution interpretation
    solution = np.full((num_tasks, 1), -1)
    df_solution = pd.DataFrame(solution)
    # Calculate task time per machine


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
    # print(df_load_per_machine.T.std().values[0])
    # print(df_load_per_machine)
    return solution
    # print(df_load_per_machine)
    # return df_load_per_machine.T.std().values[0]
