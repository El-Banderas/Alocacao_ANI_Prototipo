import requests
import json
import sqlite3

from info_classes.Project import Proj
from info_classes.Tech import Tech

from input.handleDB import clean_old_tables, create_tables, insert_basics

def convert_acr_to_full(name : str) -> tuple[str, str]:
    if name=="AGRO/BIO/QUI":
        return (1, "'Agricultura / Biologia / Quimica'")
    if name=="TIC/INST":
        return (2, 'Tecnologias da Informação e Comunicação')
    if name=="MAT/MEC/ENER/CONST":
        return (3,'Materiais / Mecânica / Energia / Construção')
    print("[1] Strange value: ", name)
    Exception("OLÀ")


def convert_tipology_name_to_int(name : str):
    if name == "Copromoção":
        return 1
    if name=="Individual":
        return 2
    if name=="Mobilizador":
        return 3
    print("[2] Strange value: ", name)
    Exception("OLÀ")
  
class Connection_BD:
    def __init__(self ) -> None:
        conn = sqlite3.connect('./BD/ANI_DB.db')
        cur = conn.cursor()
        self.cur = cur
        self.conn = conn
        
        # Delete old and create new tables ?
        for drop in clean_old_tables:
            self.do_command(drop)
        for create in create_tables:
            self.do_command(create)
        


    def do_command(self, instruction : str):
        try:
            self.cur.execute(instruction)
            rows = self.cur.fetchall()
            return rows
        finally:
            self.conn.commit()
        

def insert_tecns_info(url : str, connection : Connection_BD):
    x = requests.get(f'{url}/tecns')
    response = x.json()
    for tecn in response:
    #    new_tecn = Tech(service_year=1, id=tecn["ID"], availability=1, current_effort=0)
    #    list_tecns.append(new_tecn)
        connection.do_command(f"INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES({tecn["ID"]}, '{tecn["Nome"]}', '{tecn["Data_vinculo"]}');")

def insert_proms_info(url : str, connection : Connection_BD):
    x = requests.get(f'{url}/proms')
    response = x.json()
    print("Proms?")
    for prom in response:
    #    new_tecn = Tech(service_year=1, id=tecn["ID"], availability=1, current_effort=0)
    #    list_tecns.append(new_tecn)
        print(prom)
        #connection.do_command(f"INSERT INTO T_TECNICO (Id_Tecnico, Nome, Data_Vinculo) VALUES({tecn["ID"]}, '{tecn["Nome"]}', '{tecn["Data_vinculo"]}');")
    exit(0)


def insert_projs_info(url : str, connection : Connection_BD):
    x = requests.get(f'{url}/projs')
    response = x.json()
    '''
    for proj in response:

        new_proj = Proj(id=proj["ID"], costAnalysis=-1, costAccomp=-1, 
                        theme=convert_area_name_to_int(proj["Area_Tematica"]),
                        nProm=proj["Tipologia"], currentPhase=0, analysis_tech=proj["Tec_analise"],
                        other_tech=proj["Tec_acompanhamento"]
                                                       )
        list_projs.append(new_proj)
    '''
    # Like "Copromoção" e "Mobilizador"
    unique_tipologies = set(map(lambda proj : proj["Tipologia"], response))
    # Like "Mat" and so on...
    unique_areas = set(map(lambda proj : proj["Area_Tematica"], response))

    # Insert tipologies and areas
    for area in unique_areas:
        id, full_name = convert_acr_to_full(name=area)
        connection.do_command(f"INSERT INTO T_AREA_TEMATICA VALUES({id}, '{area}', '{full_name}');")
        #connection.do_command(f"INSERT INTO T_AREA_TEMATICA VALUES(1, 'AGRO/BIO/QUI', 'Agricultura / Biologia / Quimica');")

    for type in unique_tipologies:
        id = convert_tipology_name_to_int(name=type)
        connection.do_command(f"INSERT INTO T_TIPOLOGIA VALUES({id}, '{type}');")
    
    for proj in response:
        id_area, _ignore = convert_acr_to_full(name=proj["Area_Tematica"])
        connection.do_command(f"""
INSERT INTO T_PROJETO (Id_Projeto, Sigla_Projeto, Nome, Id_Tipologia, Id_Fase, Id_Area, Data_Inicio, Data_Fim, Esf_Prev_Analise, Esf_Prev_Acompanhamento)
			VALUES({proj["ID"]}, '{proj["Sigla"]}', '{proj["Nome"]}', {convert_tipology_name_to_int(name=proj["Tipologia"])}, 
                    0, {id_area} , '{proj["Data_inicio"]}', '{proj["Data_fim"]}', 10, 20);
                              """)



'''
When saving data, it is necessary do consider that the insertion of info in DB must consider dependencies.
Because of that, we start by getting all info, and insert data in smaller tables, like "Fase". 
'''
def read_input_api(url : str) :

    connection = Connection_BD()
    insert_tecns_info(url=url, connection=connection)
    insert_proms_info(url=url, connection=connection)
    insert_projs_info(url=url, connection=connection)

    print("Test projects stored")
    rows = connection.do_command("Select * from T_TECNICO")
    for row in rows:
        print(row)
    print("----")
    rows = connection.do_command("Select * from T_PROJETO")
    for row in rows:
        print(row)

    
def convert_area_name_to_int(name : str):
    if name=="AGRO/BIO/QUI":
        return 1
    if name=="TIC/INST":
        return 2
    if name=="MAT/MEC/ENER/CONST":
        return 3
    print("Strange value: ", name)
    Exception("OLÀ")

