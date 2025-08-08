#!/usr/bin/env python3
"""
Newsletter Generator - RSS Feed Parser

A complete Python script that retrieves and parses RSS feeds using the feedparser library.
Includes robust error handling for network requests and malformed feeds.
Now enhanced with Gemini AI-powered article summarization and deduplication.
"""

import feedparser
import requests
import time
from typing import List, Dict, Optional
from urllib.parse import urlparse
import logging
from datetime import datetime
import sys
import os
import google.generativeai as genai

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")
    print("Or set GEMINI_API_KEY as environment variable.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('newsletter_generator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class NewsProcessor:
    """
    A class to process news articles using Gemini AI for summarization and deduplication.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize the NewsProcessor with Gemini API key.
        
        Args:
            api_key (str): Gemini API key for authentication
        """
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)
            
            # Initialize the model
            self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
            
            logger.info("NewsProcessor initialized successfully with Gemini API")
        except Exception as e:
            logger.error(f"Failed to initialize NewsProcessor: {str(e)}")
            raise
    
    def _get_summary(self, article_text: str) -> str:
        """
        Generate a concise summary of the article using Gemini AI.
        
        Args:
            article_text (str): The full text of the article
            
        Returns:
            str: A short, one-paragraph summary
        """
        try:
            system_prompt = """You are a professional news summarizer. Your task is to create concise, 
            informative one-paragraph summaries of news articles. Focus on the key facts, main events, 
            and important context. Keep summaries clear, accurate, and engaging. Avoid repetition and 
            ensure the summary captures the essence of the story."""
            
            prompt = f"{system_prompt}\n\nArticle text:\n{article_text}\n\nProvide a concise summary:"
            
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text.strip()
            else:
                logger.warning("Gemini API returned empty response")
                return "Summary unavailable"
                
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg and "quota" in error_msg.lower():
                logger.warning("Rate limit reached. Waiting 60 seconds before retrying...")
                time.sleep(60)  # Wait 60 seconds for rate limit to reset
                try:
                    response = self.model.generate_content(prompt)
                    if response.text:
                        return response.text.strip()
                except Exception as retry_e:
                    logger.error(f"Retry failed: {str(retry_e)}")
                    return "Summary unavailable (rate limited)"
            else:
                logger.error(f"Error generating summary with Gemini API: {error_msg}")
            return "Summary generation failed"
    
    def _score_article(self, article: Dict) -> float:
        """
        Score an article from 1-10 based on various factors.
        
        Args:
            article (Dict): Article dictionary with title, summary, source
            
        Returns:
            float: Score from 1-10
        """
        try:
            title = article.get('title', '').lower()
            summary = article.get('summary', '').lower()
            source = article.get('source', '').lower()
            
            # Scoring criteria
            score = 5.0  # Base score
            
            # Source credibility (weight: 2.0)
            credible_sources = ['bbc', 'reuters', 'ap', 'bloomberg', 'cnn', 'nbc', 'abc', 'cbs']
            tech_sources = ['techcrunch', 'the verge', 'ars technica', 'venturebeat', 'wired']
            
            if any(source in source for source in credible_sources):
                score += 2.0
            elif any(source in source for source in tech_sources):
                score += 1.5
            
            # Content length and quality (weight: 1.5)
            content_length = len(summary)
            if content_length > 200:
                score += 1.5
            elif content_length > 100:
                score += 1.0
            elif content_length > 50:
                score += 0.5
            
            # Breaking news indicators (weight: 1.0)
            breaking_keywords = ['breaking', 'urgent', 'just in', 'latest', 'update']
            if any(keyword in title for keyword in breaking_keywords):
                score += 1.0
            
            # Topic relevance (weight: 1.0)
            important_topics = ['ai', 'artificial intelligence', 'technology', 'climate', 'economy', 
                              'politics', 'health', 'science', 'space', 'cybersecurity']
            if any(topic in title or topic in summary for topic in important_topics):
                score += 1.0
            
            # Title quality (weight: 0.5)
            if len(title) > 20 and not title.startswith('top') and not title.startswith('best'):
                score += 0.5
            
            # Ensure score is between 1-10
            return max(1.0, min(10.0, score))
            
        except Exception as e:
            logger.error(f"Error scoring article: {str(e)}")
            return 5.0  # Default score
    
    def process_articles(self, raw_articles: List[Dict], max_articles: int = 50) -> List[Dict]:
        """
        Process articles by generating AI summaries, removing duplicates, scoring, and limiting to max_articles.
        
        Args:
            raw_articles (List[Dict]): List of article dictionaries with 'title', 'link', and 'summary'
            max_articles (int): Maximum number of articles to process (default: 50)
            
        Returns:
            List[Dict]: Processed, scored, and sorted articles with 'llm_summary' and 'score' fields
        """
        if not raw_articles:
            logger.warning("No articles provided for processing")
            return []
        
        logger.info(f"Processing up to {max_articles} articles from {len(raw_articles)} total articles")
        
        processed_articles = []
        seen_links = set()
        
        for i, article in enumerate(raw_articles):
            # Stop if we've reached the limit
            if len(processed_articles) >= max_articles:
                logger.info(f"Reached limit of {max_articles} articles, stopping processing")
                break
                
            try:
                # Check if article has required fields
                if not all(key in article for key in ['title', 'link', 'summary']):
                    logger.warning(f"Article {i} missing required fields, skipping")
                    continue
                
                # Skip if we've already seen this link (deduplication)
                if article['link'] in seen_links:
                    logger.info(f"Skipping duplicate article: {article['title'][:50]}...")
                    continue
                
                # Add link to seen set
                seen_links.add(article['link'])
                
                # Score the article
                score = self._score_article(article)
                article['score'] = score
                
                # Generate AI summary
                logger.info(f"Processing article {len(processed_articles)+1}/{max_articles}: {article['title'][:50]}... (Score: {score:.1f})")
                llm_summary = self._get_summary(article['summary'])
                
                # Add the AI summary to the article
                article['llm_summary'] = llm_summary
                
                # Add to processed articles
                processed_articles.append(article)
                
                # Delay to respect rate limits (free tier: 10 requests per minute)
                time.sleep(6)  # 6 seconds between requests = 10 per minute
                
            except Exception as e:
                logger.error(f"Error processing article {i}: {str(e)}")
                continue
        
        # Sort articles by score (highest first)
        processed_articles.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        logger.info(f"Successfully processed {len(processed_articles)} articles (removed {len(raw_articles) - len(processed_articles)} duplicates/over limit)")
        logger.info(f"Articles sorted by score (highest: {processed_articles[0].get('score', 0):.1f}, lowest: {processed_articles[-1].get('score', 0):.1f})")
        
        return processed_articles


def fetch_rss_feeds(feed_urls: List[str], timeout: int = 30) -> List[Dict]:
    """
    Fetch and parse RSS feeds from a list of URLs.
    
    Args:
        feed_urls (List[str]): List of RSS feed URLs to fetch
        timeout (int): Request timeout in seconds (default: 30)
    
    Returns:
        List[Dict]: List of article dictionaries with 'title', 'link', 'summary', and 'source'
    
    Each article dictionary contains:
        - title: Article title
        - link: Article URL
        - summary: Article summary/description
        - source: Source feed name/domain
    """
    
    all_articles = []
    
    for feed_url in feed_urls:
        try:
            logger.info(f"Fetching feed: {feed_url}")
            
            # Parse the feed using feedparser
            feed = feedparser.parse(feed_url)
            
            # Check if feed parsing was successful
            if feed.bozo:
                logger.warning(f"Feed has parsing issues: {feed_url}")
                if hasattr(feed, 'bozo_exception'):
                    logger.warning(f"Parsing exception: {feed.bozo_exception}")
            
            # Check if feed has entries
            if not feed.entries:
                logger.warning(f"No entries found in feed: {feed_url}")
                continue
            
            # Extract source name from feed or URL
            source_name = get_source_name(feed, feed_url)
            
            # Process each entry in the feed
            for entry in feed.entries:
                try:
                    article = extract_article_data(entry, source_name)
                    if article:
                        all_articles.append(article)
                except Exception as e:
                    logger.error(f"Error processing entry from {feed_url}: {str(e)}")
                    continue
            
            logger.info(f"Successfully processed {len(feed.entries)} articles from {source_name}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error fetching {feed_url}: {str(e)}")
        except KeyboardInterrupt:
            logger.info("User interrupted the process")
            break
        except Exception as e:
            logger.error(f"Unexpected error processing {feed_url}: {str(e)}")
        
        # Add a small delay between requests to be respectful
        time.sleep(1)
    
    logger.info(f"Total articles collected: {len(all_articles)}")
    return all_articles


def get_source_name(feed: feedparser.FeedParserDict, feed_url: str) -> str:
    """
    Extract a meaningful source name from the feed or URL.
    
    Args:
        feed: Parsed feed object
        feed_url: Original feed URL
    
    Returns:
        str: Source name
    """
    # Try to get source from feed title
    if hasattr(feed.feed, 'title') and feed.feed.title:
        return feed.feed.title.strip()
    
    # Try to get source from feed link
    if hasattr(feed.feed, 'link') and feed.feed.link:
        domain = urlparse(feed.feed.link).netloc
        if domain:
            return domain
    
    # Fallback to domain from feed URL
    domain = urlparse(feed_url).netloc
    return domain if domain else "Unknown Source"


def extract_article_data(entry: feedparser.FeedParserDict, source_name: str) -> Optional[Dict]:
    """
    Extract article data from a feed entry.
    
    Args:
        entry: Feed entry object
        source_name: Name of the source
    
    Returns:
        Optional[Dict]: Article data dictionary or None if invalid
    """
    try:
        # Extract title
        title = entry.get('title', '').strip()
        if not title:
            logger.warning(f"Entry missing title from {source_name}")
            return None
        
        # Extract link
        link = entry.get('link', '').strip()
        if not link:
            logger.warning(f"Entry missing link from {source_name}")
            return None
        
        # Extract summary/description
        summary = ""
        
        # Try different possible summary fields
        summary_fields = ['summary', 'description', 'content', 'subtitle']
        for field in summary_fields:
            if hasattr(entry, field) and entry[field]:
                if field == 'content' and isinstance(entry[field], list):
                    # Handle content field which might be a list
                    summary = entry[field][0].get('value', '') if entry[field] else ''
                else:
                    summary = entry[field]
                break
        
        # Clean up summary (remove HTML tags if present)
        if summary:
            import re
            # Simple HTML tag removal
            summary = re.sub(r'<[^>]+>', '', summary)
            summary = summary.strip()
        
        # Truncate summary if too long
        if len(summary) > 500:
            summary = summary[:497] + "..."
        
        return {
            'title': title,
            'link': link,
            'summary': summary,
            'source': source_name
        }
        
    except Exception as e:
        logger.error(f"Error extracting article data: {str(e)}")
        return None


def main():
    """
    Main function to demonstrate the newsletter generator with AI processing.
    """
    # Example RSS feed URLs (you can replace these with your preferred feeds)
    sample_feeds = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://feeds.feedburner.com/TechCrunch/",
        "https://www.theverge.com/rss/index.xml",
        "https://feeds.feedburner.com/venturebeat/SZYF",
        "https://feeds.feedburner.com/arstechnica/index"
    ]
    
    print("Newsletter Generator - RSS Feed Parser with AI Processing")
    print("=" * 60)
    
    # Fetch articles from all feeds
    articles = fetch_rss_feeds(sample_feeds)
    
    if not articles:
        print("No articles were retrieved. Please check your feed URLs and internet connection.")
        return
    
    # Load Gemini API key from environment variable or .env file
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        print("Warning: GEMINI_API_KEY not found. AI processing will be skipped.")
        print("\nTo enable AI processing, set your Gemini API key using one of these methods:")
        print()
        print("Method 1 - Edit .env file (Recommended):")
        print("   1. Open the .env file in this directory")
        print("   2. Replace 'your-api-key-here' with your actual API key")
        print("   3. Save the file and run this script again")
        print()
        print("Method 2 - Set environment variable (Windows PowerShell):")
        print("   $env:GEMINI_API_KEY='your-api-key-here'")
        print()
        print("Method 3 - Set environment variable (Windows Command Prompt):")
        print("   set GEMINI_API_KEY=your-api-key-here")
        print()
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        
        # Save articles without AI processing
        save_articles_to_file(articles, "newsletter_articles.txt")
        print(f"\nArticles saved to 'newsletter_articles.txt' (without AI processing)")
        return
    
    # Initialize NewsProcessor with Gemini API
    try:
        news_processor = NewsProcessor(gemini_api_key)
        
        # Process articles with AI summarization, scoring, and deduplication
        print(f"\nProcessing up to 50 articles with Gemini AI (scoring and sorting by relevance)...")
        processed_articles = news_processor.process_articles(articles, max_articles=50)
        
        if processed_articles:
            # Display results
            print(f"\n📰 Top {len(processed_articles)} Articles (Sorted by Score)")
            print("=" * 80)
            
            for i, article in enumerate(processed_articles[:10], 1):  # Show top 10 articles
                score = article.get('score', 0)
                print(f"\n🏆 #{i} (Score: {score:.1f}/10)")
                print(f"📰 {article['title']}")
                print(f"📡 Source: {article['source']}")
                print(f"🔗 Link: {article['link']}")
                if article.get('llm_summary'):
                    print(f"🤖 AI Summary: {article['llm_summary']}")
                print("-" * 60)
            
            if len(processed_articles) > 10:
                print(f"\n... and {len(processed_articles) - 10} more articles")
            
            # Show score statistics
            scores = [article.get('score', 0) for article in processed_articles]
            avg_score = sum(scores) / len(scores) if scores else 0
            print(f"\n📊 Score Statistics:")
            print(f"   Highest Score: {max(scores):.1f}/10")
            print(f"   Lowest Score: {min(scores):.1f}/10")
            print(f"   Average Score: {avg_score:.1f}/10")
            print(f"   Articles with score ≥8: {len([s for s in scores if s >= 8])}")
            print(f"   Articles with score ≥6: {len([s for s in scores if s >= 6])}")
            
            # Save to file
            save_articles_to_file(processed_articles, "newsletter_articles_ai.txt")
            print(f"\nAI-processed articles saved to 'newsletter_articles_ai.txt'")
            
        else:
            print("No articles were successfully processed.")
            
    except Exception as e:
        logger.error(f"Error with AI processing: {str(e)}")
        print("AI processing failed. Saving articles without AI processing...")
        save_articles_to_file(articles, "newsletter_articles.txt")
        print(f"\nArticles saved to 'newsletter_articles.txt' (without AI processing)")


def save_articles_to_file(articles: List[Dict], filename: str):
    """
    Save articles to a text file for easy reading.
    
    Args:
        articles: List of article dictionaries
        filename: Output filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Newsletter Articles - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Calculate statistics if scores are available
            scores = [article.get('score', 0) for article in articles if article.get('score')]
            if scores:
                avg_score = sum(scores) / len(scores)
                f.write(f"📊 Score Statistics:\n")
                f.write(f"   Highest Score: {max(scores):.1f}/10\n")
                f.write(f"   Lowest Score: {min(scores):.1f}/10\n")
                f.write(f"   Average Score: {avg_score:.1f}/10\n")
                f.write(f"   Articles with score ≥8: {len([s for s in scores if s >= 8])}\n")
                f.write(f"   Articles with score ≥6: {len([s for s in scores if s >= 6])}\n\n")
                f.write("=" * 80 + "\n\n")
            
            for i, article in enumerate(articles, 1):
                score = article.get('score', 0)
                if score > 0:
                    f.write(f"🏆 #{i} (Score: {score:.1f}/10)\n")
                else:
                    f.write(f"{i}.\n")
                f.write(f"📰 {article['title']}\n")
                f.write(f"📡 Source: {article['source']}\n")
                f.write(f"🔗 Link: {article['link']}\n")
                if article.get('llm_summary'):
                    f.write(f"🤖 AI Summary: {article['llm_summary']}\n")
                elif article.get('summary'):
                    f.write(f"📝 Summary: {article['summary']}\n")
                f.write("\n" + "-" * 60 + "\n\n")
        
        logger.info(f"Articles saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving articles to file: {str(e)}")


def example_usage():
    """
    Example of how to use the NewsProcessor class.
    """
    # Load API key from environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable")
        return
    
    # Initialize NewsProcessor
    processor = NewsProcessor(api_key)
    
    # Example articles
    sample_articles = [
        {
            'title': 'Sample Article 1',
            'link': 'https://example.com/article1',
            'summary': 'This is a sample article about technology and innovation in the modern world.',
            'source': 'Example News'
        },
        {
            'title': 'Sample Article 2',
            'link': 'https://example.com/article2',
            'summary': 'Another sample article discussing the latest developments in artificial intelligence.',
            'source': 'Tech News'
        }
    ]
    
    # Process articles
    processed = processor.process_articles(sample_articles)
    
    # Display results
    for article in processed:
        print(f"Title: {article['title']}")
        print(f"AI Summary: {article.get('llm_summary', 'No summary')}")
        print("-" * 40)


if __name__ == "__main__":
    main() 