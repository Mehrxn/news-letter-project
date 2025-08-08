from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from db.connection import get_database


class Article:
    def __init__(
        self,
        title: str,
        summary: str,
        url: str,
        source: str,
        publication_date: datetime,
        author: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        self.title = title
        self.summary = summary
        self.url = url
        self.source = source
        self.publication_date = publication_date
        self.author = author
        self.tags = tags if tags is not None else []

    def to_document(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "summary": self.summary,
            "url": self.url,
            "source": self.source,
            "publication_date": self.publication_date,
            "author": self.author,
            "tags": self.tags,
        }


def insert_article(db, article: Union[Article, Dict[str, Any]]) -> bool:
    """Insert an Article into the provided database.

    Expects a database handle (from get_database/connect_to_mongo) and an Article instance.
    Returns True on success, False otherwise.
    """
    try:
        if db is None:
            print("No database handle provided (db is None)")
            return False

        articles_collection = db["articles"]

        # Ensure unique index on the url field
        articles_collection.create_index([("url", 1)], unique=True)

        # Support both Article instances and plain dicts
        document = article.to_document() if hasattr(article, "to_document") else dict(article)

        result = articles_collection.insert_one(document)
        if result.inserted_id:
            print(f"Article inserted with id: {result.inserted_id}")
            return True
        print("Failed to insert article.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False