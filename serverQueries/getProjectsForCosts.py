

def get_Projects_For_Costs(bd):
    projects_raw = bd.do_command("Select * from T_PROJETO  ")
    res = []
    for project in projects_raw:
        id, sigla, name, id_topo,id_fase, id_area, data_init, data_end, effort_analisis, effort_accomp = project
        area = bd.do_command(f"select Area from T_AREA_TEMATICA where Id_Area == {id_area} ")[0][0]
        tipo = bd.do_command(f"select Tipologia from T_TIPOLOGIA where Id_Tipologia == {id_topo}")[0][0]

        res.append({
            "id" : id,
            "name": name,
            "area" : area,
            "topology" : tipo,
            "effort_analisis" : effort_analisis,
            "effort_accomp" : effort_accomp,
        })
    return res
        

