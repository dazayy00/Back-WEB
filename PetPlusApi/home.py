from fastapi import FastAPI, HTTPException
from models import Admin
from bson.objectid import ObjectId  
from database import get_one_admin_by_id

app = FastAPI()

#imprimir datos de admin
@app.get("/api/admins/{id}", response_model=Admin)
async def get_admin_by_id(id: str):
    admin = await get_one_admin_by_id(id)
    if admin:
        return admin
    else:
        raise HTTPException(status_code=404, detail=f"Admin with ID '{id}' not found")
    

