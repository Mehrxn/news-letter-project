#!/usr/bin/env python3
"""
Setup script for Gemini API Key in .env file
This script helps you set up your API key in the .env file.
"""

import os
import sys

def setup_env_file():
    """Set up the .env file with the API key."""
    
    print("🔧 Setting up Gemini API Key in .env file")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# Gemini API Key\n")
            f.write("# Get your API key from: https://makersuite.google.com/app/apikey\n")
            f.write("GEMINI_API_KEY=your-api-key-here\n")
    
    # Read current .env file
    try:
        with open('.env', 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False
    
    # Check if API key is already set
    if 'GEMINI_API_KEY=your-api-key-here' in content or 'GEMINI_API_KEY=' in content:
        print("📝 Current .env file content:")
        print("-" * 30)
        print(content)
        print("-" * 30)
        
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
            # Update .env file with the provided API key
            new_content = content.replace('GEMINI_API_KEY=your-api-key-here', f'GEMINI_API_KEY={api_key}')
            if 'GEMINI_API_KEY=' in new_content and 'your-api-key-here' not in new_content:
                try:
                    with open('.env', 'w') as f:
                        f.write(new_content)
                    print(f"\n✅ API key updated in .env file: {api_key[:10]}...")
                    return True
                except Exception as e:
                    print(f"❌ Error updating .env file: {e}")
                    return False
            else:
                print("❌ Could not update API key. Please edit .env file manually.")
                return False
        else:
            print("\nTo set your API key, run:")
            print("   python setup_env.py YOUR_API_KEY_HERE")
            print("\nOr edit the .env file manually and replace 'your-api-key-here' with your actual API key.")
            return False
    else:
        print("✅ API key already set in .env file")
        return True

def test_api_key():
    """Test if the API key from .env file is working."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your-api-key-here':
            print("❌ No valid API key found in .env file")
            return False
        
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        
        # Simple test
        response = model.generate_content("Hello, this is a test.")
        if response.text:
            print("✅ API key is working correctly!")
            return True
        else:
            print("❌ API key test failed - no response received")
            return False
            
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

def main():
    """Main function to set up the API key."""
    if setup_env_file():
        print("\n🧪 Testing API key...")
        if test_api_key():
            print("\n🎉 Setup complete! You can now run:")
            print("   python newsletter_generator.py")
            print("   python example_usage.py")
        else:
            print("\n⚠️  API key set but test failed. Please check your key.")
    else:
        print("\n📝 Please set your API key and run this script again.")

if __name__ == "__main__":
    main() 