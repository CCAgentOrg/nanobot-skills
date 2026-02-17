---
name: youtube_recommender
description: Recommends relevant YouTube videos for any topic, with duration filtering and engagement-based ranking.
---

# YouTube Recommender Skill

## When to Use This Skill

Use this skill when the user asks for:
- YouTube video recommendations for any topic
- Best videos for learning or entertainment
- Videos of specific durations (short, medium, long)
- Educational content, tutorials, or entertainment

## Commands

### `ytrec <topic> <duration>`

**Arguments:**
- `topic`: Search term (e.g., "machine learning", "guitar tutorial", "cooking pasta")
- `duration`: Video length preference
  - `tiny` - Less than 5 minutes
  - `short` - 5 to 20 minutes
  - `long` - 20+ minutes

**Example Usage:**
```bash
cd ~/.nanobot/workspace/skills/youtube-recommender
python youtube_recommender.py "react hooks tutorial" short
python youtube_recommender.py "space exploration" long
python youtube_recommender.py "cooking tips" tiny
```

## Python API

For programmatic use within nanobot or other Python code:

```python
import sys
sys.path.insert(0, '/home/ubuntu/.nanobot/workspace/skills/youtube-recommender')
import youtube_recommender

# Get recommendations
videos = youtube_recommender.get_recommendations(
    topic="python tutorial",
    duration="short",
    backend="youtube",  # or "invidious"
    num_results=5
)

# Format a video for display
formatted = youtube_recommender.format_recommendation(videos[0])
print(formatted)

# Access raw data
for video in videos:
    print(f"{video['title']} by {video['author']}")
    print(f"Score: {video['score']:.2f}")
    print(f"URL: https://youtube.com/watch?v={video['videoId']}")
```

### API Functions

#### `get_recommendations(topic, duration='short', backend=None, num_results=5)`
Returns a list of video dictionaries sorted by recommendation score.

**Parameters:**
- `topic` (str): Search query
- `duration` (str): 'tiny', 'short', or 'long' (default: 'short')
- `backend` (str): 'youtube' or 'invidious' (default: auto-detect)
- `num_results` (int): Number of videos to return (default: 5)

**Returns:**
- `list`: List of video dicts with keys: videoId, title, author, lengthSeconds, viewCount, likeCount, published, score

**Raises:**
- `ValueError`: Invalid duration parameter
- `APIKeyError`: YouTube API key missing or invalid
- `BackendError`: Backend failed to fetch results

#### `format_recommendation(video, include_explanation=True)`
Formats a video dictionary as a human-readable string.

**Parameters:**
- `video` (dict): Video data dict
- `include_explanation` (bool): Include "Why this video" section

**Returns:**
- `str`: Formatted recommendation string with emojis

## How to Execute

1. **Check API Key**: The script requires `YOUTUBE_API_KEY` environment variable
   - Auto-detects from shell environment
   - Get YouTube API key from: https://console.cloud.google.com/
   - Add to `~/.bashrc`:
     ```bash
     export YOUTUBE_API_KEY="your-api-key"
     source ~/.bashrc
     ```

2. **Run the Script**: Execute using Python:
   ```bash
   cd ~/.nanobot/workspace/skills/youtube-recommender
   python youtube_recommender.py "<topic>" "<duration>"
   ```

3. **Return Results**: Present the full output to the user, including:
   - Top Pick with title, channel, duration, views, and explanation
   - "Also worth watching" section with additional recommendations
   - Direct YouTube links

## Output Format

The script will return structured output with emojis:

**Top Pick:**
- 🎬 Title
- 📺 Channel name
- ⏱️ Duration
- 👀 Views
- 📅 Posted date
- 📝 Why this video (explanation)
- 🔗 Watch link

**Also worth watching:**
- 3 additional recommended videos
- Each with duration, view count, and link

## Security Notes

- The API key is loaded from the environment, never from files
- The script uses YouTube Data API v3 or Invidious
- No user input is directly executed as commands
- The search query is safely passed as arguments

## Troubleshooting

**If the script fails:**
1. Check if `YOUTUBE_API_KEY` is set: `echo $YOUTUBE_API_KEY`
2. If not set, instruct user to add to `~/.bashrc`:
   ```bash
   echo 'export YOUTUBE_API_KEY="your-api-key"' >> ~/.bashrc
   source ~/.bashrc
   ```
3. For API quota issues, suggest checking quota in Google Cloud Console
4. **Invidious backend is unreliable** - public instances frequently fail with 403/404 errors. Use YouTube API for reliable results.

**Duration Filters:**
- `tiny` = < 5 minutes (quick tips, overviews)
- `short` = 5-20 minutes (tutorials, explainers)
- `long` = 20+ minutes (deep dives, documentaries)

## Algorithm Notes

The recommendation uses a weighted scoring system:
- **View count** (logarithmic scaling - prevents viral-only results)
- **Duration bonus** (+2 for medium 5-20min videos)
- **Recency bonus** (slight boost for newer content)

This ensures a balance between popularity, content quality, and freshness.
