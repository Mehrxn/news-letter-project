#!/usr/bin/env python3
"""
Simple AI test script - processes only a few articles to avoid rate limits
"""

import os
from newsletter_generator import NewsProcessor, fetch_rss_feeds, save_articles_to_file

def main():
    """Test AI processing with just a few articles."""
    
    print("🤖 Simple AI Newsletter Test")
    print("=" * 40)
    
    # Get API key from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("❌ python-dotenv not installed. Run: pip install python-dotenv")
        return
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your-api-key-here':
        print("❌ No valid API key found in .env file")
        print("Please set your API key in the .env file")
        return
    
    try:
        # Initialize NewsProcessor
        print("✅ Initializing AI processor...")
        processor = NewsProcessor(api_key)
        
        # Fetch just a few articles from one feed
        print("📰 Fetching articles from BBC News...")
        articles = fetch_rss_feeds(["https://feeds.bbci.co.uk/news/rss.xml"])
        
        if not articles:
            print("❌ No articles retrieved")
            return
        
        # Take only the first 5 articles to avoid rate limits
        test_articles = articles[:5]
        print(f"🧪 Testing with {len(test_articles)} articles...")
        
        # Process articles with AI (limit to 5 for testing)
        processed_articles = processor.process_articles(test_articles, max_articles=5)
        
        if processed_articles:
            print(f"\n✅ Successfully processed {len(processed_articles)} articles!")
            print("\n📋 Results:")
            print("-" * 50)
            
            for i, article in enumerate(processed_articles, 1):
                score = article.get('score', 0)
                print(f"\n🏆 #{i} (Score: {score:.1f}/10)")
                print(f"📰 {article['title']}")
                print(f"📡 Source: {article['source']}")
                print(f"🔗 Link: {article['link']}")
                if article.get('llm_summary'):
                    print(f"🤖 AI Summary: {article['llm_summary']}")
                print("-" * 50)
            
            # Save results
            save_articles_to_file(processed_articles, "test_ai_simple_results.txt")
            print("💾 Results saved to 'test_ai_simple_results.txt'")
            
        else:
            print("❌ No articles were successfully processed.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 