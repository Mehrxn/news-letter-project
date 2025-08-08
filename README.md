# Newsletter Generator - RSS Feed Parser

A complete and robust Python script that retrieves and parses RSS feeds using the `feedparser` library. The script includes comprehensive error handling for network requests and malformed feeds, and returns structured article data.

## Features

- **Robust Error Handling**: Gracefully handles network errors, malformed feeds, and parsing issues
- **Multiple Feed Formats**: Supports various RSS and Atom feed formats
- **Structured Output**: Returns clean, structured article data with title, link, summary, and source
- **Logging**: Comprehensive logging for debugging and monitoring
- **Rate Limiting**: Respectful delays between requests
- **File Output**: Saves articles to a readable text file

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the script directly to fetch articles from the included sample feeds:

```bash
python newsletter_generator.py
```

### Using the Function in Your Code

```python
from newsletter_generator import fetch_rss_feeds

# Define your RSS feed URLs
feed_urls = [
    "https://rss.cnn.com/rss/edition.rss",
    "https://feeds.bbci.co.uk/news/rss.xml",
    "https://www.reddit.com/r/Python/.rss"
]

# Fetch articles
articles = fetch_rss_feeds(feed_urls)

# Process the articles
for article in articles:
    print(f"Title: {article['title']}")
    print(f"Source: {article['source']}")
    print(f"Link: {article['link']}")
    print(f"Summary: {article['summary']}")
    print("-" * 50)
```

## Function Documentation

### `fetch_rss_feeds(feed_urls, timeout=30)`

Fetches and parses RSS feeds from a list of URLs.

**Parameters:**
- `feed_urls` (List[str]): List of RSS feed URLs to fetch
- `timeout` (int): Request timeout in seconds (default: 30)

**Returns:**
- `List[Dict]`: List of article dictionaries

**Article Dictionary Structure:**
```python
{
    'title': 'Article Title',
    'link': 'https://example.com/article',
    'summary': 'Article summary or description',
    'source': 'Source Name'
}
```

## Error Handling

The script includes comprehensive error handling for:

- **Network Errors**: Connection timeouts, DNS failures, HTTP errors
- **Malformed Feeds**: Invalid XML, missing required fields
- **Parsing Issues**: Bozo flags and parsing exceptions
- **Missing Data**: Articles without titles or links

## Output Files

- `newsletter_articles.txt`: Human-readable file with all retrieved articles
- `newsletter_generator.log`: Detailed log file with processing information

## Sample RSS Feeds

The script includes sample feeds for testing:
- CNN News
- BBC News
- Reddit r/Python
- TechCrunch
- The Verge

## Customization

### Adding Your Own Feeds

Replace the `sample_feeds` list in the `main()` function with your preferred RSS feed URLs:

```python
my_feeds = [
    "https://your-favorite-blog.com/feed",
    "https://news-site.com/rss",
    "https://tech-blog.com/feed.xml"
]
articles = fetch_rss_feeds(my_feeds)
```

### Modifying Output Format

You can customize the article processing by modifying the `extract_article_data()` function to include additional fields or change the output format.

## Requirements

- Python 3.6+
- feedparser==6.0.10
- requests==2.31.0

## Troubleshooting

### Common Issues

1. **No articles retrieved**: Check your internet connection and feed URLs
2. **Feed parsing errors**: Some feeds may have malformed XML - the script will log warnings but continue processing
3. **Network timeouts**: Increase the timeout parameter for slower feeds

### Logs

Check the `newsletter_generator.log` file for detailed information about:
- Feed fetching progress
- Parsing errors and warnings
- Network issues
- Processing statistics

## License

This project is open source and available under the MIT License. 