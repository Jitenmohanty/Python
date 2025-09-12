from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Global variables
client = None
db = None
users_collection = None
todos_collection = None
is_connected = False

async def init_db():
    """Initialize the database connection"""
    global client, db, users_collection, todos_collection, is_connected
    try:
        client = AsyncIOMotorClient(MONGO_DETAILS, serverSelectionTimeoutMS=5000)
        logger.info("Attempting to connect to MongoDB...")
        await client.admin.command('ping')
        logger.info("✅ Successfully connected to MongoDB!")

        db = client.todo_db
        users_collection = db.users
        todos_collection = db.todos
        logger.info(f"Using database: {db.name}")
        is_connected = True
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        client = db = users_collection = todos_collection = None
        is_connected = False

# Accessor functions
def get_users_collection():
    return users_collection

def get_todos_collection():
    return todos_collection
