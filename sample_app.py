from fastapi import FastAPI,Depends,Response,HTTPException, Request
import uvicorn
from sixth.sdk import SixthSense
import json
import time
from typing import Optional, Dict, Union, Type, Callable
from fastapi_versioning import VersionedFastAPI, version
from starlette.routing import Mount


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

@app.get("/")
@version(1)
async def new(request:Request):
    return request.headers

@app.post("/tessting")
@version(1)
async def news(request: Request):
    return {"test": "test"}

app = VersionedFastAPI(
        app,
        version_format="{major}",
        prefix_format="/v{major}"
)

SixthSense(apikey="YVawS7tr1SaBmeG4NVZt3OniEw52", app=app).init()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5001)