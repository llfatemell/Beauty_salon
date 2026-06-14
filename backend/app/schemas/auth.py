from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str  
    password: str
    role: str = "customer"  

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[int] = None
    role: Optional[str] = None
    access_token: Optional[str] = None
    token_type: str = "bearer"