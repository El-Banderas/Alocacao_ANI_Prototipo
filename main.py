from input.input import read_input
from solver.solver import main_solver
from output.write_output_excel import write_output
from server.server import server_main

path_input_excel = './input/states_V2.xlsm'

if __name__ == '__main__':
    input = read_input(path_excel=path_input_excel)
    attribution = main_solver(input=input)
    # Because the excel could be all filled
    if attribution != None:
        write_output(output=attribution, excel_path=path_input_excel, excel_input_info=input.excel_information)
        input.excel_information.get_projects_info()
    server_main(input=input, atributtion=attribution)


#Olá teste
    