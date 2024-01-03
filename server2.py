from fastapi import FastAPI

import nain

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

print("Hello from server2?")