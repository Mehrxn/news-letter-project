# Newsletter Generator Setup Guide

This guide will help you set up the Newsletter Generator with AI-powered article summarization using Google's Gemini API.

## 🚀 Quick Start

### 1. Install Dependencies

First, install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Get a Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (it will look like: `AIzaSyC...`)

### 3. Set Up the API Key

Choose one of these methods:

#### Method 1: Using the Setup Script (Recommended)
```bash
python setup_api_key.py YOUR_API_KEY_HERE
```

#### Method 2: Using the Batch File (Windows)
```cmd
set_api_key.bat YOUR_API_KEY_HERE
```

#### Method 3: Manual Environment Variable
```cmd
# For current session only:
set GEMINI_API_KEY=YOUR_API_KEY_HERE

# For permanent setup (run as Administrator):
setx GEMINI_API_KEY YOUR_API_KEY_HERE
```

### 4. Test the Setup

Run the test script to verify everything is working:

```bash
python test_ai_with_key.py
```

## 📰 Using the Newsletter Generator

### Basic Usage

Run the main newsletter generator:

```bash
python newsletter_generator.py
```

This will:
- Fetch articles from popular RSS feeds
- Generate AI summaries using Gemini
- Remove duplicate articles
- Save results to `newsletter_articles_ai.txt`

### Custom Feeds

Use the example script with your own RSS feeds:

```bash
python example_usage.py
```

Edit the `custom_feeds` list in `example_usage.py` to add your preferred news sources.

### AI Processing Only

Test just the AI processing with sample articles:

```bash
python test_ai_with_key.py
```

## 🔧 Troubleshooting

### "GEMINI_API_KEY environment variable not set"

**Solution**: Set your API key using one of the methods above.

### "API key test failed"

**Solutions**:
1. Check that your API key is correct
2. Ensure you have internet connectivity
3. Verify your API key has the necessary permissions
4. Try regenerating your API key

### "Module not found" errors

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Network errors when fetching RSS feeds

**Solutions**:
1. Check your internet connection
2. Some RSS feeds may be temporarily unavailable
3. Try different RSS feed URLs

## 📁 Project Structure

```
newsletter-generator/
├── newsletter_generator.py      # Main script with AI processing
├── example_usage.py            # Example with custom feeds
├── test_ai_with_key.py        # AI processing test
├── setup_api_key.py           # API key setup helper
├── set_api_key.bat            # Windows batch file for setup
├── requirements.txt            # Python dependencies
├── README.md                  # Original README
└── SETUP_GUIDE.md            # This setup guide
```

## 🎯 Features

- **RSS Feed Parsing**: Fetches articles from multiple RSS feeds
- **AI Summarization**: Uses Gemini AI to create concise summaries
- **Deduplication**: Removes duplicate articles automatically
- **Error Handling**: Robust error handling for network issues
- **Logging**: Detailed logging for debugging
- **Customizable**: Easy to add your own RSS feeds

## 📊 Output Files

- `newsletter_articles_ai.txt`: Articles with AI summaries
- `newsletter_articles.txt`: Articles without AI processing
- `newsletter_generator.log`: Detailed logs
- `test_ai_articles.txt`: Test results

## 🔒 Security Notes

- Never commit your API key to version control
- Use environment variables for API keys
- The API key in `test_ai_with_key.py` is for testing only

## 📞 Support

If you encounter issues:

1. Check the log file: `newsletter_generator.log`
2. Verify your API key is working
3. Test with the provided test scripts
4. Check your internet connection

## 🚀 Next Steps

After setup, you can:

1. Customize RSS feeds in `example_usage.py`
2. Modify the AI prompts in `newsletter_generator.py`
3. Add more RSS feeds to the sample list
4. Create custom output formats
5. Set up automated newsletter generation

Happy newsletter generating! 📰✨ 