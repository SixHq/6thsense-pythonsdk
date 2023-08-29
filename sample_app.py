from fastapi import FastAPI,Depends,Response,HTTPException, Request
import uvicorn
from typing import Optional, Dict, Union, Type, Callable
from fastapi_versioning import VersionedFastAPI, version
from sixth.sdk import Sixth
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

otp = "1234"

@app.get("/ope")
async def new(name: str, request:Request):
    return request.headers

@app.post("/testing")
async def news(request: Request, schema:TestSchema):
    body = schema.json()
    return body

@app.post("/users/resend_otp/")
@version(1)
async def send_otp(request: Request):
    return {
        "data": {
            "message": [1, 2, 3, 4, 5], 
            "new": "ope"
        }
    }

@app.post("/users/send_otp/")
@version(1)
async def send_otp(request: Request):
    return {
        "message": "otp sent successfully"
    }

@app.get("/users/verify/")
@version(1)
async def verify_otp(email: str, otp: str):
    if email != "" and email != None and otp == "0100":
        print("""
        -------------------------------
              We have been hacked
        -------------------------------      

    """)
        return {
            "message": "Account has been verified"
        }
    else:
        return {
            "message": "Wrong OTP"
        }
    


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/newsss_items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

Sixth("YVawS7tr1SaBmeG4NVZt3OniEw52", app).init()
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=PORT)