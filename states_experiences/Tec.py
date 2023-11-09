class Tech:
    # Yes, the technician that does the analisis of "candidatura" is called "anal" :)
    def __init__(self, id : int, area : int, list_projects, line_index : int):
        self.id = id
        self.area = area
        self.list_projects = list_projects
        self.line_index = line_index

    def __str__(self):
        return f"[{self.id} ({self.list_projects})] "
    
def read_tech(workbook):
    projetos_sheet = workbook["Técnicos"]
    current_line = 2
    list_techs = []
    while (True):

        this_id = projetos_sheet.cell(row=current_line, column=1).value
        if this_id == None:
            break
        theme_area = projetos_sheet.cell(row=current_line, column=2).value
        already_alocated_projects = projetos_sheet.cell(row=current_line, column=3).value
        list_techs.append(Tech(id=this_id, area=theme_area, list_projects=already_alocated_projects ,line_index=current_line))
        current_line+=1
    return list_techs

