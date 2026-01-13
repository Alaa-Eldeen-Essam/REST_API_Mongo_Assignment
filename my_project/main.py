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

if not MONGO_URL or not DATABASE_NAME:
    raise RuntimeError("MONGO_URL or DATABASE_NAME not found in environment variables")

client: AsyncIOMotorClient | None = None
db = None

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DATABASE_NAME]


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
@app.get("/add_message")
async def add_message(message: str, subject: Optional[str] = None,
class_name: Optional[str] = None):
# Your code to store the message in MongoDB
    pass

# Get all messages endpoint
@app.get("/messages")
async def get_messages():
# Your code to fetch all messages from MongoDB
    pass

# Analyze messages endpoint
@app.get("/analyze")
async def analyze(group_by: Optional[str] = None):
# Your code to analyze data and group by parameter
    pass

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()