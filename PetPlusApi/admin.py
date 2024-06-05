from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

app = FastAPI()

# MongoDB configuration
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.admins_db
admins_collection = database.get_collection("admins")

# Modelos de Pydantic
class AdminBase(BaseModel):
    nombre: str
    correo: str
    imagen: str

class AdminCreate(AdminBase):
    pass

class Admin(AdminBase):
    id: str

# Función auxiliar para convertir documento de MongoDB a modelo Pydantic
def admin_helper(admin) -> dict:
    return {
        "id": str(admin["_id"]),
        "nombre": admin["nombre"],
        "correo": admin["correo"],
        "imagen": admin["imagen"]
    }

# Obtener todos los admins
@app.get("/admins", response_model=List[Admin])
async def get_all_admins():
    admins = []
    async for admin in admins_collection.find():
        admins.append(admin_helper(admin))
    return admins

# Actualizar un admin
@app.put("/admins/{admin_id}", response_model=Admin)
async def update_admin(admin_id: str, admin_data: AdminCreate):
    if not ObjectId.is_valid(admin_id):
        raise HTTPException(status_code=400, detail="ID de admin no válido")

    update_result = await admins_collection.update_one(
        {"_id": ObjectId(admin_id)},
        {"$set": admin_data.dict()}
    )

    if update_result.modified_count == 1:
        updated_admin = await admins_collection.find_one({"_id": ObjectId(admin_id)})
        if updated_admin:
            return admin_helper(updated_admin)
    
    existing_admin = await admins_collection.find_one({"_id": ObjectId(admin_id)})
    if existing_admin:
        return admin_helper(existing_admin)

    raise HTTPException(status_code=404, detail="Admin no encontrado")

# Eliminar un admin
@app.delete("/admins/{admin_id}")
async def delete_admin(admin_id: str):
    if not ObjectId.is_valid(admin_id):
        raise HTTPException(status_code=400, detail="ID de admin no válido")

    delete_result = await admins_collection.delete_one({"_id": ObjectId(admin_id)})

    if delete_result.deleted_count == 1:
        return {"mensaje": "Admin eliminado"}
    
    raise HTTPException(status_code=404, detail="Admin no encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)