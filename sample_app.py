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

app=FastAPI()


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

@app.get("/ope")
@version(1)
async def new(request:Request):
    return request.headers

@app.post("/testing")
@version(1)
async def news(request: Request, schema:TestSchema):
    body = schema.dict()
    return body

Sixth("YVawS7tr1SaBmeG4NVZt3OniEw52", app).init()
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)