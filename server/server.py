# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json 

hostName = "localhost"
serverPort = 7999

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Recebeu pedido ")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode('utf-8'))

def server_main():
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")