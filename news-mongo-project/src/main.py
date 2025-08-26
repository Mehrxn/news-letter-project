from dotenv import load_dotenv
import os
from datetime import datetime
from db.connection import get_db
from db.schema import insert_article
from models.article import Article

def save_articles_to_mongo(processed_articles):
    db = get_db()
    for art in processed_articles:
        article = Article(
            title=art['title'],
            summary=art.get('llm_summary', art.get('summary')),
            url=art['link'],
            source=art['source'],
            publication_date=art.get('publication_date', datetime.now()),
            author=art.get('author'),
            tags=art.get('tags', []),
            score=art.get('score')
        )
        insert_article(db, article.to_dict())

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
    # Import your scoring/news generator logic
    from newsletter_generator import main as generate_news

    # Modify newsletter_generator.py: main(return_articles=True) returns processed_articles
    processed_articles = generate_news(return_articles=True)
    save_articles_to_mongo(processed_articles)
    print("Articles saved to MongoDB Atlas.")