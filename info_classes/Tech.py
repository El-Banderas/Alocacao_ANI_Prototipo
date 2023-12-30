
class Tech:
    def __init__(self, service_year : int, id : int, availability  : int, current_effort : float, name : str):
        self.sevice_year = service_year
        self.id = id
        self.availability = availability 
        self.current_effort  = current_effort  
        self.name = name

    def __str__(self):
        return f"Técnico {self.name} ( id {self.id}): {self.sevice_year} "

    def convert_to_dict(self):
        return self.__dict__

    def convert_to_dict_pt(self):

        dict_res = {}
        dict_res["id"] = self.id
        dict_res["Disponível"] = self.availability
        dict_res["Esforço atual"] = int(self.current_effort)
        return dict_res
    
    
