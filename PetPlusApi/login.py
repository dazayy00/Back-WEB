from fastapi import FastAPI, HTTPException
from database import login, get_admin_by_matricula
from models import Login, Admin

app = FastAPI()


@app.post("/login", response_model=Admin)
async def login_user(login_data: Login):
    db_admin = await login(login_data.Matricula, login_data.password)

    if not db_admin:
        raise HTTPException(status_code=400, detail="Invalid Matricula or password")

    admin = Admin(**db_admin)
    return admin
