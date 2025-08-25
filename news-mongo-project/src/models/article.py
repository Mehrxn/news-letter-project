from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from pymongo.errors import DuplicateKeyError


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

        # Require URL for idempotent behavior
        url_value = document.get("url")
        if not url_value:
            print("Document missing required 'url' field; cannot upsert")
            return False

        # Idempotent upsert: insert on first occurrence, skip on duplicate
        result = articles_collection.update_one(
            {"url": url_value},
            {"$setOnInsert": document},
            upsert=True,
        )

        if result.upserted_id is not None:
            print(f"Article inserted with id: {result.upserted_id}")
        else:
            print("Article with this URL already exists; skipped inserting duplicate.")
        return True
    except DuplicateKeyError:
        print("Article with this URL already exists; skipped inserting duplicate.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False