from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

class DispositivoBase(BaseModel):
    id: str
    status: str
    owner_id: str

class DispositivoCreate(DispositivoBase):
    pass

class Dispositivo(DispositivoBase):
    pass

@app.get("/dispositivos", response_model=List[Dispositivo])
async def get_all_dispositivos():
    response = requests.get("https://eouww9yquk.execute-api.us-east-1.amazonaws.com/pets/get_pets")
    if response.status_code == 200:
        datos_dispositivos = response.json()["pets"]
        dispositivos = []
        for dato_dispositivo in datos_dispositivos:
            dispositivo = Dispositivo(
                id=dato_dispositivo["id"],
                status=dato_dispositivo["status"],
                owner_id=dato_dispositivo["owner_id"]
            )
            dispositivos.append(dispositivo)
        return dispositivos
    else:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener datos")

async def get_dispositivo(dispositivo_id: str) -> Dispositivo:
    response = requests.get(f"https://eouww9yquk.execute-api.us-east-1.amazonaws.com/pets/get_pet?id={dispositivo_id}")
    if response.status_code == 200:
        dato_dispositivo = response.json()
        dispositivo = Dispositivo(
            id=dato_dispositivo["id"],
            status=dato_dispositivo["status"],
            owner_id=dato_dispositivo["owner_id"]
        )
        return dispositivo
    else:
        raise HTTPException(status_code=response.status_code, detail="Dispositivo no encontrado")

@app.put("/dispositivos/{dispositivo_id}", response_model=Dispositivo)
async def update_dispositivo(dispositivo_id: str, dispositivo_data: DispositivoCreate):
    dispositivo_actual = await get_dispositivo(dispositivo_id)

    dispositivo_actual.status = dispositivo_data.status

    url = f"https://eouww9yquk.execute-api.us-east-1.amazonaws.com/pets/update_pet?id={dispositivo_id}"
    headers = {"Content-Type": "application/json"}
    datos = dispositivo_actual.dict()

    try:
        respuesta = requests.put(url, headers=headers, json=datos)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el dispositivo: {error}")

    return dispositivo_actual

@app.delete("/dispositivos/{dispositivo_id}")
async def delete_dispositivo(dispositivo_id: str):
    url = f"https://eouww9yquk.execute-api.us-east-1.amazonaws.com/pets/delete_pet?id={dispositivo_id}"

    try:
        respuesta = requests.delete(url)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el dispositivo: {error}")

    return {"mensaje": "Dispositivo eliminado exitosamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)