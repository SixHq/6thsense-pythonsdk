from fastapi import FastAPI,Depends,Response,HTTPException, Request
import uvicorn
import json
import time
from typing import Optional, Dict, Union, Type, Callable
from fastapi_versioning import VersionedFastAPI, version
from starlette.routing import Mount
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pyngrok import ngrok
from sixth.sdk import Sixth
import uuid
from pydantic import BaseModel
public_url = ngrok.connect(9126).public_url
print(public_url)

app=FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def version_app(
    app: FastAPI,
    exception_handlers: Optional[Dict[Union[int, Type[Exception]], Callable]] = {},
    **kwargs,
):
    app = VersionedFastAPI(
        app,
        version_format="{major}",
        prefix_format="/v{major}"
    )
    return app

origins = ['*']


class TestSchema(BaseModel):
    user_id: str

PORT = 5001

@app.get("/")
@version(1)
async def new(request:Request):
    return request.headers

@app.post("/tessting")
@version(1)
async def news(request: Request, schema:TestSchema):
    time.sleep(10)
    body = schema.dict()
    return body

@app.get("/new", response_class=HTMLResponse)
async def cors(request: Request):
    print(uuid.uuid4())
    return templates.TemplateResponse("index.html", {"request": request})



Sixth("4d512129ff7d5c53958d84e6c3be99f6", app).init()
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)