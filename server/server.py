# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
import json 
from urllib.parse import urlparse
from info_classes.Project import Proj
from info_classes.Tech import Tech
from urllib.parse import unquote

hostName = "localhost"
serverPort = 7999

def get_attributions_from_input(projs : list[Proj], input_translations):
        tasks_costs_relative_to_tecn : dict= {}
        attributions = {}
        for proj in projs:
            proj_name = input_translations["projs"][proj.id]
            # Check analysis
            if proj.analysis_tech != None:
                tecn_name = input_translations["tecns"][proj.analysis_tech]
                proj_name_analysis = f"{proj_name}-Análise"
                tasks_costs_relative_to_tecn[proj_name_analysis] = proj.costAnalysis
                if tecn_name not in attributions:
                    attributions[tecn_name] = []
                attributions[tecn_name].append(proj_name_analysis)
            if proj.other_tech != None:
                tecn_name = input_translations["tecns"][proj.other_tech]
                proj_name_accomp = f"{proj_name}-Acompanhamento"
                tasks_costs_relative_to_tecn[proj_name_accomp] = proj.costAccomp
                if tecn_name not in attributions:
                    attributions[tecn_name] = []
                attributions[tecn_name].append(proj_name_accomp)
        return (tasks_costs_relative_to_tecn, attributions)

    

class MyServer(BaseHTTPRequestHandler):
    def __init__(self, tecns : list[Tech], projs : list[Proj], compabilities, input_translations, *args, **kwargs):
        self.tecns = tecns
        self.projs = projs
        self.compabilities = compabilities
        self.translations = input_translations
        self.attributions = {}
        (tasks_costs, attributions_name_techn) = get_attributions_from_input(projs=projs, input_translations=input_translations)
        self.attributions["tasks_costs_relative_to_tecn"] = tasks_costs
        self.attributions["technicians"] = attributions_name_techn
        # BaseHTTPRequestHandler calls do_GET **inside** __init__ !!!
        # So we have to call super().__init__ after setting attributes.
        super().__init__(*args, **kwargs)


    def get_tecn(self, tecn_name : str):

        clean_name = unquote(tecn_name)
        tecn_id = int(self.translations["tecns"].index(clean_name))
        tecn = list(filter(lambda tecn: tecn.id == tecn_id, self.tecns))
        if len(tecn) > 0:
            res = {}
            res["info"] = tecn[0].convert_to_dict()
            print("Prepare stuff")
            tecn_name = self.get_tecn_name_by_id(tecn_id=tecn_id)
            projs = self.attributions["technicians"][clean_name]
            for proj in projs:
                [proj_name, phase] = proj.split("-")
                print("\n\nProject: ")
                print(proj_name)
                print(phase)

                proj_id = int(self.translations["projs"].index(unquote(proj_name)))
                proj_info = list(filter(lambda this_proj: this_proj.id == proj_id, self.projs))[0]
                print(proj_info)

            return tecn[0].convert_to_dict()
        else: 
            # DEBUG, no project found
            print("No proj: ", tecn_id)
            for i in self.tecns:
                print(i.id)
            return {"ERROR": "NO TECN FOUND"}


    def get_proj(self, proj_name : str):
        proj_id = int(self.translations["projs"].index(unquote(proj_name)))
        
        proj = list(filter(lambda proj: proj.id == proj_id, self.projs))
        if len(proj) > 0:
            return proj[0].convert_to_dict()
        else: 
            # DEBUG, no project found
            print("No proj: ", proj_id)
            for i in self.projs:
                print(i.id)
            return {"ERROR": "NO PROJECT FOUND"}
    
    def get_proj_name_by_id(self, proj_id : int):
        return self.translations["projs"][proj_id]

    def get_tecn_name_by_id(self, tecn_id : int):
        return self.translations["tecns"][tecn_id]

    def get_attribution(self):
        print("GET attribution")
        
        return {"input": {
                "tasks" : self.attributions["tasks_costs_relative_to_tecn"],
                "technicians": self.attributions["technicians"]
            }
        } 


    def do_GET(self):
        print("Recebeu pedido ")
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        print(query_components)
        answer = {'hello': 'world', 'received': 'ok'}
        if "proj" in query_components:
            answer = self.get_proj(proj_name=query_components["proj"])
        elif "tecn" in query_components:
            answer = self.get_tecn(tecn_name=query_components["tecn"])
        elif "attri" in query_components:
            answer = self.get_attribution()
            print("ANSWER")
            print(answer)
        elif "removeTecn" in query_components:
            print("Remover técnico")
            print(unquote(query_components['removeTecn']))
        else:
            print("Not handled")
            print(query_components)
        

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps(answer).encode('utf-8'))
        

        #print(self.tecns)
        #print(self.projs)

def server_main(input):
    handler = partial(MyServer, input.excel_information.tecns, input.excel_information.tasks, input.excel_information.compatibilities, input.names_translations )
    webServer = HTTPServer((hostName, serverPort), handler)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
        
    except KeyboardInterrupt:
        webServer.server_close()
        print("Server stopped.")

    webServer.server_close()
    print("Server stopped.")