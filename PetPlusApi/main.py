from fastapi import FastAPI, HTTPException
from database import get_all_admins, create_admin, get_one_admin_by_id, update, delete
from models import Admin
from bson import ObjectId


app = FastAPI()

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

#post de admin
@app.post('/api/admins', response_model=Admin)
async def create_admin(admin: Admin):  
    response = await create_admin(admin) #linea de error post 
    if response:
        return response
    raise HTTPException(status_code=400, detail="Error creating admin")



#update de admin
@app.put('/api/admins/{id}', response_model=Admin)
async def update_admin(id: str, admin_data: Admin):
    updated_admin = await update(id, admin_data.dict())
    if updated_admin:
        return updated_admin
    else:
        raise HTTPException(status_code=404, detail=f"Admin with ID '{id}' not found")


#delete de admin 
@app.delete('/api/admins/{id}', status_code=204)
async def delete_admin(id: str):
    deleted = await delete(id)
    if deleted:
        return None
    else:
        raise HTTPException(status_code=404, detail=f"Admin with ID '{id}' not found")



