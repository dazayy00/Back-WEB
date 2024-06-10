from fastapi import FastAPI, HTTPException
from database import get_admin_by_matricula
from models import Login, Admin

app = FastAPI()

@app.post("/login", response_model=Admin)
async def login_user(login_data: Login):
    db_admin = await get_admin_by_matricula(login_data.Matricula)

    if not db_admin:
        raise HTTPException(status_code=400, detail="Invalid Matricula")

    admin = Admin(**db_admin)
    return admin
