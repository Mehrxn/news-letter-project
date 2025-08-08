# Enhanced Newsletter Generator with AI Processing

A complete and robust Python newsletter generator that retrieves RSS feeds and processes articles using **Gemini AI** for intelligent summarization and deduplication.

## 🚀 New Features

### ✅ **AI-Powered Article Processing**
- **Gemini AI Integration**: Uses Google's Gemini 2.5 Flash model for intelligent article summarization
- **Professional Summaries**: Generates concise, informative one-paragraph summaries
- **Smart Deduplication**: Removes duplicate articles based on URL matching
- **Error Handling**: Graceful handling of API failures and network issues

### ✅ **NewsProcessor Class**
- **`__init__(api_key)`**: Initialize with Gemini API key
- **`_get_summary(article_text)`**: Private method for AI-powered summarization
- **`process_articles(raw_articles)`**: Public method for processing and deduplicating articles

## 📋 Requirements

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `feedparser==6.0.10` - RSS feed parsing
- `requests==2.31.0` - HTTP requests
- `google-generativeai==0.8.3` - Gemini AI integration

## 🔑 Setup

### 1. Get Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 2. Set Environment Variable

**Windows:**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY='your-api-key-here'
```

## 🎯 Usage Examples

### Basic Usage (with AI processing)
```python
from newsletter_generator import NewsProcessor, fetch_rss_feeds
import os

# Set up API key
api_key = os.getenv('GEMINI_API_KEY')

# Initialize processor
processor = NewsProcessor(api_key)

# Fetch articles from RSS feeds
feed_urls = [
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://feeds.feedburner.com/TechCrunch/"
]
raw_articles = fetch_rss_feeds(feed_urls)

# Process with AI
processed_articles = processor.process_articles(raw_articles)

# Display results
for article in processed_articles:
    print(f"Title: {article['title']}")
    print(f"AI Summary: {article['llm_summary']}")
    print("-" * 40)
```

### Run the Enhanced Script
```bash
python newsletter_generator.py
```

### Run AI Processor Example
```bash
python ai_news_processor_example.py
```

## 📊 Article Structure

**Input Articles:**
```python
{
    'title': 'Article Title',
    'link': 'https://example.com/article',
    'summary': 'Original article text...',
    'source': 'Source Name'
}
```

**Processed Articles (with AI):**
```python
{
    'title': 'Article Title',
    'link': 'https://example.com/article',
    'summary': 'Original article text...',
    'source': 'Source Name',
    'llm_summary': 'AI-generated concise summary...'
}
```

## 🔧 NewsProcessor Class Methods

### `__init__(api_key: str)`
Initializes the NewsProcessor with Gemini API key.

**Parameters:**
- `api_key` (str): Gemini API key for authentication

### `_get_summary(article_text: str) -> str`
Private method that generates AI summaries using Gemini.

**Parameters:**
- `article_text` (str): Full article text to summarize

**Returns:**
- `str`: Concise, professional summary

### `process_articles(raw_articles: List[Dict]) -> List[Dict]`
Public method that processes articles with AI summarization and deduplication.

**Parameters:**
- `raw_articles` (List[Dict]): List of article dictionaries

**Returns:**
- `List[Dict]`: Processed articles with AI summaries and duplicates removed

## 🛡️ Error Handling

The enhanced version includes comprehensive error handling:

- **API Failures**: Graceful handling of Gemini API errors
- **Network Issues**: Robust handling of connection problems
- **Missing Data**: Validation of required article fields
- **Rate Limiting**: Respectful delays between API calls
- **Fallback Mode**: Works without API key (basic processing only)

## 📁 File Structure

```
newsletter-generator/
├── newsletter_generator.py           # Main script with AI processing
├── ai_news_processor_example.py     # AI processor example
├── requirements.txt                  # Dependencies
├── README_ENHANCED.md              # This file
├── newsletter_articles.txt          # Basic output (no AI)
├── newsletter_articles_ai.txt       # AI-processed output
└── ai_processed_articles.txt        # Example AI output
```

## 🎨 Features

### ✅ **AI Summarization**
- Professional news summarizer prompt
- Concise, informative summaries
- Focus on key facts and context
- Clear, accurate, and engaging output

### ✅ **Smart Deduplication**
- URL-based duplicate detection
- Maintains original article order
- Keeps first occurrence of duplicates
- Logs duplicate removal for transparency

### ✅ **Enhanced Logging**
- Detailed processing progress
- API call status tracking
- Error reporting and debugging
- Performance metrics

### ✅ **Flexible Configuration**
- Environment variable for API key
- Graceful fallback without API key
- Configurable processing parameters
- Easy customization

## 🔄 Processing Flow

1. **Fetch Articles**: Retrieve from RSS feeds
2. **Validate Data**: Check required fields
3. **Remove Duplicates**: Based on article links
4. **AI Summarization**: Generate professional summaries
5. **Error Handling**: Graceful failure management
6. **Save Results**: Output to formatted files

## 🚨 Troubleshooting

### Common Issues

1. **API Key Not Set**
   ```
   Warning: GEMINI_API_KEY environment variable not set
   ```
   **Solution**: Set the environment variable with your API key

2. **API Rate Limits**
   ```
   Error generating summary with Gemini API
   ```
   **Solution**: The script includes delays between calls to respect rate limits

3. **Network Issues**
   ```
   Network error fetching feed
   ```
   **Solution**: Check internet connection and feed URLs

### Debug Mode
Check the log file for detailed information:
```bash
tail -f newsletter_generator.log
```

## 📈 Performance

- **Processing Speed**: ~0.5 seconds per article (with API delays)
- **Deduplication**: O(n) time complexity
- **Memory Usage**: Efficient handling of large article sets
- **API Efficiency**: Respectful rate limiting and error handling

## 🔮 Future Enhancements

- **Batch Processing**: Process multiple articles simultaneously
- **Custom Prompts**: Configurable AI summarization prompts
- **Content Filtering**: Topic-based article filtering
- **Export Formats**: JSON, XML, and email-friendly formats
- **Scheduling**: Automated daily/weekly processing

## 📄 License

This project is open source and available under the MIT License.

---

**Ready to use?** Set your `GEMINI_API_KEY` and run `python newsletter_generator.py` to get started with AI-powered news processing! 