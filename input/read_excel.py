from openpyxl import load_workbook
#import sys
import xlwings as xw 
#sys.path.insert(0,"..")
from info_classes.Tech import Tech
from info_classes.Project import Proj
import sys
import datetime

def convert_int_char(col : int):
    return chr(col+64)

def maybe_convert_int(value : int):
    if value:
        return int(value)

class Excel_Information:
    def __init__(self, excel_file, configuration : dict ):
        self.excel_file = excel_file
        self.configuration = configuration
        self.num_technician  = -1  
        # To heuristic
        self.num_projects = -1 
        # To frontend (this values can be different if projects are already allocated)
        self.num_projects_all = -1 
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
        # Techs unavailable stored by id
        self.tecs_unavailable : list[int] = []
        # Efforts of each available tecn. Each index corresponds to the id of valid tecn minus 1.
        # Used to heuristic, reduce input size
        self.available_tecns_effort : list[int] = []
        # Used to interface, show effort all tecns
        self.all_tecns_effort : list[int] = []
        # The two variables above should have been combined to save memory, but could create errors...

    ################################# General functions to read excel ######################

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
    
    ############################ INFO TO HEURISTICS ##########################################

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
        self.num_projects_all = num_projects
        print(f"NUM tecns: {num_tecns} / NUM projs: {num_projects}")

    # If all cells of the project are empty (None), the project is already allocated, or has finished.
    def check_if_project_needs_allocation(self, sheet, row : int, start_col : int):
        for i in range(self.num_technician):
            if self.get_value_by_index(sheet=sheet, index_row=row, index_col=start_col+i) != None:
                return True
        return False

    def get_compability_matrix(self):
        sheetname, cell = self.split_cell_position(cell_position=self.configuration["compatibility2"])
        sheet = self.get_sheet_by_name(sheetname=sheetname)
        row_index_start = ord(cell[0].lower())-96 
        column_index_start = int(cell[1:]) 
        current_proj = 0
        # This is used in the end to replace the +inf
        max_value = -1
        while(current_proj < self.num_projects):
            current_row = row_index_start+current_proj

            this_project_values = []
            current_col = column_index_start
            # Check if project needs calculation
            if self.check_if_project_needs_allocation(sheet=sheet, row=current_row, start_col=current_col):
                for current_tecn in range(self.num_technician):
                    this_aptitude = self.get_value_by_index(sheet=sheet, index_row=row_index_start+current_proj, index_col=column_index_start+current_tecn)
                    # When tecn can't do the job
                    if this_aptitude == None:
                        #print("NONE?")
                        # Because Python 3 doesn't have a max number
                        this_aptitude = sys.maxsize
                    else:
                        this_aptitude = (this_aptitude)
                        if this_aptitude > max_value: 
                            max_value = this_aptitude
                    this_project_values.append(this_aptitude)
                    #print(f"Aptidão tecn: {current_tecn+1} | proj : {current_proj+1} : {this_aptitude}")
                
                #print(f"Project readen: {self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_index_start-1)}")
                #self.compatibilities.append(this_technician_projects)
                self.compatibilities.append(this_project_values)
                self.projects_handled.append(int(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_index_start-1)))
            current_proj += 1
        for line in range(len(self.compatibilities)):
            for cell in range(len(self.compatibilities[line])):
                if self.compatibilities[line][cell] == sys.maxsize:
                    self.compatibilities[line][cell]= max_value*5
        print("Results")
        print(self.compatibilities)
        print(self.projects_handled)
        self.num_projects = len(self.compatibilities)

        
    def get_current_ocupation_tecns(self):
        sheetname, cell = self.split_cell_position(cell_position=self.configuration["current_effort"])

        sheet = self.get_sheet_by_name(sheetname=sheetname)
        column_index_start = ord(cell[0].lower())-96 
        row_index_start = int(cell[1:]) 
        for current_tecn in range(self.num_technician):
            effort_current_tecn = self.get_value_by_index(sheet=sheet, index_row=row_index_start, index_col=(current_tecn+column_index_start))
            self.all_tecns_effort.append(effort_current_tecn)
            if current_tecn+1 not in self.tecs_unavailable:
                self.available_tecns_effort.append(effort_current_tecn)

    def get_tecs_not_available(self):
        sh_disponibility, cell_disponibility = self.split_cell_position(cell_position=self.configuration["technician"]["disponibility"])
        _, cell_id = self.split_cell_position(cell_position=self.configuration["technician"]["id"])

        sheet = self.get_sheet_by_name(sheetname=sh_disponibility)
        column_disponibility = ord(cell_disponibility[0].lower())-96 
        column_id = ord(cell_id[0].lower())-96 
        current_row = int(cell_disponibility[1:]) 
        while(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_id) != None):
            if self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_disponibility) == 0:
                current_tec_id = int(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_id) )
                self.tecs_unavailable.append(current_tec_id) 
            current_row+=1
    
    ######################################### FRONTEND INFO READEN HERE #######################
    
    # Here we assume every info of a tech is in the same row
    # So, we read line by line, and store in a tech.
    # There should be no empty cells between them
    def get_tecns_info(self):
        sh_techs, cell_id = self.split_cell_position(cell_position=self.configuration["technician"]["id"])
        _same_as_previous, cell_disponibility = self.split_cell_position(cell_position=self.configuration["technician"]["disponibility"])
        _same_as_previous, cell_service_year = self.split_cell_position(cell_position=self.configuration["technician"]["service_year"])

        sheet = self.get_sheet_by_name(sheetname=sh_techs)
        current_row = int(cell_id[1:]) 
        column_id = ord(cell_id[0].lower())-96 
        column_disponibility = ord(cell_disponibility[0].lower())-96 
        column_service_year = ord(cell_service_year[0].lower())-96 
        for current_tech in range(self.num_technician):
            this_id = self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_id)
            this_disponibility = int(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_disponibility)) == 1
            this_service_year = self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_service_year)
            this_cur_effort = self.all_tecns_effort[current_tech]
            #print(f"Tech {this_id}: Available {this_disponibility} started {this_service_year} effort {this_cur_effort}")
            this_tech = Tech(service_year=this_service_year, id=this_id, availability=this_disponibility,current_effort=this_cur_effort ) 
            self.tecns.append(this_tech)
            current_row += 1

    
    # Here we assume every info of a tech is in the same row
    # So, we read line by line, and store in a tech.
    # There should be no empty cells between them
    def get_projects_info(self):
        self.tasks = []
        tasks_config = self.configuration["tasks"]
        sh_tasks, cell_id = self.split_cell_position(cell_position=tasks_config["id"])
        _same_as_previous, cell_durationAnalysis = self.split_cell_position(cell_position=tasks_config["durationAnal"])
        _same_as_previous, cell_durationAccomp = self.split_cell_position(cell_position=tasks_config["durationAcom"])
        _same_as_previous, cell_themeArea = self.split_cell_position(cell_position=tasks_config["ThemeArea"])
        _same_as_previous, cell_nProm = self.split_cell_position(cell_position=tasks_config["N.Prom"])
        _same_as_previous, cell_Phase = self.split_cell_position(cell_position=tasks_config["Phase"])
        _same_as_previous, cell_Phase = self.split_cell_position(cell_position=tasks_config["Phase"])
        _same_as_previous, cell_InitDate = self.split_cell_position(cell_position=tasks_config["DateInit"])
        _same_as_previous, cell_EndDate = self.split_cell_position(cell_position=tasks_config["DateEnd"])
        cell_analise = self.configuration["write_allocation"]["analise"]
        cell_other = self.configuration["write_allocation"]["gestor"]
        sheet = self.get_sheet_by_name(sheetname=sh_tasks)
        current_row = int(cell_id[1:]) 
        column_id = ord(cell_id[0].lower())-96 
        column_duration1  = ord(cell_durationAnalysis[0].lower())-96 
        column_duration2  = ord(cell_durationAccomp[0].lower())-96 
        column_area = ord(cell_themeArea[0].lower())-96 
        column_nProm = ord(cell_nProm[0].lower())-96 
        column_phase = ord(cell_Phase[0].lower())-96 
        column_initDate = ord(cell_InitDate[0].lower())-96 
        column_endDate = ord(cell_EndDate[0].lower())-96 
        column_analises = ord(cell_analise[0].lower())-96 
        column_other = ord(cell_other[0].lower())-96 
        for current_project in range(self.num_projects_all):
            this_id = int(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_id))
            this_durationAnalysis = int(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_duration1))
            this_durationAccomp = int(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_duration2))
            this_area = self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_area)
            this_nProm = self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_nProm)
            this_phase = self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_phase)
            this_initDate = self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_initDate)
            this_endDate = self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_endDate)
            this_analise = maybe_convert_int(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_analises))
            this_other = maybe_convert_int(self.get_value_by_index(sheet=sheet, index_row=current_row, index_col=column_other))
            print(f"Proj {this_id}: duration {this_durationAccomp+this_durationAnalysis} area {this_area} prom {this_nProm} phase {this_phase} tecns: {this_analise}/{this_other}")
            this_proj = Proj(id=this_id,costAnalysis=this_durationAnalysis, costAccomp=this_durationAccomp, nProm=this_nProm, currentPhase=this_phase, theme=this_area,analysis_tech=this_analise, other_tech=this_other)
            this_initDate = this_initDate.strftime("%d/%m/%Y")
            this_endDate = this_endDate.strftime("%d/%m/%Y")
            this_initDate = str(this_initDate).split(" ")[0]
            this_endDate = str(this_endDate).split(" ")[0]
            this_proj.addDates(init_date=this_initDate, end_date=this_endDate)
            self.tasks.append(this_proj)
            current_row += 1
    

def read_excel(path_excel_input : str, configuration : dict):

    excelFile = xw.Book(path_excel_input)#load_workbook(filename = path_excel_input, data_only=True)
    excel_information = Excel_Information(excel_file=excelFile, configuration=configuration)
    excel_information.get_tecs_not_available()
    excel_information.get_num_tecns_projs()
    excel_information.get_compability_matrix()
    excel_information.get_current_ocupation_tecns()
    excel_information.get_tecns_info()
    #excel_information.get_projects_info()
    return excel_information


    
