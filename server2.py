from fastapi import FastAPI
from input.inputAPI import Connection_BD
from input.inputAPI import read_input_api
from serverQueries.getProjectsForCosts import get_Projects_For_Costs
from serverQueries.storeEfforts import store_efforts
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

 # uvicorn server2:app --reload --port 10000 
inputURL = 'https://ani-fake-api.onrender.com'

# Here we also write to BD
bd = read_input_api(url=inputURL)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/a")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def root():
    print("AQUI")
    areas = bd.do_command("Select * from T_Tecnico  ")
    print(areas)
    return {"message": areas}

# Get info of projects, so the user can change efforts of projects
# That info will be used for allocation 
# This should only send the projects that need alocation
@app.get("/proj_cost")
async def root():
    print("AQUI")
    projects = get_Projects_For_Costs(bd=bd)
    print(projects)
    return projects

# Used for confirmation, to frontend
class Project2(BaseModel):
    name2: str

class Project(BaseModel):
    area: str
    effort_accomp: int
    effort_analisis: int
    id: int
    name: str 
    topology: str

class ListProjects(BaseModel):
    projects: list[Project]

# When user changes efforts of projects. This could trigger allocation
# So the user doesn't has to wait for allocation
@app.put("/add_efforts", response_model=Project2)
async def add_efforts(projects : ListProjects):
    print("PUT")
    store_efforts(bd=bd, projects=projects.projects)
    return {"name2" : "ok"}
