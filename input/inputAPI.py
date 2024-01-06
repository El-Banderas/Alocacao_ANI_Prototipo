import requests
import json

from info_classes.Project import Proj
from info_classes.Tech import Tech

def convert_area_name_to_int(name : str):
    if name=="AGRO/BIO/QUI":
        return 1
    if name=="TIC/INST":
        return 2
    if name=="MAT/MEC/ENER/CONST":
        return 3
    print("Strange value: ", name)
    Exception("OLÀ")

def convert_phase_name_to_int(name : str):
    if name=="AGRO/BIO/QUI":
        return 1
    if name=="TIC/INST":
        return 2
    if name=="MAT/MEC/ENER/CONST":
        return 3
    print("Strange value: ", name)
    Exception("OLÀ")
  
class InputAPI:
    def __init__(self, list_tecns : list[Tech], list_projs: list[Proj]) -> None:
        self.list_tecns=list_tecns
        self.list_projs=list_projs

def read_input_api(url : str) -> InputAPI:
    x = requests.get(f'{url}/tecns')
    response = x.json()
    list_tecns : list[Tech] = [] 
    list_projs : list[Proj] = [] 
    for tecn in response:
        new_tecn = Tech(service_year=1, id=tecn["ID"], availability=1, current_effort=0, name=tecn["Nome"])
        list_tecns.append(new_tecn)

    x = requests.get(f'{url}/projs')
    response = x.json()
    for proj in response:

        new_proj = Proj(id=proj["ID"], costAnalysis=-1, costAccomp=-1, 
                        theme=convert_area_name_to_int(proj["Area_Tematica"]),
                        nProm=proj["Tipologia"], currentPhase=0, analysis_tech=proj["Tec_analise"],
                        other_tech=proj["Tec_acompanhamento"]
                                                       )
        new_proj.addDates(init_date=proj["Data_inicio"], end_date=proj["Data_fim"])    
        new_proj.add_name(name=proj["Nome"])    
        list_projs.append(new_proj)
    join_stuff = InputAPI(list_projs=list_projs, list_tecns=list_tecns)
    return join_stuff