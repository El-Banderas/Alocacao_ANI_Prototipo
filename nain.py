# The main for second phase ;)

from input.inputAPI import read_input_api
from solver.solver import main_solver
from output.write_output_excel import write_output
from output.write_info_excel import write_api_info_excel
from server.server import server_main

inputURL = 'http://127.0.0.1:1234'
path_input_excel = './states_experiences/states_V2.xlsm'
test_frontend = False

if __name__ == '__main__':
    input = read_input_api(url=inputURL)
    write_api_info_excel(input=input, path_excel=path_input_excel)
    '''
    Isto aqui é o que está na main antiga, que em princípio se vai manter. 
    input = read_input(path_excel=path_input_excel)

    if not test_frontend:
        attribution = main_solver(input=input)
        # Because the excel could be all filled
        if attribution != None:
            write_output(output=attribution, excel_path=path_input_excel, excel_input_info=input.excel_information)
    input.excel_information.get_projects_info()
    server_main(input=input)
    '''