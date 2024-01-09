from fastapi import FastAPI
from input.inputAPI import Connection_BD
from input.inputAPI import read_input_api

 # uvicorn fakeAPI:app --reload --port 10000 --host 0.0.0.0
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

@app.get("/proj_cost")
async def root():
    print("AQUI")
    projects = bd.do_command("Select * from T_PROJETO  ")
    print(projects)
    return {"message": projects}