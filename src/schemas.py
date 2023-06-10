from pydantic import BaseModel,validator,EmailStr
from typing import List, Optional, Dict


class RateLimiter(BaseModel):
    id: str
    route: str
    interval: int 
    rate_limit: int
    last_updated: float 
    created_at: float
    unique_id: str = "host"

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
    last_updated: float
    created_at: float