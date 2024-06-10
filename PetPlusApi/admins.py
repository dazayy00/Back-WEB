from fastapi import FastAPI, HTTPException
from database import get_all_admins, get_one_admin_by_id
from models import Admin
from bson import ObjectId

app = FastAPI()

#codigo actualizado
#get de todos 
@app.get('/api/admins', response_model=list[Admin]) 
async def get_admins():
    admins = await get_all_admins()
    return admins

#get uno solo 
#manda a traer por el ObjectId de cada
@app.get('/api/admins/{id}', response_model=Admin)
async def get_admin_by_id(id: str):
    admin = await get_one_admin_by_id(id)
    if admin:
        return admin
    else:
        raise HTTPException(status_code=404, detail=f"Admin with ID '{id}' not found")