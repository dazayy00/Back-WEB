from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

class Admin(BaseModel):
    matricula: str
    nombre: str
    apellido: str
    edad: str
    turno: str

def admin_helper(admin) -> dict:
    return {
        "matricula": admin["Matricula"],
        "nombre": admin["Nombre"],
        "apellido": admin["Apellido"],
        "edad": admin["Edad"],
        "turno": admin["Turno"]
    }

from motor.motor_asyncio import AsyncIOMotorClient
MONGO_URI = "mongodb+srv://dazayy:pononoinuv@adminpp.dywe5yc.mongodb.net/?retryWrites=true&w=majority&appName=AdminPP"
client = AsyncIOMotorClient(MONGO_URI)
admins_collection = client["AdminPP"]["administrador"]

app = FastAPI()

# Obtener todos los admins
@app.get("/admins", response_model=List[Admin])
async def get_all_admins():
    admins = []
    async for admin in admins_collection.find():
        admins.append(admin_helper(admin))
    return admins

# Obtener un admin por ID cuando muestre datos generales del admin
@app.get("/admins/{id}", response_model=Admin)
async def get_admin_by_id(id: str):
    admin = await admins_collection.find_one({"_id": ObjectId(id)})
    if not admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")
    return admin_helper(admin)
