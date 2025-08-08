from dotenv import load_dotenv
import os
from datetime import datetime
from db.connection import connect_to_mongo
from models.article import insert_article

def main():
    # Load environment variables
    load_dotenv()
    
    # Connect to the database
    db = connect_to_mongo()
    
    # Define a sample article document
    sample_article = {
        "title": "Sample News Article",
        "summary": "This is a summary of the sample news article.",
        "url": "https://example.com/sample-news-article",
        "source": "Example News",
        "publication_date": datetime.now(),
        "author": "John Doe",
        "tags": ["sample", "news", "example"]
    }
    
    # Insert the sample article into the articles collection
    if insert_article(db, sample_article):
        print("Article inserted successfully.")
    else:
        print("Failed to insert article.")

if __name__ == "__main__":
    main()