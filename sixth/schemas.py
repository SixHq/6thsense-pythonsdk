from pydantic import BaseModel
from typing import List, Optional, Dict, Union
import uuid


class RateLimiter(BaseModel): 
    error_payload_id: str = str(uuid.uuid4())
    id: str
    route: str
    interval: Union[float, int, str]
    rate_limit: int
    last_updated: float 
    created_at: float
    rate_limit_type: str = "ip address" #ip address, header, body, query_param
    unique_id: str = "host"
    error_payload: Dict[str , dict] = {
        error_payload_id:{
            "message": "max_limit_request_reached", 
            "uid": error_payload_id
        }
    }
    is_active:bool

class Encryption(BaseModel):
    public_key: str 
    private_key: str 
    use_count: int
    last_updated: float
    created_at: float

class ProjectConfig(BaseModel):
    user_id: str
    rate_limiter: Dict[str, RateLimiter]
    encryption: Encryption
    base_url: str 
    encryption_enabled: bool
    rate_limiter_enabled: bool
    last_updated: float
    created_at: float

class SlackMessageSchema(BaseModel):
    header:dict
    user_id:str
    body:object
    query_args: object = None
    timestamp: float 
    attack_type: str
    cwe_link: str
    status: str 
    learn_more_link: str    
    route: str