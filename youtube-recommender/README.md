# YouTube Recommender

A CLI tool to recommend the most relevant YouTube videos based on topic, duration, and engagement metrics.

## ✨ Features

- **Dual Backend Support**: YouTube Data API or Invidious
- **Smart ranking**: Combines views, recency, and duration preferences
- **Duration filtering**: Find videos that fit your time budget (tiny/short/long)
- **Metric explanation**: Learn why a video was recommended
- **Fast results**: Direct API calls with efficient ranking

## 🚀 Installation

```bash
# Clone or copy this directory
cd youtube-recommender

# Make sure Python 3.8+ is installed
python --version

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Setup

### Option 1: YouTube Data API (Recommended)

**⚠️ Security First: Never store API keys in files! Use environment variables only.**

**Setup Steps:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project or select existing
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. **Important**: Restrict the API key for security:
   - Set **Application restrictions**: None (for CLI use)
   - Set **API restrictions**: Only YouTube Data API v3
6. Set environment variable:

```bash
export YOUTUBE_API_KEY="your-api-key-here"
```

**For persistent use**, add to your shell config:

```bash
# For bash
echo 'export YOUTUBE_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# For zsh
echo 'export YOUTUBE_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

**Security Best Practices:**
- ❌ **Never** commit `.env` files to git
- ❌ **Never** share API keys in messages, docs, or screenshots
- ✅ Use environment variables (shell config or runtime)
- ✅ Restrict API key in Google Cloud Console to specific APIs
- ✅ Rotate keys immediately if they're ever exposed
- ✅ Use separate keys for different environments

### Option 2: Invidious (No API Key)

```bash
export BACKEND="invidious"
```

Optionally specify an instance:
```bash
export INVIDIOUS_INSTANCE="invidious.snopyta.org"
```

**Pros**: No API key required, free, ad-free links
**Cons**: Public instances can be slow/unavailable, less reliable

## 📖 Usage

```bash
python youtube_recommender.py "<topic>" "<duration>"
```

### Duration Options

- `tiny` - Less than 5 minutes
- `short` - 5 to 20 minutes
- `long` - 20+ minutes

### Examples

```bash
# Short tutorial on React hooks
export YOUTUBE_API_KEY="your-key"
python youtube_recommender.py "react hooks tutorial" short

# Long documentary on space
python youtube_recommender.py "space exploration documentary" long

# Tiny quick tips for cooking
python youtube_recommender.py "cooking tips" tiny
```

## 📊 Output Example

```
🔍 Searching for: "machine learning basics" (short videos)
📡 Using YouTube Data API

🎬 Top Pick: Machine Learning in 10 Minutes
📺 Channel: Codecademy
⏱️ Duration: 10:24
👀 Views: 1.2M (Massive)
📅 Posted: 6 months ago

📝 Why this video:
   Viral hit with 1.2M views - proven popularity across YouTube.

🔗 Watch: https://youtube.com/watch?v=ukzFI9rgwfU
```

## 🧠 How It Works

1. **Search**: Query API for relevant videos
2. **Filter**: Remove videos that don't match duration preference
3. **Calculate Score**: Weighted combination of:
   - View count (logarithmic scaling)
   - Duration preference (medium-length bonus)
   - Recency (slight boost for newer content)
4. **Rank**: Sort by score and return top recommendation

### Scoring Algorithm

```
score = log10(views + 1) * 10      // View score (logarithmic)
      + durationBonus              // +2 for 5-20min videos
      + max(0, 5 - ageInDays/30)   // Recency bonus (up to +5)
```

## 🔐 Security

**API Key Management:**

✅ **Recommended**:
- Store in `~/.bashrc` or `~/.zshrc` (your shell config)
- Set as environment variable before running
- Use separate keys for dev/production
- Restrict key to specific APIs in Google Cloud Console
- Rotate keys periodically

❌ **Never**:
- Commit `.env` files to version control
- Share keys in messages, screenshots, or docs
- Store in plaintext files in workspace
- Embed keys in code

**Why environment variables?**
- Not stored in files in workspace
- Can be restricted in shell config permissions
- Can be rotated without changing code
- Separation of config and code

## 🔄 Backend Comparison

| Feature | YouTube API | Invidious |
|---------|-------------|-----------|
| API Key | Required | Not required |
| Reliability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Quota | 10,000 units/day | Unlimited |
| Cost | Free tier limited | Free |
| Setup Time | 5 minutes | 0 minutes |
| Ad-free Viewing | No | Yes |
| Security | ✅ With env vars | ⚠️ Public instances |

## 📝 Troubleshooting

### YouTube API Errors

**Error: "API key not valid"**
- Check your API key is correct
- Ensure YouTube Data API v3 is enabled in Google Cloud Console
- Verify API key restrictions allow YouTube Data API v3

**Error: "quotaExceeded"**
- You've hit your daily limit (10,000 units)
- Wait until quota resets or request higher quota in Google Cloud Console
- Each search costs ~125 units (100 for search + ~25 for video stats)

### Invidious Errors

**Error: "Connection refused" or timeout**
- Public instance is down or overloaded
- Try a different instance: `export INVIDIOUS_INSTANCE="invidious.kavin.rocks"`
- Consider using YouTube Data API for reliability

**Error: "HTTP 403" or "HTTP 429"**
- Instance has rate limiting or blocking
- Switch to YouTube Data API backend

## 🚧 Future Enhancements

- [ ] Support multiple recommendations (top 3, top 5)
- [ ] Filter by upload date (last week, last month)
- [ ] Support channel-specific search
- [ ] Add like ratio tracking
- [ ] Cache results for repeated queries
- [ ] Interactive mode with refine options

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `YOUTUBE_API_KEY` | - | **YouTube Data API key** (for backend="youtube") |
| `BACKEND` | `youtube` if API key set, else `invidious` | Which API to use |
| `INVIDIOUS_INSTANCE` | `invidious.snopyta.org` | Invidious instance to use |

## 📄 License

MIT

## 🙏 Credits

- **YouTube Data API** - Official Google API
- **Invidious** - Open-source YouTube frontend
- **nanobot** - Agent framework
