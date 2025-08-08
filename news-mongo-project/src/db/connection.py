from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_database():
    """Return a MongoDB database handle.

    Resolution order:
    1) If env `MONGO_DB_NAME` is set, return that database
    2) If URI contains a default DB, use `get_default_database()`
    3) Fallback to `news_database`
    """
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("Error: MONGO_URI not set in environment")
        return None
    try:
        client = MongoClient(mongo_uri)

        # Prefer explicit DB name from env
        db_name = os.getenv("MONGO_DB_NAME")
        if db_name:
            return client[db_name]

        # Try default DB from URI (works when URI ends with /dbname)
        try:
            db = client.get_default_database()
            if db is not None:
                return db
        except Exception:
            pass

        # Fallback to a sensible default
        return client["news_database"]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


# Backwards-compatible alias expected by callers
def connect_to_mongo():
    """Return a MongoDB database handle using env var MONGO_URI.

    This function is a thin wrapper around get_database() provided
    for compatibility with existing imports in the codebase.
    """
    return get_database()