from openpyxl import load_workbook

class Excel_Information:
    def __init__(self, excel_file, configuration : dict ):
        self.excel_file = excel_file
        self.configuration = configuration
        self.num_technician  = -1  
        self.num_projects = -1 
        # This matrix is stored like it's in the excel file.
        # Each row is a technician, and the columns are projects.
        self.compatibilities = []
        # Each position corresponds to the number of technician
        self.tecn_years_service = []

    def split_cell_position(self, cell_position : str):
        return cell_position.split("/")

    def get_sheet_by_name(self, sheetname : str):
        if sheetname in self.excel_file.sheetnames:
            return self.excel_file[sheetname]
        else:
            raise Exception(f"[READ EXCEL] Invalid excel, missing {sheetname} sheet")



    # This function receives the excel file open, and the position of the cell, and returns the value
    # The cell position must be in the following format: "sheetname/cell"
    # One example: Compatibilidade/C2
    def get_value(self, cell_position : str):
        sheetname, cell = self.split_cell_position(cell_position=cell_position)
        sheet  = self.get_sheet_by_name(sheetname=sheetname)
        return sheet[cell].value

    def get_compability_matrix(self):
        sheetname, cell = self.split_cell_position(cell_position=self.configuration["compatibility"])
        sheet = self.get_sheet_by_name(sheetname=sheetname)
        print("CELL")
        row_index_start = ord(cell[0].lower())-96 
        column_index_start = int(cell[1:]) 
        print(f"Starting at {column_index_start} {row_index_start}")
        
        for current_tecn in range(self.num_technician+1):
                current_row = column_index_start+current_tecn
                this_technician_projects = []
                for current_project in range(self.num_projects+1):
                    current_col = row_index_start+current_project
                    this_technician_projects.append(sheet.cell(row=current_row, column=current_col).value)
                    #print(f"Current position {current_row} / {current_col}:   {sheet.cell(row=current_row, column=current_col).value}")
                    print(f"Aptidão tecn: {current_tecn+1} | proj : {current_project+1} : {sheet.cell(row=current_row, column=current_col).value}")
                self.compatibilities.append(this_technician_projects)

        
    def get_years_service(self):
        sheetname, cell = self.split_cell_position(cell_position=self.configuration["technician"]["service_year"])

        sheet = self.get_sheet_by_name(sheetname=sheetname)
        column_index_start = ord(cell[0].lower())-96 
        row_index_start = int(cell[1:]) 
        for current_tecn in range(self.num_technician+1):
            self.tecn_years_service.append(sheet.cell(row=row_index_start+current_tecn, column=column_index_start).value)
        print("Years service")
        print(self.tecn_years_service)

def read_excel(path_excel_input : str, configuration : dict):

    excelFile = load_workbook(filename = path_excel_input, data_only=True)
    excel_information = Excel_Information(excel_file=excelFile, configuration=configuration)
    excel_information.num_technician = excel_information.get_value( cell_position=configuration["general_data"]["num_technician"])
    excel_information.num_projects = excel_information.get_value( cell_position=configuration["general_data"]["num_projects"])
    excel_information.get_compability_matrix()
    excel_information.get_years_service()
    return excel_information
    
