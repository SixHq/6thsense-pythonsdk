from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from fastapi import FastAPI,Depends,Response,HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.datastructures import MutableHeaders
import time
import json
from sixth import schemas
import re
import requests
import pickledb
import ast


class SixRateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, apikey: str, fastapi_app: FastAPI, project_config: schemas.ProjectConfig):
        super().__init__(app)
        self._config = project_config
        self._log_dict = {}
        self._app = app
        self._apikey = apikey
        self._route_last_updated = {}
        self._rate_limit_logs_sent = {}
        self.db = pickledb.load(f'{apikey}_db.db', auto_dump=True)
        
        for route in fastapi_app.router.routes:
            if type(route.app) == FastAPI:
                for new_route in route.app.routes:
                    path = "/v"+str(route.app.version)+new_route.path
                    edited_route = re.sub(r'\W+', '~', path)
                    self._log_dict[str(edited_route)] = {}
                    self._route_last_updated[str(edited_route)] = time.time()
                    self._rate_limit_logs_sent[str(edited_route)] = 0
            else:
                edited_route = re.sub(r'\W+', '~', route.path)
                self._log_dict[str(edited_route)] = {}
                self._route_last_updated[str(edited_route)] = time.time()
                self._rate_limit_logs_sent[str(edited_route)] = 0                

    async def set_body(self, request: Request, body: bytes):
        async def receive() -> Message:
            return {'type': 'http.request', 'body': body}
        request._receive = receive
        
    def _is_rate_limit_reached(self, uid, route):
        rate_limit = self._config.rate_limiter[route].rate_limit
        interval = self._config.rate_limiter[route].interval
        body = {
            "route": route, 
            "interval": interval, 
            "rate_limit": rate_limit, 
            "unique_id": uid.replace(".","~"), 
            "user_id": self._apikey,
            "is_active":True
        }
        resp = requests.post("https://backend.withsix.co/rate-limit/enquire-has-reached-rate_limit", json=body)
        if resp.status_code == 200:
            body =  resp.json()
            return body["response"]
        else:
            return False

        
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
    
    async def _send_logs(self, route: str, header, body, query)-> None:
        timestamp = time.time()
        last_log_sent = self._rate_limit_logs_sent[route]
        if timestamp - last_log_sent > 10:
            requests.post("https://backend.withsix.co/slack/send_message_to_slack_user", json=schemas.SlackMessageSchema(
                header=header, 
                user_id=self._apikey, 
                body=str(body), 
                query_args=str(query), 
                timestamp=timestamp, 
                attack_type="No Rate Limit Attack", 
                cwe_link="https://cwe.mitre.org/data/definitions/770.html", 
                status="MITIGATED", 
                learn_more_link="https://en.wikipedia.org/wiki/Rate_limiting", 
                route=route
            ).dict())
            self._rate_limit_logs_sent[route]=timestamp
            

        
    async def dispatch(self,request: Request,call_next) -> None:
        host = request.client.host
        route = request.scope["path"]
        route = re.sub(r'\W+', '~', route)
        headers = request.headers
        query_params = request.query_params
        rate_limit_resp = None
        status_code = 200

        
        
        #fail safe if there is an internal server error our servers are currenly in maintnance
        try:
            update_time = time.time()
            if update_time - self._route_last_updated[route] >60:
                #update rate limit details every 60 seconds
                rate_limit_resp = requests.get("https://backend.withsix.co/project-config/config/get-route-rate-limit/"+self._apikey+"/"+route)
                self._route_last_updated[route] = update_time
                status_code = rate_limit_resp.status_code
            body = None

            try:
                body = await request.body()
                await self.set_body(request, body)
                body = await self._parse_bools(body)
            except:
                pass
            
            if status_code == 200: 
                try:
                    rate_limit = schemas.RateLimiter.model_validate(rate_limit_resp.json()) if rate_limit_resp != None else self._config.rate_limiter[route]
                    if rate_limit.is_active:
                        self._config.rate_limiter[route] = rate_limit
                        preferred_id = self._config.rate_limiter[route].unique_id
                    
                        if preferred_id == "" or preferred_id=="host":
                            preferred_id = host
                            
                        else:
                            if rate_limit.rate_limit_type == "body":
                                if body != None:
                                    preferred_id = body[preferred_id]
                                else:
                                    _response = await call_next(request)
                                    return _response
                            elif rate_limit.rate_limit_type == "header":
                                preferred_id = headers[preferred_id]
                            elif rate_limit.rate_limit_type == "args":
                                preferred_id = query_params[preferred_id]
                            else:
                                preferred_id = host
                        

                        if not self._is_rate_limit_reached(preferred_id, route): 
                            _response = await call_next(request)
                            return _response
                        else:
                            await self._send_logs(route=route, header=headers, body=body, query=query_params)
                            temp_payload = rate_limit.error_payload.values()
                            final = {}
                            for c in temp_payload:
                                for keys in c:
                                    if keys != "uid":
                                        final[keys] = c[keys]
                            output= final
                            headers = MutableHeaders(headers={"content-length": str(len(str(output).encode())), 'content-type': 'application/json'})
                            return Response(json.dumps(output), status_code=420, headers=headers)
                    else:
                        _response = await call_next(request)
                        return _response
                except Exception as e:
                    _response = await call_next(request)
                    return _response
            else:
                #fail safe if there is an internal server error our servers are currenly in maintnance
                _response = await call_next(request)
                return _response
        except Exception as e:
            _response = await call_next(request)
            return _response