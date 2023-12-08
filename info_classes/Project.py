
class Proj:
    def __init__(self, id : int, cost : int, theme: int, nProm : str, currentPhase : int, analysis_tech : int = None, other_tech : int = None):
        self.id = id
        self.cost = cost
        self.theme = theme
        self.nProm = nProm
        self.currentPhase = currentPhase
        self.analysis_tech = analysis_tech 
        self.other_tech = other_tech 

    def __str__(self):
        return f"{self.id} - {self.theme} (tema): cost {self.cost} / {self.nProm} (num prom) and {self.currentPhase} (currentPhase) "
    
    def convert_to_dict(self):
        return self.__dict__
    
    

