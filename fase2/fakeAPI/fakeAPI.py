# To run: uvicorn fakeAPI:app --reload --port 1234
# To test: http://127.0.0.1:1234/projs on browser

from fastapi import FastAPI
import json
app = FastAPI()

def read_json_file(path : str):
    f = open(path)
 
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    f.close()
    return data

@app.get("/tecns")
async def root():
    return read_json_file("./JSON_tecns.json")

@app.get("/projs")
async def root():
    return read_json_file("./JSON_proj.json")

@app.get("/proms")
async def root():
    return read_json_file("./JSON_prom.json")
'''
Using this site: https://json-generator.com/

JSON Tecn:
[
  '{{repeat(5, 7)}}',
  {
    ID: '{{index()}}',
    Nome: '{{firstName()}} {{surname()}}',
    Data_vinculo: '{{date(new Date(2014, 0, 1), new Date(), "dd-MM-YYYYZ")}}'
  }
]


JSON_Project:
[
  '{{repeat(5, 10)}}',
  {
    ID: '{{index()}}',
   Sigla : '{{lorem(1, "words")}}',
    Nome : '{{lorem(3, "words")}}',
    Tipologia: '{{random("Copromoção", "Individual", "Mobilizador")}}', 

    Area: '{{random("A1", "B1", "C1")}}',
    Data_inicio: '{{date(new Date(2014, 0, 1), new Date(), "dd-MM-YYYYZ")}}',
    Data_fim: '{{date(new Date(2014, 0, 1), new Date(), "dd-MM-YYYYZ")}}', // DD/MM/AAAA
    ID_Promotores: [
      '{{repeat(1,5)}}',
        '{{integer(10, 50)}}'
          ],
    Area_Tematica: '{{random("A", "B", "C")}}',


    Tec_analise: '{{integer(0, 6)}}', 
    Tec_acompanhamento: '{{integer(0, 6)}}'
  }
]


JSON Promotores
[
  '{{repeat(5, 10)}}',
  {
    ID: '{{index()}}',
    Nome : '{{lorem(3, "words")}}',
    NIPC: '{{integer(111111111, 999999999)}}',
    Representante: '{{lorem(1, "words")}}', 
    Contato: '{{integer(111111111, 999999999)}}',

  }
]

'''
