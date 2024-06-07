from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient


class AdminLogin(BaseModel):
    Email: str
    Matricula: str


app = FastAPI()

client = AsyncIOMotorClient("mongodb+srv://dazayy:pononoinuv@adminpp.dywe5yc.mongodb.net/?retryWrites=true&w=majority&appName=AdminPP")
db = client.AdminPP
admins_collection = db.admins


# Login para admins agregados en la base de datos
@app.post("/login")
async def login(admin: AdminLogin):
    # Busca admins por email y matricula
    db_admin = await admins_collection.find_one({
        "$and": [
            {"email": admin.Email},
            {"matricula": admin.Matricula},
        ]
    })

    if not db_admin:
        raise HTTPException(status_code=400, detail="Email o matrícula incorrecta")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


#iniciar el servidor uvicorn login:app --reload
#apagar server ctrl+c
#documentacion swagger http://127.0.0.1:8000/docs
#documentacion redocly http://127.0.0.1:8000/redoc
