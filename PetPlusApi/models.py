from pydantic import BaseModel

class AdminLogin(BaseModel):
    matricula: str
    password: str
