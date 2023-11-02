
class Tech:
    def __init__(self, service_year : int, id : int):
        self.sevice_year = service_year
        self.id = id

    def __str__(self):
        return f"{self.id}: {self.sevice_year} "

    def convert_to_dict(self):
        return self.__dict__
    
    
