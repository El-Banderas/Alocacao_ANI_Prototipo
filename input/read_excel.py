from openpyxl import load_workbook

class Excel_Information:
    def __init__(self, excel_file, configuration : dict ):
        self.excel_file = excel_file
        self.configuration = configuration
        self.num_technician  = -1  
        self.num_projects = -1 

    def split_cell_position(self, cell_position : str):
        return cell_position.split("/")

    # This function receives the excel file open, and the position of the cell, and returns the value
    # The cell position must be in the following format: "sheetname/cell"
    # One example: Compatibilidade/C2
    def get_value(self, cell_position : str):
        sheetname, cell = self.split_cell_position(cell_position=cell_position)

        if sheetname in self.excel_file.sheetnames:
            sheet = self.excel_file[sheetname]
            return sheet[cell].value
        else:
            raise Exception(f"[READ EXCEL - get cell] Invalid excel, missing {sheetname} sheet")

    def get_compability_matrix(self):
        sheetname, cell = self.split_cell_position(cell_position=self.configuration["compatibility"])
        if sheetname in self.excel_file.sheetnames:
            sheet = self.excel_file[sheetname]
            print("CELL")
            row_index_start = ord(cell[0].lower())-96 
            column_index_start = int(cell[1:]) 
            print(f"Starting at {column_index_start} {row_index_start}")
            
            for current_tecn in range(self.num_technician+1):
                    current_row = column_index_start+current_tecn
                    for current_project in range(self.num_projects+1):
                        current_col = row_index_start+current_project
                        #print(f"Current position {current_row} / {current_col}:   {sheet.cell(row=current_row, column=current_col).value}")
                        print(f"Aptidão tecn: {current_tecn+1} | proj : {current_project+1} : {sheet.cell(row=current_row, column=current_col).value}")

        else:
            
            raise Exception(f"[READ EXCEL - compability] Invalid excel, missing {sheetname} sheet")
        


def read_excel(path_excel_input : str, configuration : dict):

    excelFile = load_workbook(filename = path_excel_input, data_only=True)
    excel_file = Excel_Information(excel_file=excelFile, configuration=configuration)
    excel_file.num_technician = excel_file.get_value( cell_position=configuration["general_data"]["num_technician"])
    excel_file.num_projects = excel_file.get_value( cell_position=configuration["general_data"]["num_projects"])
    excel_file.get_compability_matrix()
    
