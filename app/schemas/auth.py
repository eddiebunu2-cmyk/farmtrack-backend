from pydantic import BaseModel

class LoginRequest(BaseModel):
    phone: str
    pin: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    name: str