from dotenv import load_dotenv
import os
from datetime import datetime
from db.connection import connect_to_mongo
from models.article import insert_article
from db.schema import ArticleSchema

def main():
    # Load environment variables
    load_dotenv()
    
    # Connect to the database
    db = connect_to_mongo()
    
    # Build the document using ArticleSchema and its to_dict()
    article_doc = ArticleSchema(
        title="Sample News Article",
        summary="This is a summary of the sample news article.",
        url="https://example.com/sample-news-article",
        source="Example News",
        publication_date=datetime.now(),
        author="John Doe",
        tags=["sample", "news", "example"],
    ).to_dict()

    # Insert the document (dict) into the articles collection
    if insert_article(db, article_doc):
        print("Article inserted successfully.")
    else:
        print("Failed to insert article.")

if __name__ == "__main__":
    main()