#!/usr/bin/env python3
"""
Test X API credentials and connection.
"""

import os
import sys
import tweepy


def test_credentials():
    """Test X API credentials."""

    print("🔍 Testing X API credentials...")

    # Check environment variables
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

    missing = []
    if not api_key:
        missing.append("X_API_KEY")
    if not api_secret:
        missing.append("X_API_SECRET")
    if not access_token:
        missing.append("X_ACCESS_TOKEN")
    if not access_token_secret:
        missing.append("X_ACCESS_TOKEN_SECRET")

    if missing:
        print(f"❌ Missing environment variables: {', '.join(missing)}")
        print("\nSet them in your shell config:")
        print('export X_API_KEY="your_api_key"')
        print('export X_API_SECRET="your_api_secret"')
        print('export X_ACCESS_TOKEN="your_access_token"')
        print('export X_ACCESS_TOKEN_SECRET="your_access_token_secret"')
        return False

    print("✅ Environment variables set")

    # Try to create client and verify credentials
    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )

        # Get user info to verify credentials
        me = client.get_me()
        print(f"✅ Connected as: @{me.data.username}")
        print(f"✅ User ID: {me.data.id}")

        return True

    except tweepy.Unauthorized:
        print("❌ Unauthorized: Check your API credentials")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = test_credentials()
    sys.exit(0 if success else 1)
