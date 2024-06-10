from fastapi import APIRouter, HTTPException
from database import get_admin_by_matricula
from models import Admin

router = APIRouter()

@router.get("/admin")
async def get_admin_data(matricula: str):
    db_admin = await get_admin_by_matricula(matricula)

    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")

    admin = Admin(**db_admin)

    return admin
