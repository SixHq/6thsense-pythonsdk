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

PORT = 5002

@app.get("/ope")
@version(1)
async def new(name: str, request:Request):
    return request.headers

@app.post("/testing")
@version(1)
async def news(request: Request, schema:TestSchema):
    body = schema.json()
    return body

@app.post("/users/resend_otp/")
@version(1)
async def news(request: Request):
    return {
        "message": "otp sent successfully"
    }

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

Sixth("4d512129ff7d5c53958d84e6c3be99f6", app).init()
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)