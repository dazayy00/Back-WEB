from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from models import Login, Admin

app = FastAPI()

client = AsyncIOMotorClient('mongodb+srv://dazayy:pononoinuv@adminpp.dywe5yc.mongodb.net/?retryWrites=true&w=majority&appName=AdminPP')
database = client.AdminPet
collection = database.administrador

@app.post("/login")
async def login(login: Login):
    filter = {"$and": [{"Matricula": login.Matricula}]}  
    db_admin = await collection.find_one(filter)  

    if not db_admin:
        raise HTTPException(status_code=400, detail="Username or Matricula incorrect")
    return {"message": "Login chido"}

#documentacion swagger http://127.0.0.1:8000/docs
#documentacion redocly http://127.0.0.1:8000/redoc
