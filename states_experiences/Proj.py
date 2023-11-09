class Project:
    # Yes, the technician that does the analisis of "candidatura" is called "anal" :)
    def __init__(self, id : int, area : int, current_phase : int, tec_anal : int, tec_manager : int, line_index : int):
        self.id = id
        self.area = area
        self.current_phase = current_phase
        self.tec_anal = tec_anal
        self.tec_manager = tec_manager
        self.line_index = line_index
    def __str__(self):
        return f"[{self.id} ({self.current_phase})] "

