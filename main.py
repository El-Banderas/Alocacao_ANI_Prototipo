from input.input import read_input
from solver.solver import main_solver
from output.write_output_excel import write_output
from server.server import server_main

path_input_excel = './input/Excel_input.xlsm'
path_output_excel = './output/output.xlsx'

if __name__ == '__main__':
    input = read_input(path_excel=path_input_excel)
    attribution = main_solver(input=input)
    write_output(output=attribution, excel_path=path_output_excel)
    print("Conclusão da execução do programa")
    server_main(input=input, atributtion=attribution)



    