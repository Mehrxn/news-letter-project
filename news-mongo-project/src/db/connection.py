from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_database():
    mongo_uri = os.getenv("MONGO_URI")
    try:
        client = MongoClient(mongo_uri)
        db = client.get_default_database()
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None