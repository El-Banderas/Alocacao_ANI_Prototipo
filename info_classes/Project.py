
class Proj:
    def __init__(self, id : int, costAnalysis : int, costAccomp : int,theme: int, nProm : str, currentPhase : int, analysis_tech : int = None, other_tech : int = None):
        self.id = id
        self.costAnalysis = costAnalysis
        self.costAccomp = costAccomp
        self.theme = theme
        self.nProm = nProm
        self.currentPhase = currentPhase
        self.analysis_tech = analysis_tech 
        self.other_tech = other_tech 

    def __str__(self):
        return f"{self.id} - {self.theme} (tema): cost {self.costAccomp} / {self.nProm} (num prom) and {self.currentPhase} (currentPhase) "
    
    def convert_to_dict(self):
        return self.__dict__
    
    

