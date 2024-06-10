from fastapi import APIRouter, HTTPException
from models import Login, Admin
from database import get_admin_by_matricula

router = APIRouter()

@router.post("/", response_model=Admin)
async def login_user(login_data: Login):
    db_admin = await get_admin_by_matricula(login_data.Matricula)

    if not db_admin:
        raise HTTPException(status_code=400, detail="Invalid Matricula")

    admin = Admin(**db_admin)
    return admin
