from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Configuración para el manejo de sesiones
app.add_middleware(SessionMiddleware, secret_key="my_secret_key")

# Templates para renderizar las vistas HTML opcional
templates = Jinja2Templates(directory="templates")

# Modelos de datos Pydantic
class Admin(BaseModel):
    name: str
    email: str
    picture: str

# Rutas
@app.get("/home")
async def home(request: Request):
    admin = request.session.get("admin")
    if not admin:
        return RedirectResponse(url="/login")

    return templates.TemplateResponse("home.html", {"request": request, "admin": admin})


@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login")
