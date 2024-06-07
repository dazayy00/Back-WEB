from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

class Admin(BaseModel):
    Nombre: str
    Email: str
    Imagen: str


app = FastAPI()

client = AsyncIOMotorClient("mongodb+srv://dazayy:pononoinuv@adminpp.dywe5yc.mongodb.net/?retryWrites=true&w=majority&appName=AdminPP")
db = client.AdminPP
admins_collection = db.admins


@app.get("/admin")
async def get_admin_data(Matricula: str): 
    db_admin = await admins_collection.find_one({"_Matricula": Matricula})  

    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin no encontrado")

    admin = Admin(**db_admin)

    return admin


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
