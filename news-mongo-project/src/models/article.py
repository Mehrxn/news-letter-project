from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class Article:
    def __init__(self, title, summary, url, source, publication_date, author=None, tags=None):
        self.title = title
        self.summary = summary
        self.url = url
        self.source = source
        self.publication_date = publication_date
        self.author = author
        self.tags = tags if tags is not None else []

def insert_article(article):
    try:
        client = MongoClient(os.getenv("MONGO_URI"))
        db = client['news_database']
        articles_collection = db['articles']
        
        # Ensure unique index on the url field
        articles_collection.create_index([("url", 1)], unique=True)

        result = articles_collection.insert_one(article.__dict__)
        if result.inserted_id:
            print(f"Article inserted with id: {result.inserted_id}")
        else:
            print("Failed to insert article.")
    except Exception as e:
        print(f"An error occurred: {e}")