from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

#codigo a implementar
class PetBase(BaseModel):
    id_race: str
    id_user: str
    id: str
    name: str
    weight: str
    age: str

class PetCreate(PetBase):
    pass

class Pet(PetBase):
    pass

@app.get("/pets", response_model=List[Pet])
async def get_all_pets():
    response = requests.get("https://eouww9yquk.execute-api.us-east-1.amazonaws.com/pets/get_pets")
    if response.status_code == 200:
        datos_pets = response.json()["pets"]
        pets = []
        for dato_pet in datos_pets:
            pet = Pet(
                id_race=dato_pet["id_race"],
                id_user=dato_pet["id_user"],
                id=dato_pet["id"],
                name=dato_pet["name"],
                weight=dato_pet["weight"],
                age=dato_pet["age"]
            )
            pets.append(pet)
        return pets
    else:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener datos")

async def get_pet(pet_id: str) -> Pet:
    response = requests.get(f"https://eouww9yquk.execute-api.us-east-1.amazonaws.com/pets/get_pet?id={pet_id}")
    if response.status_code == 200:
        dato_pet = response.json()
        pet = Pet(
            id_race=dato_pet["id_race"],
            id_user=dato_pet["id_user"],
            id=dato_pet["id"],
            name=dato_pet["name"],
            weight=dato_pet["weight"],
            age=dato_pet["age"]
        )
        return pet
    else:
        raise HTTPException(status_code=response.status_code, detail="Mascota no encontrada")

@app.put("/pets/{pet_id}", response_model=Pet)
async def update_pet(pet_id: str, pet_data: PetCreate):
    pet_actual = await get_pet(pet_id)

    pet_actual.id_race = pet_data.id_race
    pet_actual.id_user = pet_data.id_user
    pet_actual.name = pet_data.name
    pet_actual.weight = pet_data.weight
    pet_actual.age = pet_data.age

    url = f"https://eouww9yquk.execute-api.us-east-1.amazonaws.com/pets/update_pet?id={pet_id}"
    headers = {"Content-Type": "application/json"}
    datos = pet_actual.dict()

    try:
        respuesta = requests.put(url, headers=headers, json=datos)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la mascota: {error}")

    return pet_actual

@app.delete("/pets/{pet_id}")
async def delete_pet(pet_id: str):
    url = f"https://eouww9yquk.execute-api.us-east-1.amazonaws.com/pets/delete_pet?id={pet_id}"

    try:
        respuesta = requests.delete(url)
        respuesta.raise_for_status()
    except requests.exceptions.RequestException as error:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la mascota: {error}")

    return {"mensaje": "Mascota eliminada exitosamente"}
