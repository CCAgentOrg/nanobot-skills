#!/usr/bin/env python3
"""
X (Twitter) Posting Module
"""

import os
import tweepy
import requests
from pathlib import Path
from typing import Optional, List, Dict, Any


def get_client() -> tweepy.Client:
    """
    Get an authenticated tweepy client.

    Returns:
        tweepy.Client: Authenticated client

    Raises:
        ValueError: If credentials are not set
    """
    api_key = os.environ.get("X_API_KEY")
    api_secret = os.environ.get("X_API_SECRET")
    access_token = os.environ.get("X_ACCESS_TOKEN")
    access_token_secret = os.environ.get("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise ValueError(
            "Missing X API credentials. Set X_API_KEY, X_API_SECRET, "
            "X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET environment variables."
        )

    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )


def post_tweet(
    text: str,
    image_path: Optional[str] = None,
    reply_to: Optional[int] = None
) -> Dict[str, Any]:
    """
    Post a tweet to X.

    Args:
        text: Tweet text (max 280 characters)
        image_path: Optional path to image file
        reply_to: Optional tweet ID to reply to

    Returns:
        Dict with tweet id and url
    """
    client = get_client()

    # Check character limit
    if len(text) > 280:
        raise ValueError(f"Tweet text too long: {len(text)} characters (max 280)")

    media_ids = []
    if image_path:
        # Need to use v1.1 API for media upload
        api = tweepy.API(
            tweepy.OAuth1UserHandler(
                os.environ["X_ACCESS_TOKEN"],
                os.environ["X_ACCESS_TOKEN_SECRET"],
                os.environ["X_API_KEY"],
                os.environ["X_API_SECRET"]
            )
        )
        media = api.media_upload(filename=image_path)
        media_ids.append(media.media_id)

    # Post the tweet
    response = client.create_tweet(
        text=text,
        media_ids=media_ids or None,
        in_reply_to_tweet_id=reply_to
    )

    tweet_id = response.data["id"]
    return {
        "id": tweet_id,
        "url": f"https://x.com/i/web/status/{tweet_id}"
    }


def post_thread(tweets: List[str]) -> List[Dict[str, Any]]:
    """
    Post a thread of connected tweets.

    Args:
        tweets: List of tweet texts

    Returns:
        List of tweet dicts with id and url
    """
    if not tweets:
        raise ValueError("Tweet list cannot be empty")

    if len(tweets) > 25:
        raise ValueError("Thread too long: max 25 tweets")

    results = []
    previous_tweet_id = None

    for i, text in enumerate(tweets):
        if len(text) > 280:
            raise ValueError(f"Tweet {i+1} too long: {len(text)} characters")

        client = get_client()

        if previous_tweet_id:
            response = client.create_tweet(
                text=text,
                in_reply_to_tweet_id=previous_tweet_id
            )
        else:
            response = client.create_tweet(text=text)

        tweet_id = response.data["id"]
        previous_tweet_id = tweet_id
        results.append({
            "id": tweet_id,
            "url": f"https://x.com/i/web/status/{tweet_id}"
        })

    return results


def delete_tweet(tweet_id: int) -> bool:
    """
    Delete a tweet by ID.

    Args:
        tweet_id: Tweet ID to delete

    Returns:
        True if successful
    """
    client = get_client()
    client.delete_tweet(tweet_id)
    return True


def get_tweet(tweet_id: int) -> Dict[str, Any]:
    """
    Get a tweet by ID.

    Args:
        tweet_id: Tweet ID to fetch

    Returns:
        Dict with tweet data
    """
    client = get_client()
    response = client.get_tweet(tweet_id)
    return response.data


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python poster.py <text> [--image <path>] [--reply <id>]")
        sys.exit(1)

    text = sys.argv[1]
    image_path = None
    reply_to = None

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--image" and i + 1 < len(sys.argv):
            image_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--reply" and i + 1 < len(sys.argv):
            reply_to = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    try:
        result = post_tweet(text, image_path=image_path, reply_to=reply_to)
        print(f"✅ Posted: {result['url']}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
