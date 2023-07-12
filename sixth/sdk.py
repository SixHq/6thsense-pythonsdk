from fastapi import FastAPI, status, Depends
from sixth.middlewares.six_rate_limiter_middleware import SixRateLimiterMiddleware
from sixth.middlewares.encryption_middleware import EncryptionMiddleware
from sixth.middlewares.six_independent_rate_limiter import SixRateIndependentLimiterMiddleware
import requests
from dotenv import load_dotenv
from sixth import schemas
import os
from sixth.utils.time_utils import get_time_now
import json
import re
from pydantic.error_wrappers import ValidationError

load_dotenv()


class Sixth():
    def __init__(self, apikey: str, app: FastAPI):
        self._apikey = apikey
        self._app = app 

    def init(self):
        _base_url = "https://backend.withsix.co"
        _project_config_resp = requests.get(_base_url+"/project-config/config/"+self._apikey)
        # get the user's project config
        try:
            if _project_config_resp.status_code == 200:
                _config: schemas.ProjectConfig = schemas.ProjectConfig.parse_obj(dict(_project_config_resp.json()))
                self._sync_project_route(_config)
            else:
                _config = self._sync_project_route()
        except ValidationError as e:
            _config = self._sync_project_route()

        if (_config.encryption_enabled):
            self._app.add_middleware(EncryptionMiddleware, apikey= self._apikey, fastapi_app= self._app)
            self._app.add_middleware(SixRateLimiterMiddleware, apikey= self._apikey, fastapi_app= self._app, project_config=_config)
        else:
            self._app.add_middleware(SixRateLimiterMiddleware, apikey= self._apikey, fastapi_app= self._app, project_config=_config)
         
        
    def _sync_project_route(self, config: schemas.ProjectConfig = None)-> schemas.ProjectConfig:
        #sync the config with db
        _rl_configs = {}
        for route in self._app.router.routes:
            if type(route.app )== FastAPI:
                for new_route in route.app.routes:
                    path = "/v"+str(route.app.version)+new_route.path
                    edited_route = re.sub(r'\W+', '~', path)
                    if config and edited_route in config.rate_limiter.keys():
                        #default config has been set earlier on so skip
                        _rl_configs[edited_route] = config.rate_limiter[edited_route]
                        continue
                    #set the default values
                    _rl_config = schemas.RateLimiter(id = edited_route, route=edited_route, interval=60, rate_limit=10, last_updated=get_time_now(), created_at=get_time_now(), unique_id="host", rate_limit_type="ip address", is_active=False)
                    _rl_configs[edited_route] = _rl_config
            else:
                edited_route = re.sub(r'\W+', '~', route.path)
                if config and edited_route in config.rate_limiter.keys():
                        #default config has been set earlier on so skip
                        _rl_configs[edited_route] = config.rate_limiter[edited_route]
                        continue
                    #set the default values
                _rl_config = schemas.RateLimiter(id = edited_route, route=edited_route, interval=60, rate_limit=10, last_updated=get_time_now(), created_at=get_time_now(), unique_id="host", is_active=False)
                _rl_configs[edited_route] = _rl_config

        _config = schemas.ProjectConfig(
            user_id = self._apikey, 
            rate_limiter = _rl_configs, 
            encryption = schemas.Encryption(public_key="dummy",private_key="dummy", use_count=0, last_updated=0,created_at=0, is_active=False), 
            base_url = "project",
            last_updated=get_time_now(), 
            created_at=get_time_now(), 
            encryption_enabled=config.encryption_enabled if config != None else False, 
            rate_limiter_enabled=config.rate_limiter_enabled if config != None else True
        )
        _base_url = "https://backend.withsix.co"
        _project_config_resp = requests.post(_base_url+"/project-config/config/sync-user-config", json=_config.dict())
        if _project_config_resp.status_code == status.HTTP_200_OK:
            return _config
        else: 
            return _config


