from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from sixth import schemas
from fastapi import FastAPI
from starlette.types import ASGIApp, Message
from fastapi import FastAPI, Request
import requests
import ast
import time
import re
from typing import List
from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import PlainTextResponse, Response
import json


class SixSecureLogsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, apikey: str, fastapi_app: FastAPI, secure_logs: List[schemas.SecureLogMessage]):
        super().__init__(app)
        self._secure_logs = secure_logs
        self._logs_sent = {}
        self._apikey=apikey
        self._last_updated_logs_config = 0
        for route in fastapi_app.router.routes:
            if type(route.app) == FastAPI:
                for new_route in route.app.routes:
                    path = "/v"+str(route.app.version)+new_route.path
                    edited_route = re.sub(r'\W+', '~', path)
                    self._logs_sent[str(edited_route)] = 0
            else:
                edited_route = re.sub(r'\W+', '~', route.path)
                self._logs_sent[str(edited_route)] = 0          

    async def set_body(self, request: Request, body: bytes):
        async def receive() -> Message:
            return {'type': 'http.request', 'body': body}
        request._receive = receive

    async def _parse_bools(self, string: bytes)-> str:
        '''
            used  to parse boolean values in string format and convert it to Python's boolean format
        '''
        string = string.decode("utf-8")
        string = string.replace(' ', "")
        string = string.replace('true,', "True,")
        string = string.replace(",true", "True,")
        string = string.replace('false,', "False,")
        string = string.replace(",false", "False,")
        out=ast.literal_eval(string)
        return out
    
    async def _send_logs(self, route: str, header, body, query, value, type)-> None:
        timestamp = time.time()
        last_log_sent = self._logs_sent[route]
        if timestamp - last_log_sent > 5:
            requests.post("https://backend.withsix.co/slack/send_secure_log_to_slack_user", json=schemas.SecureLogMessage(
                header=header, 
                user_id=self._apikey, 
                body=str(body), 
                query_args=str(query), 
                timestamp=timestamp, 
                route=route, 
                value=value, 
                type=type,
            ).dict())
            self._logs_sent[route]=timestamp

    async def _config_secure_log(self):
        update_time = time.time()
        if update_time - self._last_updated_logs_config >10:
            url = "https://backend.withsix.co/secure-monitoring/get-all-secure-log?apikey="+self._apikey
            secure_log_resp = requests.get(url)
            secure_log_resp_body = secure_log_resp.json()
            secure_log_resp_data = secure_log_resp_body["data"]
            self._secure_logs = secure_log_resp_data
            self._last_updated_logs_config = update_time

    async def _get_log_type(value, type):
        if type == "str":
            return str(value)
        if type == "float":
            return float(value)
        if type == "int":
            return int(value)
        if type == "dict":
            return eval(value)
        if type == "list":
            return ast.literal_eval(value)


    async def dispatch(self,request: Request,call_next) -> None:
        await self._config_secure_log()
        route = request.scope["path"]
        route = re.sub(r'\W+', '~', route)
        headers = request.headers
        query_params = request.query_params
        body = None
        
        try:
            body = await request.body()
            await self.set_body(request, body)
            body = await self._parse_bools(body)
        except:
            pass
        secure_log: schemas.SecureLog = None 
        for log in self._secure_logs:
            if log.get("route", "") == route:
                secure_log = log

        _response = await call_next(request)
        
        if secure_log == None or secure_log["is_active"] == False:
            return _response
        response_body = b"".join([part async for part in _response.body_iterator])
        response_body = response_body.decode("utf-8")
       
        #special instances to carter for dictionary and list
        if secure_log["type"] != "dict" and secure_log["type"] != "list":
            # Get the response body content from the custom property
            if secure_log["value"] in response_body or secure_log["value"] in _response.headers.values():
                await self._send_logs(route, headers, body, query_params, secure_log["value"], secure_log["type"])
        else:
            modified_body = response_body.replace("'",'"').replace(" ", "")
            modified_value = str(secure_log["value"]).replace("'", '"').replace(" ", "")

            if modified_value in modified_body or modified_value in _response.headers.values():
                await self._send_logs(route, headers, body, query_params, secure_log["value"], secure_log["type"])

        output = response_body
        headers = MutableHeaders(headers={"content-length": str(len(str(output).encode())), 'content-type': 'application/json'})
        return Response(output, status_code=200, headers=headers)