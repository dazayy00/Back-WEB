from motor.motor_asyncio import AsyncIOMotorClient
from models import Admin
from bson import ObjectId

client = AsyncIOMotorClient('mongodb+srv://dazayy:pononoinuv@adminpp.dywe5yc.mongodb.net/?retryWrites=true&w=majority&appName=AdminPP')
database = client.AdminPet
collection = database.administrador

async def get_one_admin_by_id(id: str):
    admin = await collection.find_one({'_id': ObjectId(id)})
    return admin

async def get_all_admins():
    cursor = collection.find({})
    admins = []
    async for document in cursor:
        admins.append(document)
    return admins

async def create_admin(admin: Admin):  
    result = await collection.insert_one(admin.dict())
    created_admin = await collection.find_one({'_id': result.inserted_id})
    return created_admin

async def update(id: str, admin_data: dict):
    await collection.update_one({'_id': ObjectId(id)}, {'$set': admin_data})
    updated_admin = await collection.find_one({'_id': ObjectId(id)})
    return updated_admin

async def delete(id: str):
    await collection.delete_one({'_id': ObjectId(id)})
    return True

async def get_admin_by_matricula(matricula: str):
    admin = await collection.find_one({'Matricula': matricula})
    return admin
