import requests
import json
import sqlite3

from info_classes.Project import Proj
from info_classes.Tech import Tech

from input.handleDB import clean_old_tables, create_tables, insert_basics

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
  
class Connection_BD:
    def __init__(self ) -> None:
        conn = sqlite3.connect('./BD/ANI_DB.db')
        cur = conn.cursor()
        self.cur = cur
        self.conn = conn
        rows = self.do_command("SELECT * FROM T_TECNICO")
        for row in rows:
            print(row)
        print("Start writing default stuff")
        for drop in clean_old_tables:
            self.do_command(drop)
        print("[DONE] Delete  old")
        for create in create_tables:
            self.do_command(create)
        print("[DONE] Create newld")
        for insert in insert_basics:
            self.do_command(insert)
        print("[DONE] Insert info")
        answer = self.do_command("Select * from T_AREA_TEMATICA ")
        print(answer)

    def do_command(self, instruction : str):
        try:
            self.cur.execute(instruction)
            rows = self.cur.fetchall()
            return rows
        finally:
            self.conn.commit()
        


def read_input_api(url : str) :
    connection = Connection_BD()
    exit(0)        

    x = requests.get(f'{url}/tecns')
    response = x.json()
    list_tecns : list[Tech] = [] 
    list_projs : list[Proj] = [] 
    for tecn in response:
        new_tecn = Tech(service_year=1, id=tecn["ID"], availability=1, current_effort=0)
        list_tecns.append(new_tecn)

    x = requests.get(f'{url}/projs')
    response = x.json()
    for proj in response:

        new_proj = Proj(id=proj["ID"], costAnalysis=-1, costAccomp=-1, 
                        theme=convert_area_name_to_int(proj["Area_Tematica"]),
                        nProm=proj["Tipologia"], currentPhase=0, analysis_tech=proj["Tec_analise"],
                        other_tech=proj["Tec_acompanhamento"]
                                                       )
        list_projs.append(new_proj)
    join_stuff = InputAPI(list_projs=list_projs, list_tecns=list_tecns)
    return join_stuff