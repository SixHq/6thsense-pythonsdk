from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.types import ASGIApp, Message
from fastapi import FastAPI, Request
from starlette.concurrency import iterate_in_threadpool
import ast
from dotenv import load_dotenv
import os
import requests
from sixth.utils import encryption_utils
import copy
import json
from fastapi import Response, Header
from sixth.middlewares.six_base_http_middleware import SixBaseHTTPMiddleware
from fastapi import HTTPException
load_dotenv()


class EncryptionMiddleware(SixBaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, apikey: str, fastapi_app: FastAPI):
        super().__init__(app)
        self._app = app
        self._apikey = apikey
    async def set_body(self, request: Request, body: bytes):
        async def receive() -> Message:
            return {'type': 'http.request', 'body': body}
        request._receive = receive

    async def _parse_bools(self, string: bytes)-> str:
        string = string.decode("utf-8")
        string = string.replace(' ', "")
        string = string.replace('true,', "True,")
        string = string.replace(",true", "True,")
        string = string.replace('false,', "False,")
        string = string.replace(",false", "False,")
        out=ast.literal_eval(string)
        return out
    

    async def dispatch(self,request: Request,call_next) -> None:

        req_body = await request.body()
        await self.set_body(request, req_body)
        req_body =await self._parse_bools(req_body)
        private_key_request = requests.post("https://backend.withsix.co/encryption-service/get-user-private_key", data=json.dumps({
            "apiKey": self._apikey
        }))
        if private_key_request.status_code == 200:
            private_key_url = private_key_request.json()["data"]["private_key"]
            private_key_txt = requests.get(private_key_url)
            data = private_key_txt.text
            if type(req_body) == str:
                req_body = eval(req_body)
            output = copy.deepcopy(req_body)
            try:
                await encryption_utils.post_order_decrypt(data, None, req_body, output)
                output = json.dumps(output)
                headers = dict(request.headers)
                headers["content-length"]= str(len(output.encode()))
            except Exception as e:
                raise HTTPException(401, {"Unauthorized":e})
            

        response = await call_next(200, output, headers)
        resp_body = response.body
        resp_body = await self._parse_bools(resp_body)
        public_key_request = requests.post("https://backend.withsix.co/encryption-service/get-user-public-key", data=json.dumps({
            "apiKey": self._apikey
        }))
        if public_key_request.status_code == 200:
            public_key_url = public_key_request.json()["data"]["public_key"]
            public_key_txt = requests.get(public_key_url)
            data = public_key_txt.text
            if type(resp_body) == str:
                resp_body = eval(resp_body)
            output = copy.deepcopy(resp_body)
            try:
                await encryption_utils.post_order_encrypt(data, None, resp_body, output)
                output = json.dumps(output)
                response.headers["content-length"]= str(len(output.encode()))
                return Response(
                    content=output, 
                    headers=response.headers,
                    media_type=response.media_type, 
                    background=response.background
                )
                
            except Exception as e:
                raise HTTPException(401, {"Unauthorized":e})