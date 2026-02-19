# X (Twitter) Posting Skill

Post tweets to X (Twitter) from nanobot.

## Features

- Post simple text tweets
- Post tweets with images
- Post tweet threads (multiple connected tweets)
- Reply to existing tweets
- Delete tweets

## Setup

### 1. Get X API Credentials

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a free developer account (Basic tier)
3. Create a new app to get your credentials:
   - **API Key** (Consumer Key)
   - **API Secret** (Consumer Secret)
   - **Access Token** (OAuth 1.0a)
   - **Access Token Secret**

### 2. Install Dependencies

```bash
pip install tweepy requests
```

### 3. Configure Environment Variables

Add these to your shell config (`~/.bashrc`, `~/.zshrc`, or `.env`):

```bash
export X_API_KEY="your_api_key"
export X_API_SECRET="your_api_secret"
export X_ACCESS_TOKEN="your_access_token"
export X_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

Then reload your shell or run:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### 4. Verify Setup

Run the test script to verify your credentials:
```bash
python3 skills/x-poster/test.py
```

## Usage

### Post a simple text tweet

```python
from skills.x_poster.poster import post_tweet

result = post_tweet("Hello from nanobot! 🤖")
print(f"Tweeted: {result['id']}")
print(f"URL: {result['url']}")
```

### Post with an image

```python
from skills.x_poster.poster import post_tweet

result = post_tweet("Check this out!", image_path="/path/to/image.png")
print(f"Tweeted: {result['id']}")
```

### Post a thread (multiple tweets)

```python
from skills.x_poster.poster import post_thread

tweets = [
    "Thread Part 1/3 🧵",
    "Thread Part 2/3 - More content here",
    "Thread Part 3/3 - Fin! #nanobot"
]

results = post_thread(tweets)
for i, tweet in enumerate(results):
    print(f"Tweet {i+1}: {tweet['url']}")
```

### Reply to a tweet

```python
from skills.x_poster.poster import post_tweet

result = post_tweet("Thanks!", reply_to=1234567890)
print(f"Replied: {result['url']}")
```

### Delete a tweet

```python
from skills.x_poster.poster import delete_tweet

success = delete_tweet(1234567890)
print(f"Deleted: {success}")
```

## Limitations

- **API Tier**: Basic tier allows posting but has rate limits (300 tweets per 15 minutes for OAuth 1.0a)
- **Media**: Images must be under 5MB, GIFs under 15MB
- **Text**: Max 280 characters per tweet

## Troubleshooting

### "401 Unauthorized"
- Check your API credentials are correct
- Ensure your Access Token has write permissions

### "429 Too Many Requests"
- You've hit the rate limit. Wait 15 minutes before trying again.

### "413 Payload Too Large"
- Your media file is too large. Compress it first.

## References

- X API v2 Documentation: https://developer.twitter.com/en/docs/twitter-api
- Tweepy Documentation: https://docs.tweepy.org/
