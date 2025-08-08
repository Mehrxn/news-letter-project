#!/usr/bin/env python3
"""
AI News Processor Example

This script demonstrates how to use the NewsProcessor class with Gemini AI
for article summarization and deduplication.
"""

import os
from newsletter_generator import NewsProcessor, fetch_rss_feeds

def main():
    """Example usage of the NewsProcessor class."""
    
    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY environment variable not set!")
        print("To use this example:")
        print("1. Get a Gemini API key from: https://makersuite.google.com/app/apikey")
        print("2. Set the environment variable:")
        print("   export GEMINI_API_KEY='your-api-key-here'")
        print("   # or on Windows:")
        print("   set GEMINI_API_KEY=your-api-key-here")
        return
    
    print("🤖 AI News Processor Example")
    print("=" * 40)
    
    try:
        # Initialize NewsProcessor
        print("Initializing NewsProcessor with Gemini AI...")
        processor = NewsProcessor(api_key)
        print("✅ NewsProcessor initialized successfully!")
        
        # Fetch some articles from RSS feeds
        print("\n📡 Fetching articles from RSS feeds...")
        feed_urls = [
            "https://feeds.bbci.co.uk/news/rss.xml",
            "https://feeds.feedburner.com/TechCrunch/"
        ]
        
        raw_articles = fetch_rss_feeds(feed_urls)
        
        if not raw_articles:
            print("❌ No articles retrieved. Using sample articles instead.")
            # Use sample articles if RSS feeds fail
            raw_articles = [
                {
                    'title': 'AI Breakthrough in Medical Diagnosis',
                    'link': 'https://example.com/ai-medical',
                    'summary': 'Researchers have developed a new AI system that can diagnose rare diseases with 95% accuracy. The system uses deep learning algorithms to analyze medical images and patient data, providing faster and more accurate diagnoses than traditional methods. This breakthrough could revolutionize healthcare by reducing diagnostic errors and improving patient outcomes.',
                    'source': 'Tech News'
                },
                {
                    'title': 'Climate Change Impact on Global Economy',
                    'link': 'https://example.com/climate-economy',
                    'summary': 'A comprehensive study reveals that climate change could cost the global economy up to $23 trillion by 2050. The research examines various scenarios including extreme weather events, rising sea levels, and agricultural disruptions. Economists warn that immediate action is needed to mitigate these financial impacts.',
                    'source': 'Environmental News'
                },
                {
                    'title': 'Space Exploration: Mars Mission Update',
                    'link': 'https://example.com/mars-mission',
                    'summary': 'NASA\'s latest Mars rover has discovered evidence of ancient water on the red planet. The findings include mineral deposits that suggest Mars once had flowing rivers and lakes. Scientists believe this discovery could indicate that Mars was habitable billions of years ago.',
                    'source': 'Space News'
                }
            ]
        
        print(f"📰 Retrieved {len(raw_articles)} articles for processing")
        
        # Process articles with AI
        print("\n🧠 Processing articles with Gemini AI...")
        processed_articles = processor.process_articles(raw_articles)
        
        if processed_articles:
            print(f"\n✅ Successfully processed {len(processed_articles)} articles!")
            print("\n📋 Sample processed articles:")
            print("-" * 50)
            
            for i, article in enumerate(processed_articles[:3], 1):
                print(f"\n{i}. {article['title']}")
                print(f"   Source: {article['source']}")
                print(f"   Link: {article['link']}")
                if article.get('llm_summary'):
                    print(f"   🤖 AI Summary: {article['llm_summary']}")
                print()
            
            # Save results
            from newsletter_generator import save_articles_to_file
            save_articles_to_file(processed_articles, "ai_processed_articles.txt")
            print("💾 Results saved to 'ai_processed_articles.txt'")
            
        else:
            print("❌ No articles were successfully processed.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure your API key is valid and you have internet connectivity.")


if __name__ == "__main__":
    main() 