from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI()

# MongoDB config
MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")
Message_Collection = os.getenv("Message_Collection")

if not MONGO_URL or not DATABASE_NAME:
    raise RuntimeError("MONGO_URL or DATABASE_NAME not found in environment variables")

client: AsyncIOMotorClient | None = None
db = None
collection = None
async def connect_to_mongo():
    global client, db, collection
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DATABASE_NAME]
    collection = db[Message_Collection]


async def close_mongo_connection():
    client.close()

# Endpoints definition
#startup event to connect to MongoDB
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

# Root endpoint
@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI REST API!"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}
# Database Health check
@app.get("/db-health")
async def db_health():
    try:
        await client.admin.command("ping")
        return {"mongodb": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add message endpoint
@app.post("/add_message")
async def add_message(message: str, subject: Optional[str] = None,
class_name: Optional[str] = None):
    message_data = {    
        "message": message,
        "subject": subject,
        "class_name": class_name,
        "timestamp": datetime.utcnow()
    }
    await collection.insert_one(message_data)
    return {"message": "Message added successfully"}

# Get all messages endpoint
@app.get("/messages")
async def get_messages():
# Your code to fetch all messages from MongoDB
    messages = await collection.find().to_list(length=None)
    return messages
# Analyze messages endpoint
@app.get("/analyze")
async def analyze(group_by: Optional[str] = None):
# Your code to analyze data and group by parameter
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()