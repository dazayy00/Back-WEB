from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_all_admins, create_admin, get_one_admin_by_id, update, delete
from models import Admin
from login import router as login_router
from home import router as home_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(home_router, prefix="", tags=["home"])

@app.get('/api/admins', response_model=list[Admin]) 
async def get_admins():
    admins = await get_all_admins()
    return admins

@app.get('/api/admins/{id}', response_model=Admin)
async def get_admin_by_id(id: str):
    admin = await get_one_admin_by_id(id)
    if admin:
        return admin
    else:
        raise HTTPException(status_code=404, detail=f"Admin with ID '{id}' not found")

@app.post('/api/admins', response_model=Admin)
async def create_admin(admin: Admin):  
    response = await create_admin(admin)
    if response:
        return response
    raise HTTPException(status_code=400, detail="Error creating admin")

@app.put('/api/admins/{id}', response_model=Admin)
async def update_admin(id: str, admin_data: Admin):
    updated_admin = await update(id, admin_data.dict())
    if updated_admin:
        return updated_admin
    else:
        raise HTTPException(status_code=404, detail=f"Admin with ID '{id}' not found")

@app.delete('/api/admins/{id}', status_code=204)
async def delete_admin(id: str):
    deleted = await delete(id)
    if deleted:
        return None
    else:
        raise HTTPException(status_code=404, detail=f"Admin with ID '{id}' not found")
