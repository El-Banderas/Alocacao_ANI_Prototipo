# The main for second phase ;)

from input.inputAPI import read_input_api
#from solver.solver import main_solver
#from server.server import server_main

inputURL = 'https://ani-fake-api.onrender.com'
path_input_excel = './states_experiences/states_V2.xlsm'
test_frontend = False

if __name__ == '__main__':
    # Here we also write to BD
    input = read_input_api(url=inputURL)

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