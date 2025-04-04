from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "TS Ashley PMO"}

