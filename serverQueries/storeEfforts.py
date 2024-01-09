

def store_efforts(bd, projects):
    for project in projects:
        bd.do_command(f"update T_PROJETO set Esf_Prev_Acompanhamento = {project.effort_accomp}, Esf_Prev_Analise = {project.effort_analisis} where Id_Projeto={project.id} ")
