from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

app = FastAPI()

# Configuración de MongoDB
DETALLES_MONGO = os.getenv("DETALLES_MONGO", "mongodb://localhost:27017")
cliente = AsyncIOMotorClient(DETALLES_MONGO)
base_de_datos = cliente.dispositivos_db
coleccion_dispositivos = base_de_datos.get_collection("dispositivos")

# Modelos de Pydantic
class DispositivoBase(BaseModel):
    id_dispositivo: str
    status: str
    id_dueno: str

class DispositivoCreate(DispositivoBase):
    pass

class Dispositivo(DispositivoBase):
    id: str

# Función auxiliar para convertir documento de MongoDB a modelo Pydantic
def dispositivo_helper(dispositivo) -> dict:
    return {
        "id": str(dispositivo["_id"]),
        "id_dispositivo": dispositivo["id_dispositivo"],
        "status": dispositivo["status"],
        "id_dueno": dispositivo["id_dueno"]
    }

# Obtener todos los dispositivos
@app.get("/dispositivos", response_model=List[Dispositivo])
async def get_all_dispositivos():
    dispositivos = []
    async for dispositivo in coleccion_dispositivos.find():
        dispositivos.append(dispositivo_helper(dispositivo))
    return dispositivos

# Crear un dispositivo
@app.post("/dispositivos", response_model=Dispositivo)
async def create_dispositivo(dispositivo: DispositivoCreate):
    nuevo_dispositivo = await coleccion_dispositivos.insert_one(dispositivo.dict())
    creado_dispositivo = await coleccion_dispositivos.find_one({"_id": nuevo_dispositivo.inserted_id})
    return dispositivo_helper(creado_dispositivo)

# Actualizar un dispositivo
@app.put("/dispositivos/{dispositivo_id}", response_model=Dispositivo)
async def update_dispositivo(dispositivo_id: str, dispositivo_data: DispositivoCreate):
    if not ObjectId.is_valid(dispositivo_id):
        raise HTTPException(status_code=400, detail="ID de dispositivo no válido")

    update_result = await coleccion_dispositivos.update_one(
        {"_id": ObjectId(dispositivo_id)},
        {"$set": dispositivo_data.dict()}
    )

    if update_result.modified_count == 1:
        updated_dispositivo = await coleccion_dispositivos.find_one({"_id": ObjectId(dispositivo_id)})
        if updated_dispositivo:
            return dispositivo_helper(updated_dispositivo)
    
    existing_dispositivo = await coleccion_dispositivos.find_one({"_id": ObjectId(dispositivo_id)})
    if existing_dispositivo:
        return dispositivo_helper(existing_dispositivo)

    raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

# Eliminar un dispositivo
@app.delete("/dispositivos/{dispositivo_id}")
async def delete_dispositivo(dispositivo_id: str):
    if not ObjectId.is_valid(dispositivo_id):
        raise HTTPException(status_code=400, detail="ID de dispositivo no válido")

    delete_result = await coleccion_dispositivos.delete_one({"_id": ObjectId(dispositivo_id)})

    if delete_result.deleted_count == 1:
        return {"mensaje": "Dispositivo eliminado"}
    
    raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
