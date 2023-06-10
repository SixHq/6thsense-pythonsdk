from fastapi import FastAPI, status, Depends
from src.middlewares.six_rate_limiter_middleware import SixRateLimiterMiddleware
from src.middlewares.encryption_middleware import EncryptionMiddleware
import requests
from dotenv import load_dotenv
from src import schemas
import os
from utils.time_utils import get_time_now
import json
import re

load_dotenv()


class Six():
    def __init__(self, apikey: str, app: FastAPI):
        self._apikey = apikey
        self._app = app 

    def init(self):
        _base_url = "https://backend.withsix.co"
        _project_config_resp = requests.get(_base_url+"/project-config/config/"+self._apikey)
        # get the user's project config
        if _project_config_resp.status_code == 200:
            _config: schemas.ProjectConfig = schemas.ProjectConfig.parse_obj(dict(_project_config_resp.json()))
            self._sync_project_route(_config)
        else:
            _config = self._sync_project_route()
        
        self._app.add_middleware(EncryptionMiddleware, apikey= self._apikey, fastapi_app= self._app)
        self._app.add_middleware(SixRateLimiterMiddleware, apikey= self._apikey, fastapi_app= self._app, project_config=_config)
         
        
    def _sync_project_route(self, config: schemas.ProjectConfig = None)-> schemas.ProjectConfig:
        #sync the config with db
        _rl_configs = {}
        for route in self._app.routes:
            new_route = re.sub(r'\W+', '~', route.path)
            if config and new_route in config.rate_limiter.keys():
                #default config has been set earlier on so skip
                _rl_configs[new_route] = config.rate_limiter[new_route]
                continue
            #set the default values
            _rl_config = schemas.RateLimiter(id = new_route, route=new_route, interval=60, rate_limit=10, last_updated=get_time_now(), created_at=get_time_now(), unique_id="host")
            _rl_configs[new_route] = _rl_config

        _config = schemas.ProjectConfig(
            user_id = self._apikey, 
            rate_limiter = _rl_configs, 
            encryption = schemas.Encryption(public_key="dummy",private_key="dummy", use_count=0, last_updated=0,created_at=0), 
            base_url = "op",
            last_updated=get_time_now(), 
            created_at=get_time_now()
        )
        _base_url = "https://backend.withsix.co"
        _project_config_resp = requests.post(_base_url+"/project-config/config/sync-user-config", json=_config.dict())
        if _project_config_resp.status_code == status.HTTP_200_OK:
            return True
        else: 
            return False


