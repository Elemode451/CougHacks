from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "I have a secret for you 🥺🥺🥺🥺"}


@app.get("/get")
async def function():
    return {"FastAPI": "FASTAPIIII"}


@app.get("/chatrooms/{slug}/messages"):
async def getMessages():
    return {"Skibidi Toilet": "dop dop"}