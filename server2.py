from fastapi import FastAPI
from input.inputAPI import Connection_BD
from input.inputAPI import read_input_api


inputURL = 'https://ani-fake-api.onrender.com'

# Here we also write to BD
bd = read_input_api(url=inputURL)


app = FastAPI()

@app.get("/a")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def root():
    print("AQUI")
    areas = bd.do_command("Select * from T_Tecnico  ")
    print(areas)
    return {"message": areas}