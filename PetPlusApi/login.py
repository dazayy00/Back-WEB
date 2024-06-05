from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from werkzeug.security import generate_password_hash, check_password_hash
from models import AdminLogin

app = FastAPI()

#base de datos ejemplo
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.my_database
admins_collection = db.admins

#login admins agregados en bd
@app.post("/login")
async def login(admin: AdminLogin):
    # checa matriculas existentes 
    db_admins = await admins_collection.find_one({"matricula": {"$exists": True}, "matricula": admin.matricula})
    if not db_admins:
        raise HTTPException(status_code=400, detail="No exite la matricula")

    # valida contraseñas
    if not check_password_hash(db_admins["hashed_password"], admin.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {"message": "Login correcto"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


#iniciar el servidor uvicorn login:app --reload
#apagar server ctrl+c
#documentacion swagger http://127.0.0.1:8000/docs
#documentacion redocly http://127.0.0.1:8000/redoc
