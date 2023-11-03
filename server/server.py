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

class MyServer(BaseHTTPRequestHandler):
    def __init__(self, tecns : list[Tech], projs : list[Proj], attribution, compabilities, input_translations, *args, **kwargs):
        self.tecns = tecns
        self.projs = projs
        self.attribution = attribution
        self.compabilities = compabilities
        self.translations = input_translations
        # BaseHTTPRequestHandler calls do_GET **inside** __init__ !!!
        # So we have to call super().__init__ after setting attributes.
        super().__init__(*args, **kwargs)
    
    def get_tecn(self, tecn_name : str):

        print("Before error")
        print(tecn_name)
        print(self.translations["tecns"])
        tecn_id = int(self.translations["tecns"].index(unquote(tecn_name)))
        tecn = list(filter(lambda tecn: tecn.id == tecn_id, self.tecns))
        if len(tecn) > 0:
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
        print("Error")
        print(self.translations["projs"])
        print(proj_id)
        return self.translations["projs"][proj_id]
    def get_tecn_name_by_id(self, tecn_id : int):
        return self.translations["tecns"][tecn_id]

    # We got numbers 0, in input there is no 0
    def get_attribution(self):
        tasks_costs_relative_to_tecn : dict= {}
        attributions = {}
        for id_proj, tecn in enumerate(self.attribution):
            proj_name = self.get_proj_name_by_id(id_proj)
            tecn_name = self.get_tecn_name_by_id(tecn_id=tecn)
            # I confirmed, this is correct
            cost_this_project = self.compabilities[tecn][id_proj] * self.projs[id_proj].cost
            tasks_costs_relative_to_tecn[proj_name] = cost_this_project
            if tecn not in attributions:
                attributions[tecn_name] = []
            attributions[tecn_name].append(proj_name)
        return {"input": {
                "tasks" : tasks_costs_relative_to_tecn,
                "technicians": attributions
            }
        } 


    def do_GET(self):
        print("Recebeu pedido ")
        query = urlparse(self.path).query
        self.get_attribution()
        query_components = dict(qc.split("=") for qc in query.split("&"))
        print(query_components)
        answer = {'hello': 'world', 'received': 'ok'}
        if "proj" in query_components:
            answer = self.get_proj(proj_name=query_components["proj"])
        elif "tecn" in query_components:
            answer = self.get_tecn(tecn_name=query_components["tecn"])
        elif "attri" in query_components:
            answer = self.get_attribution()
        else:
            pass
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps(answer).encode('utf-8'))
        
 

        #print(self.tecns)
        #print(self.projs)

def server_main(input, atributtion):
    handler = partial(MyServer, input.excel_information.tecns, input.excel_information.tasks, atributtion, input.excel_information.compatibilities, input.names_translations )
    webServer = HTTPServer((hostName, serverPort), handler)
    print("Server started http://%s:%s" % (hostName, serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
        print("Server stopped.")

    webServer.server_close()
    print("Server stopped.")