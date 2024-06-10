from pydantic import BaseModel

class Admin(BaseModel):
    Matricula: str
    Nombre: str
    Apellido: str
    Edad: str
    Turno: str
    Correo: str
    Imagen: str

class Login(BaseModel):
    Matricula: str  

