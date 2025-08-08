#!/usr/bin/env python3
"""
Test script to demonstrate the scoring functionality
"""

import os
from newsletter_generator import NewsProcessor, save_articles_to_file

def main():
    """Test the scoring functionality with sample articles."""
    
    print("🏆 Testing Article Scoring System")
    print("=" * 50)
    
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
        
        # Sample articles for testing
        sample_articles = [
            {
                'title': 'Breaking: Major AI Breakthrough in Medical Diagnosis',
                'link': 'https://example.com/ai-medical',
                'summary': 'Researchers have developed a new AI system that can diagnose rare diseases with 95% accuracy. The system uses deep learning algorithms to analyze medical images and patient data, providing faster and more accurate diagnoses than traditional methods. This breakthrough could revolutionize healthcare by reducing diagnostic errors and improving patient outcomes.',
                'source': 'BBC News'
            },
            {
                'title': 'Climate Change Impact on Global Economy',
                'link': 'https://example.com/climate-economy',
                'summary': 'A comprehensive study reveals that climate change could cost the global economy up to $23 trillion by 2050. The research examines various scenarios including extreme weather events, rising sea levels, and agricultural disruptions. Economists warn that immediate action is needed to mitigate these financial impacts.',
                'source': 'Reuters'
            },
            {
                'title': 'Top 10 Best AI Tools for 2024',
                'link': 'https://example.com/ai-tools',
                'summary': 'Here are the best AI tools you should use this year.',
                'source': 'Tech Blog'
            },
            {
                'title': 'Latest Update on Space Exploration Mission',
                'link': 'https://example.com/space-mission',
                'summary': 'NASA has announced new findings from the Mars rover mission, revealing evidence of ancient water systems and potential signs of microbial life. The discovery could reshape our understanding of the red planet and its potential for supporting life.',
                'source': 'Ars Technica'
            },
            {
                'title': 'Just In: Cybersecurity Threat Detected',
                'link': 'https://example.com/cybersecurity',
                'summary': 'Security researchers have identified a new sophisticated cyber attack targeting government systems worldwide. The attack uses advanced techniques to bypass traditional security measures.',
                'source': 'The Verge'
            }
        ]
        
        print(f"🧪 Testing scoring with {len(sample_articles)} sample articles...")
        
        # Process articles with AI and scoring
        processed_articles = processor.process_articles(sample_articles, max_articles=5)
        
        if processed_articles:
            print(f"\n✅ Successfully processed {len(processed_articles)} articles!")
            print("\n📋 Results (Sorted by Score):")
            print("=" * 60)
            
            for i, article in enumerate(processed_articles, 1):
                score = article.get('score', 0)
                print(f"\n🏆 #{i} (Score: {score:.1f}/10)")
                print(f"📰 {article['title']}")
                print(f"📡 Source: {article['source']}")
                print(f"🔗 Link: {article['link']}")
                if article.get('llm_summary'):
                    print(f"🤖 AI Summary: {article['llm_summary']}")
                print("-" * 50)
            
            # Show score statistics
            scores = [article.get('score', 0) for article in processed_articles]
            avg_score = sum(scores) / len(scores) if scores else 0
            print(f"\n📊 Score Statistics:")
            print(f"   Highest Score: {max(scores):.1f}/10")
            print(f"   Lowest Score: {min(scores):.1f}/10")
            print(f"   Average Score: {avg_score:.1f}/10")
            print(f"   Articles with score ≥8: {len([s for s in scores if s >= 8])}")
            print(f"   Articles with score ≥6: {len([s for s in scores if s >= 6])}")
            
            # Save results
            save_articles_to_file(processed_articles, "test_scoring_results.txt")
            print("\n💾 Results saved to 'test_scoring_results.txt'")
            
        else:
            print("❌ No articles were successfully processed.")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 