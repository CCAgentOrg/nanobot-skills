#!/usr/bin/env python3
"""
YouTube Recommender Skill
Supports multiple backends: Invidious or YouTube Data API
Usage: python youtube_recommender.py "<topic>" "<duration>"

Backend selection via environment variable:
- YOUTUBE_API_KEY="..." - Use official YouTube API (default if set)
- BACKEND="invidious" - Use Invidious instances
"""

import os
import sys
import json
import time
import math
from urllib.parse import urlencode
from urllib.request import urlopen, Request, URLError, HTTPError

# Duration filters (in seconds)
DURATION_FILTERS = {
    'tiny': {'min': 0, 'max': 300},      # < 5 minutes
    'short': {'min': 300, 'max': 1200}, # 5-20 minutes
    'long': {'min': 1200, 'max': None}  # 20+ minutes
}

# Invidious instances (updated list)
INVIDIOUS_INSTANCES = [
    'invidious.snopyta.org',
    'yewtu.be',
    'invidious.kavin.rocks',
    'invidious.namazso.eu',
    'inv.riverside.rocks'
]

# Config
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
BACKEND = os.environ.get('BACKEND', 'youtube' if YOUTUBE_API_KEY else 'invidious')
INVIDIOUS_INSTANCE = os.environ.get('INVIDIOUS_INSTANCE', 'invidious.snopyta.org')


def make_request(url):
    """Make HTTPS request with timeout."""
    req = Request(url)
    try:
        with urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = response.read().decode('utf-8')
                try:
                    return json.loads(data)
                except json.JSONDecodeError as e:
                    raise Exception(f'JSON parse error: {e}')
            else:
                raise Exception(f'HTTP {response.status}: {response.reason}')
    except HTTPError as e:
        raise Exception(f'HTTP {e.code}: {e.reason}')
    except URLError as e:
        raise Exception(f'Connection error: {e.reason}')
    except Exception as e:
        raise Exception(str(e))


# ==================== YouTube Data API ====================
def search_youtube(query, duration_filter):
    """Search using YouTube Data API."""
    print(f'📡 Using YouTube Data API')

    # Map duration to YouTube API parameter
    video_duration = 'any'
    if duration == 'long':
        video_duration = 'long'
    elif duration == 'tiny':
        video_duration = 'short'

    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 25,
        'order': 'relevance',
        'videoDuration': video_duration,
        'key': YOUTUBE_API_KEY
    }

    url = f'https://www.googleapis.com/youtube/v3/search?{urlencode(params)}'
    search_result = make_request(url)

    if not search_result.get('items') or len(search_result['items']) == 0:
        return []

    # Get video IDs
    video_ids = ','.join([
        item['id']['videoId']
        for item in search_result['items']
        if item['id'].get('videoId')
    ])

    if not video_ids:
        return []

    # Get video statistics
    params = {
        'part': 'statistics,contentDetails',
        'id': video_ids,
        'key': YOUTUBE_API_KEY
    }
    url = f'https://www.googleapis.com/youtube/v3/videos?{urlencode(params)}'
    videos_result = make_request(url)

    videos = []
    for i, item in enumerate(search_result['items']):
        stats = None
        if videos_result.get('items') and i < len(videos_result['items']):
            stats = videos_result['items'][i]

        if not stats or not stats.get('statistics'):
            continue

        views = int(stats['statistics'].get('viewCount', 0))
        likes = int(stats['statistics'].get('likeCount', 0))

        # Parse duration
        duration_str = stats['contentDetails']['duration']
        hours = minutes = seconds = 0
        if 'H' in duration_str:
            hours = int(duration_str.split('H')[0].replace('PT', ''))
            duration_str = duration_str.split('H')[1]
        if 'M' in duration_str:
            minutes = int(duration_str.split('M')[0].replace('T', ''))
            duration_str = duration_str.split('M')[1]
        if 'S' in duration_str:
            seconds = int(duration_str.split('S')[0].replace('T', '').replace('PT', ''))

        total_seconds = (hours * 3600) + (minutes * 60) + seconds

        videos.append({
            'videoId': item['id']['videoId'],
            'title': item['snippet']['title'],
            'author': item['snippet']['channelTitle'],
            'lengthSeconds': total_seconds,
            'viewCount': views,
            'likeCount': likes,
            'published': item['snippet']['publishedAt']
        })

    return videos


# ==================== Invidious API ====================
def search_invidious(query, duration_filter, instance=None):
    """Search using Invidious API."""
    instance = instance or INVIDIOUS_INSTANCE
    print(f'📡 Using Invidious: {instance}')

    # Map duration to Invidious parameter
    duration_param = 'medium'
    if duration == 'long':
        duration_param = 'long'
    elif duration == 'tiny':
        duration_param = 'short'

    params = {
        'q': query,
        'type': 'video',
        'sort': 'relevance',
        'duration': duration_param
    }

    url = f'https://{instance}/api/v1/search?{urlencode(params)}'
    search_result = make_request(url)

    if not search_result or len(search_result) == 0:
        return []

    videos = []
    for item in search_result:
        if item.get('type') != 'video':
            continue

        videos.append({
            'videoId': item['videoId'],
            'title': item['title'],
            'author': item['author'],
            'lengthSeconds': item.get('lengthSeconds', 0),
            'viewCount': item.get('viewCount', 0),
            'likeCount': 0,
            'published': item.get('published')
        })

    return videos


# ==================== Common Functions ====================
def format_duration(seconds):
    """Format duration as human-readable string."""
    if seconds >= 3600:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        return f'{hours}h {mins}m'
    mins = seconds // 60
    secs = seconds % 60
    return f'{mins}:{secs:02d}'


def format_number(num):
    """Format large numbers with K/M suffixes."""
    if num >= 1000000:
        return f'{num / 1000000:.1f}M'
    if num >= 1000:
        return f'{num / 1000:.1f}K'
    return str(num)


def time_ago(timestamp):
    """Calculate relative time string."""
    try:
        # Handle ISO format or timestamp
        if isinstance(timestamp, str):
            from datetime import datetime
            published_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            timestamp_int = int(published_time.timestamp())
        else:
            timestamp_int = timestamp / 1000  # Assume milliseconds

        seconds_ago = int(time.time() - timestamp_int)

        if seconds_ago < 60:
            return 'just now'

        intervals = [
            ('year', 31536000),
            ('month', 2592000),
            ('week', 604800),
            ('day', 86400),
            ('hour', 3600)
        ]

        for label, interval_seconds in intervals:
            count = seconds_ago // interval_seconds
            if count >= 1:
                suffix = 's' if count > 1 else ''
                return f'{count} {label}{suffix} ago'

        return 'recently'
    except Exception:
        return 'recently'


def calculate_score(video):
    """Calculate recommendation score for a video."""
    views = video.get('viewCount', 0)
    seconds = video.get('lengthSeconds', 0)

    # View score (logarithmic)
    view_score = math.log10(views + 1) * 10

    # Duration bonus
    duration_bonus = 0
    if 300 <= seconds <= 1200:
        duration_bonus = 2

    # Recency bonus
    try:
        if isinstance(video['published'], str):
            from datetime import datetime
            published_time = datetime.fromisoformat(video['published'].replace('Z', '+00:00'))
            age_days = (time.time() - published_time.timestamp()) / 86400
        else:
            age_days = (time.time() * 1000 - video['published']) / (1000 * 86400)
        recency_bonus = max(0, 5 - age_days / 30)
    except Exception:
        recency_bonus = 0

    return view_score + duration_bonus + recency_bonus


def get_view_tier(views):
    """Categorize video by view count."""
    if views > 1000000:
        return 'Massive'
    if views > 100000:
        return 'High'
    if views < 10000:
        return 'Niche'
    return 'Moderate'


def generate_explanation(video, view_tier):
    """Generate explanation for why this video was recommended."""
    if view_tier == 'Massive':
        return f'Viral hit with {format_number(video["viewCount"])} views - proven popularity across YouTube.'
    if view_tier == 'High':
        return f'Strong viewership with {format_number(video["viewCount"])} views - well-regarded content in this niche.'
    if video['lengthSeconds'] < 300:
        return 'Concise and focused - perfect for quick learning on this topic.'
    return 'Top relevance match with good engagement for this specific topic.'


def print_recommendation(video):
    """Print formatted recommendation."""
    view_tier = get_view_tier(video['viewCount'])
    explanation = generate_explanation(video, view_tier)

    print(f'🎬 Top Pick: {video["title"]}')
    print(f'📺 Channel: {video["author"]}')
    print(f'⏱️ Duration: {format_duration(video["lengthSeconds"])}')
    print(f'👀 Views: {format_number(video["viewCount"])} ({view_tier})')
    print(f'📅 Posted: {time_ago(video["published"])}')
    print()
    print('📝 Why this video:')
    print(f'   {explanation}')
    print()
    print(f'🔗 Watch: https://youtube.com/watch?v={video["videoId"]}')
    if BACKEND == 'invidious':
        print(f'🔗 Invidious (ad-free): https://{INVIDIOUS_INSTANCE}/watch?v={video["videoId"]}')


# ==================== Main ====================
def recommend():
    """Main recommendation function."""
    global topic, duration

    # Parse arguments
    args = sys.argv[1:]

    if len(args) < 2:
        print('❌ Usage: python youtube_recommender.py "<topic>" "<duration>"')
        print('   Duration options: tiny, short, long')
        print()
        print('📌 Backend options:')
        print('   1. YouTube API (recommended): export YOUTUBE_API_KEY="your-key"')
        print('   2. Invidious: export BACKEND="invidious"')
        print()
        print('Get YouTube API key: https://console.cloud.google.com/')
        sys.exit(1)

    topic = args[0]
    duration = args[1].lower()

    if duration not in DURATION_FILTERS:
        print(f'❌ Invalid duration "{duration}". Use: tiny, short, or long')
        sys.exit(1)

    print(f'🔍 Searching for: "{topic}" ({duration} videos)\n')

    try:
        videos = []

        if BACKEND == 'invidious':
            # Try Invidious with fallback
            videos = search_invidious(topic, DURATION_FILTERS[duration])
        else:
            # Use YouTube Data API
            if not YOUTUBE_API_KEY:
                print('❌ YouTube Data API requires YOUTUBE_API_KEY environment variable')
                print('   Get one from: https://console.cloud.google.com/')
                print('   Or use Invidious: export BACKEND="invidious"')
                sys.exit(1)
            videos = search_youtube(topic, DURATION_FILTERS[duration])

        if not videos or len(videos) == 0:
            print(f'❌ No {duration} videos found for this topic')
            return

        # Filter by duration
        duration_filter = DURATION_FILTERS[duration]
        filtered = [
            v for v in videos
            if (not duration_filter['max'] or v['lengthSeconds'] <= duration_filter['max'])
            and v['lengthSeconds'] >= duration_filter['min']
        ]

        if len(filtered) == 0:
            print(f'❌ No {duration} videos found after filtering')
            return

        # Calculate scores and pick best
        scored = [{**v, 'score': calculate_score(v)} for v in filtered]
        scored.sort(key=lambda x: x['score'], reverse=True)

        print_recommendation(scored[0])

    except Exception as error:
        print(f'\n❌ Error: {error}')

        if BACKEND == 'invidious':
            print('\n💡 Tip: Try using YouTube Data API instead:')
            print('   export YOUTUBE_API_KEY="your-api-key"')
            print('   export BACKEND="youtube"')
        else:
            print('\n💡 Check your API key is valid and has YouTube Data API v3 enabled')
        sys.exit(1)


if __name__ == '__main__':
    recommend()
