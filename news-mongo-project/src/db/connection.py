from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    """Return a MongoDB database handle.

    Resolution order:
    1) If env `MONGO_DB_NAME` is set, return that database
    2) If URI contains a default DB, use `get_default_database()`
    3) Fallback to `news_database`
    """
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise Exception("MONGO_URI not found in environment variables")
    client = MongoClient(mongo_uri)

    # Prefer explicit DB name from env
    db_name = os.getenv("MONGO_DB_NAME", "newsletter")  # fallback db name
    db = client[db_name]

    return db


# Backwards-compatible alias expected by callers
def connect_to_mongo():
    """Return a MongoDB database handle using env var MONGO_URI.

    This function is a thin wrapper around get_database() provided
    for compatibility with existing imports in the codebase.
    """
    return get_db()