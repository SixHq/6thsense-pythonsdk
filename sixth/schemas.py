from pydantic import BaseModel
from typing import List, Optional, Dict
import uuid


class RateLimiter(BaseModel): 
    error_payload_id = str(uuid.uuid4())
    id: str
    route: str
    interval: int 
    rate_limit: int
    last_updated: float 
    created_at: float
    unique_id: str = "host"
    error_payload: Dict[str , dict] = {
        error_payload_id:{
            "message": "max_limit_request_reached", 
            "uid": error_payload_id
        }
    }

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