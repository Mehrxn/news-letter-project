from pymongo import MongoClient, errors
from datetime import datetime

class ArticleSchema:
    def __init__(self, title, summary, url, source, publication_date, author=None, tags=None):
        self.title = title
        self.summary = summary
        self.url = url
        self.source = source
        self.publication_date = publication_date
        self.author = author
        self.tags = tags if tags is not None else []

    def to_dict(self):
        return {
            "title": self.title,
            "summary": self.summary,
            "url": self.url,
            "source": self.source,
            "publication_date": self.publication_date,
            "author": self.author,
            "tags": self.tags
        }

def create_unique_index(collection):
    try:
        collection.create_index([("url", 1)], unique=True)
    except errors.DuplicateKeyError:
        print("Unique index on 'url' already exists.")