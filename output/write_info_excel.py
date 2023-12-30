

from input.inputAPI import InputAPI


def write_api_info_excel(input : InputAPI, path_excel : str):
    print("Lista tecns:")
    print(len(input.list_tecns))
    print(input.list_tecns)
    print(input.list_tecns[0], end="\n\n")
    print("Lista projects:")
    print(len(input.list_projs))
    print(input.list_projs[0], end="\n\n")
    print("Path excel: ", path_excel)