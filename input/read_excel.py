from openpyxl import load_workbook
#import sys
import xlwings as xw 
#sys.path.insert(0,"..")
from info_classes.Tech import Tech
from info_classes.Project import Proj
import sys

def convert_int_char(col : int):
    return chr(col+64)

class Excel_Information:
    def __init__(self, excel_file, configuration : dict ):
        self.excel_file = excel_file
        self.configuration = configuration
        self.num_technician  = -1  
        self.num_projects = -1 
        # This matrix is stored like it's in the excel file.
        # Each row is a technician, and the columns are projects.
        self.compatibilities : list[int][int] = []
        # To store the id's of projects that are handled
        # If this has [3,4,7], the projects we will alcoate are 3, 4 and 7, the others we don't process
        self.projects_handled : list[int] = []
        # Each position corresponds to the number of technician
        self.tecns : list[Tech] = []
        # Duration of each task
        self.tasks : list[Proj] = []

    def split_cell_position(self, cell_position : str):
        return cell_position.split("/")

    def get_sheet_by_name(self, sheetname : str):
        if sheetname in self.excel_file.sheet_names:
            return self.excel_file.sheets[sheetname]
        else:
            raise Exception(f"[READ EXCEL] Invalid excel, missing {sheetname} sheet")



    # This function receives the excel file open, and the position of the cell, and returns the value
    # The cell position must be in the following format: "sheetname/cell"
    # One example: Compatibilidade/C2
    def get_value(self, cell_position : str):
        sheetname, cell = self.split_cell_position(cell_position=cell_position)
        sheet  = self.get_sheet_by_name(sheetname=sheetname)
        return sheet[cell].value

    def get_value_by_index(self, sheet, index_row : int, index_col :int): 
        letter_col = convert_int_char(col=index_col)
        #print(f"GET: {letter_col}{index_row}")
        return sheet.range(f"{letter_col}{index_row}").value
    
    def get_num_tecns_projs(self):
        sheetname, cell = self.split_cell_position(cell_position=self.configuration["compatibility2"])
        sheet = self.get_sheet_by_name(sheetname=sheetname)
        current_row_index = ord(cell[0].lower())-96 -1
        current_column_index = int(cell[1:])        
        # Get num tecns
        num_tecns = 0
        while(True):
            if self.get_value_by_index(sheet=sheet, index_row=current_row_index, index_col=current_column_index+num_tecns) != None:
                num_tecns+=1
            else:
                break
        self.num_technician = num_tecns
        num_projects = 0

        while(True):
            if self.get_value_by_index(sheet=sheet, index_row=current_row_index+num_projects+1, index_col=current_column_index-1) != None:
                num_projects+=1
            else:
                break
        self.num_projects = num_projects
        print(f"NUM tecns: {num_tecns} / NUM projs: {num_projects}")



    def get_compability_matrix(self):
        sheetname, cell = self.split_cell_position(cell_position=self.configuration["compatibility2"])
        sheet = self.get_sheet_by_name(sheetname=sheetname)
        row_index_start = ord(cell[0].lower())-96 
        column_index_start = int(cell[1:]) 
        current_proj = 0
        while(current_proj < self.num_projects):
            current_row = row_index_start+current_proj

            this_project_values = []
            current_col = column_index_start
            value_cell1 = self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=current_col)
            value_cell2 = self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=current_col+1)
            # Check if project needs calculation
            if value_cell1 != None or value_cell2 != None:
                for current_tecn in range(self.num_technician):
                    this_aptitude = self.get_value_by_index(sheet=sheet, index_row=row_index_start+current_proj, index_col=column_index_start+current_tecn)
                    # When tecn can't do the job
                    if this_aptitude == None:
                        #print("NONE?")
                        # Because Python 3 doesn't have a max number
                        this_aptitude = sys.maxsize
                        #print(this_aptitude)
                        #this_aptitude == sys.maxsize
                    this_project_values.append(this_aptitude)
                    #print(f"Aptidão tecn: {current_tecn+1} | proj : {current_proj+1} : {this_aptitude}")
                
                #print(f"Project readen: {self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_index_start-1)}")
                #self.compatibilities.append(this_technician_projects)
                self.compatibilities.append(this_project_values)
                self.projects_handled.append(int(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_index_start-1)))
            current_proj += 1
        print("Results")
        print(self.compatibilities)
        print(self.projects_handled)
        self.num_projects = len(self.compatibilities)

        
    def get_current_ocupation_tecns(self):
        sheetname, cell = self.split_cell_position(cell_position=self.configuration["current_effort"])

        sheet = self.get_sheet_by_name(sheetname=sheetname)
        column_index_start = ord(cell[0].lower())-96 
        row_index_start = int(cell[1:]) 
        row_previoues_costs = sheet.range(f"{row_index_start}:{row_index_start}")
        for cell in row_previoues_costs:
            if cell.value == None:
                break
        '''
        for current_tecn in range(self.num_technician+1):
            years_services = sheet.cell(row=row_index_start+current_tecn, column=column_index_start).value
            this_tecn = Tech( service_year =years_services, id=current_tecn+1)
            self.tecns.append(this_tecn)
        '''

    # Here I'm going to assume they are near to each other, to make code simpler.
    # If necessary, make this more complete, when the Excel changes.
    def get_projects_info(self):
        sh_duration, cell_duration = self.split_cell_position(cell_position=self.configuration["tasks"]["duration"])

        sheet = self.get_sheet_by_name(sheetname=sh_duration)
        column_index_start = ord(cell_duration[0].lower())-96 
        row_index_start = int(cell_duration[1:]) 
        for current_project in range(self.num_projects+1):
            this_duration = sheet.cell(row=row_index_start, column=column_index_start+current_project ).value
            this_theme = sheet.cell(row=row_index_start+1, column=column_index_start+current_project ).value
            this_nProm = sheet.cell(row=row_index_start+2, column=column_index_start+current_project ).value
            #print("???")
            #print(sheet.cell(row=row_index_start+2, column=column_index_start+current_project ).value)
            #print(f"{row_index_start+2} - {column_index_start+current_project }")
            this_Phase = sheet.cell(row=row_index_start+3, column=column_index_start+current_project ).value
            this_Proj = Proj(id = current_project+1, cost=this_duration, theme=this_theme, nProm=this_nProm, currentPhase=this_Phase)
            self.tasks.append(this_Proj)


def read_excel(path_excel_input : str, configuration : dict):

    excelFile = xw.Book(path_excel_input)#load_workbook(filename = path_excel_input, data_only=True)
    excel_information = Excel_Information(excel_file=excelFile, configuration=configuration)
    excel_information.get_num_tecns_projs()
    #excel_information.num_technician = excel_information.get_value( cell_position=configuration["general_data"]["num_technician"])  -1
    #excel_information.num_projects = excel_information.get_value( cell_position=configuration["general_data"]["num_projects"]) -1
    excel_information.get_compability_matrix()
    excel_information.get_current_ocupation_tecns()
    #excel_information.get_projects_info()
    return excel_information
    
