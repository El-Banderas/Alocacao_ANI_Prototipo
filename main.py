from input.input import read_input
from solver.solver import main_solver
from write_output.write_output_excel import write_output

path_input_excel = './input/input.xlsm'

if __name__ == '__main__':
    input = read_input(path_excel=path_input_excel)
    attribution = main_solver(input=input)
    print("Output")
    print(attribution)
    write_output(output=attribution, excel_path=path_input_excel)



    