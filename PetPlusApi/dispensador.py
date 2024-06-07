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

@app.put("/dispositivos/{dispositivo_id}", response_model=Dispositivo)
async def update_dispositivo(dispositivo_id: str, dispositivo_data: DispositivoCreate):
    raise NotImplementedError

@app.delete("/dispositivos/{dispositivo_id}")
async def delete_dispositivo(dispositivo_id: str):
    raise NotImplementedError

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
