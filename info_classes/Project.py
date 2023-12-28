
class Proj:
    def __init__(self, id : int, costAnalysis : int, costAccomp : int,theme: int, nProm : str, currentPhase : int, analysis_tech : int = None, other_tech : int = None):
        self.id = id
        self.costAnalysis = costAnalysis
        self.costAccomp = costAccomp
        self.theme = theme
        # Tipo de promotores, Mobilizador, etc...
        self.nProm = nProm
        self.currentPhase = currentPhase
        self.analysis_tech = analysis_tech 
        self.other_tech = other_tech 
    
    # This value is readen in a different time
    def add_name(self, name : str):
        self.name = name

    def __str__(self):
        return f"Projeto {self.id} - {self.theme} (tema): cost {self.costAnalysis}-{self.costAccomp}/ {self.nProm} (num prom) and {self.currentPhase} (currentPhase) "
    
    def addDates(self, init_date : str, end_date : str):
        self.init_date = init_date
        self.end_date = end_date
    
    def convert_to_dict(self):
        return self.__dict__

    def convert_state_str(self):
        match self.currentPhase:
            case 0:
                return "Por analisar"
            case 1:
                return "Aprovado"
            case 2:
                return "Rejeitado"
            case 3:
                return "Concluído"
            case _:
                return "---"

    def current_effort(self):
        if self.currentPhase == 2:
            return 0
        if self.other_tech == None:
            return self.costAnalysis
        else:
            return self.costAccomp

    def convert_to_dict_pt(self):
        dict_res = {}
        dict_res["id"] = self.id
        dict_res["Esforço análise"] = self.costAnalysis
        dict_res["Esforço acompanhamento"] = self.costAccomp
        dict_res["Tema"] = self.theme
        dict_res["Tipo de projeto"] = self.nProm
        dict_res["Fase atual"] = self.convert_state_str()
        dict_res["Técnico análise"] = self.analysis_tech
        dict_res["Técnico acompanhamento"] = self.other_tech
        dict_res["Sigla"] = self.name
        dict_res["Data início"] = self.init_date
        dict_res["Data fim"] = self.end_date
        dict_res["Esforço atual"] = self.current_effort()
        return dict_res