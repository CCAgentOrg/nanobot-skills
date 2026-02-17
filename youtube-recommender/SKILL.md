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

## How to Execute

1. **Check API Key**: Ensure `YOUTUBE_API_KEY` environment variable is set
   - The script should auto-detect this from shell environment
   - If not set, inform the user they need to set it

2. **Run the Script**: Execute using Python:
   ```bash
   cd ~/.nanobot/workspace/skills/youtube-recommender
   python youtube_recommender.py "<topic>" "<duration>"
   ```

3. **Return Results**: Present the full output to the user, including:
   - Video title and channel
   - Duration and view count
   - Explanation of why this video was recommended
   - Direct YouTube link

## Output Format

The script will return structured output with emojis:
- 🎬 Top Pick (title)
- 📺 Channel
- ⏱️ Duration
- 👀 Views
- 📅 Posted date
- 📝 Why this video (explanation)
- 🔗 Watch link

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
   echo 'export YOUTUBE_API_KEY="their-key"' >> ~/.bashrc
   source ~/.bashrc
   ```
3. For API quota issues, suggest waiting or using Invidious backend

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
