#!/usr/bin/env python3
"""
Test script for YouTube Recommender API connectivity.
Tests both YouTube Data API and Invidious backends.
"""

import os
import sys
from urllib.parse import urlencode
from urllib.request import urlopen, Request, URLError

# Test YouTube API key
def test_youtube_api():
    """Test YouTube Data API connectivity."""
    api_key = os.environ.get('YOUTUBE_API_KEY')

    if not api_key:
        print('⚠️  YOUTUBE_API_KEY not set in environment')
        print('   Set it with: export YOUTUBE_API_KEY="your-key"')
        return False

    print('📡 Testing YouTube Data API...')

    try:
        # Make a simple API call
        params = {
            'part': 'snippet',
            'q': 'test',
            'type': 'video',
            'maxResults': 1,
            'key': api_key
        }
        url = f'https://www.googleapis.com/youtube/v3/search?{urlencode(params)}'

        req = Request(url)
        with urlopen(req, timeout=10) as response:
            if response.status == 200:
                print('✅ YouTube Data API is working!')
                print(f'   API Key: {api_key[:10]}...{api_key[-4:]}')
                return True
            else:
                print(f'❌ API returned HTTP {response.status}')
                return False
    except Exception as e:
        print(f'❌ YouTube API test failed: {e}')
        return False


# Test Invidious instance
def test_invidious(instance='invidious.snopyta.org'):
    """Test Invidious instance connectivity."""
    print(f'📡 Testing Invidious instance: {instance}...')

    try:
        url = f'https://{instance}/api/v1/search?q=test&type=video'

        req = Request(url)
        with urlopen(req, timeout=10) as response:
            if response.status == 200:
                print(f'✅ Invidious instance is working!')
                return True
            else:
                print(f'❌ Invidious returned HTTP {response.status}')
                return False
    except Exception as e:
        print(f'❌ Invidious test failed: {e}')
        return False


# Main test function
def main():
    print('=' * 50)
    print('YouTube Recommender - API Test')
    print('=' * 50)
    print()

    # Test YouTube API
    youtube_ok = test_youtube_api()
    print()

    # Test Invidious
    invidious_ok = test_invidious()
    print()

    # Summary
    print('=' * 50)
    print('Summary')
    print('=' * 50)
    print(f'YouTube Data API: {"✅ Working" if youtube_ok else "❌ Failed"}')
    print(f'Invidious:        {"✅ Working" if invidious_ok else "❌ Failed"}')
    print()

    if youtube_ok:
        print('💡 Use: export BACKEND="youtube"')
    elif invidious_ok:
        print('💡 Use: export BACKEND="invidious"')
    else:
        print('❌ No backend available!')
        print('   Get a YouTube API key from: https://console.cloud.google.com/')


if __name__ == '__main__':
    main()
