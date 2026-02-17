"""
YouTube Recommender Skill

A skill for recommending YouTube videos based on topic and duration,
using either the YouTube Data API or Invidious instances.

Usage:
    import youtube_recommender
    videos = youtube_recommender.get_recommendations("python tutorial", "short")
    print(youtube_recommender.format_recommendation(videos[0]))
"""

from youtube_recommender import (
    get_recommendations,
    format_recommendation,
    calculate_score,
    format_duration,
    format_number,
    DURATION_FILTERS,
    YouTubeRecommenderError,
    APIKeyError,
    BackendError,
)

__all__ = [
    'get_recommendations',
    'format_recommendation',
    'calculate_score',
    'format_duration',
    'format_number',
    'DURATION_FILTERS',
    'YouTubeRecommenderError',
    'APIKeyError',
    'BackendError',
]

__version__ = '2.0.0'
__author__ = 'nanobot'
