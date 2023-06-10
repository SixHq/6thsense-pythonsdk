from fastapi import FastAPI,Depends,Response,HTTPException, Request
import uvicorn
from src.six import Six
import json
import time


app=FastAPI()

origins = ['*']

@app.get("/")
async def new(request:Request):
    return request.headers

@app.post("/opeistesting")
async def news(request: Request):
    body = await request.json()
    return json.dumps(body)

@app.post("/finaltesting")
async def news(request: Request):
    return {"working": "working"}

Six(apikey="4d512129ff7d5c53958d84e6c3be99f6", app=app).init()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5001)