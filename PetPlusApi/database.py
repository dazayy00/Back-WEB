from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from models import Admin
from bson import ObjectId


app = FastAPI()


client = AsyncIOMotorClient('mongodb+srv://dazayy:pononoinuv@adminpp.dywe5yc.mongodb.net/?retryWrites=true&w=majority&appName=AdminPP')
database = client.AdminPet
collection = database.administrador

#get uno solo
async def get_one_admin_by_id(id: str):
    admin = await collection.find_one({'_id': ObjectId(id)})
    return admin

#get todos
async def get_all_admins():
    cursor = collection.find({})
    admins = []
    async for document in cursor:
        admins.append(document)
    return admins

#post
@app.post('/api/admins', response_model=Admin) #linea de error post 
async def create_admin(admin: Admin): 
    response = await create_admin(admin)  
    if response:
        return response
    raise HTTPException(status_code=400, detail="Error creating admin")


#put
async def update(id: str, admin_data: dict):
    await collection.update_one({'_id': ObjectId(id)}, {'$set': admin_data})
    document = await collection.find_one({'_id': ObjectId(id)})
    return document

#delete
async def delete(id: str):
    await collection.delete_one({'_id': ObjectId(id)})
    return True

async def get_admin_by_matricula(Matricula: str):
    admin = await collection.find_one({'Matricula': Matricula})
    return admin