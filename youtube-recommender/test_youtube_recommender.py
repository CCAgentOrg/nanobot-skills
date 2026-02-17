#!/usr/bin/env python3
"""
Unit tests for YouTube Recommender Skill
Tests use mocked API responses - no actual API calls required.
"""

import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import youtube_recommender


class TestDurationFiltering(unittest.TestCase):
    """Test duration filter configuration."""

    def test_duration_filters_exist(self):
        """Test that all duration filters are configured."""
        self.assertIn('tiny', youtube_recommender.DURATION_FILTERS)
        self.assertIn('short', youtube_recommender.DURATION_FILTERS)
        self.assertIn('long', youtube_recommender.DURATION_FILTERS)

    def test_tiny_duration_range(self):
        """Test tiny duration filter (0-300 seconds)."""
        tiny = youtube_recommender.DURATION_FILTERS['tiny']
        self.assertEqual(tiny['min'], 0)
        self.assertEqual(tiny['max'], 300)

    def test_short_duration_range(self):
        """Test short duration filter (300-1200 seconds)."""
        short = youtube_recommender.DURATION_FILTERS['short']
        self.assertEqual(short['min'], 300)
        self.assertEqual(short['max'], 1200)

    def test_long_duration_range(self):
        """Test long duration filter (1200+ seconds)."""
        long = youtube_recommender.DURATION_FILTERS['long']
        self.assertEqual(long['min'], 1200)
        self.assertIsNone(long['max'])


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""

    def test_format_duration_minutes_seconds(self):
        """Test formatting duration under 1 hour."""
        result = youtube_recommender.format_duration(366)  # 6:06
        self.assertEqual(result, '6:06')

    def test_format_duration_hours_minutes(self):
        """Test formatting duration over 1 hour."""
        result = youtube_recommender.format_duration(3900)  # 1h 5m
        self.assertEqual(result, '1h 5m')

    def test_format_number_kilo(self):
        """Test formatting numbers in thousands."""
        self.assertEqual(youtube_recommender.format_number(1500), '1.5K')
        self.assertEqual(youtube_recommender.format_number(99900), '99.9K')

    def test_format_number_million(self):
        """Test formatting numbers in millions."""
        self.assertEqual(youtube_recommender.format_number(2500000), '2.5M')
        self.assertEqual(youtube_recommender.format_number(15000000), '15.0M')

    def test_format_number_small(self):
        """Test formatting small numbers."""
        self.assertEqual(youtube_recommender.format_number(500), '500')
        self.assertEqual(youtube_recommender.format_number(42), '42')

    def test_get_view_tier(self):
        """Test view tier categorization."""
        self.assertEqual(youtube_recommender.get_view_tier(2000000), 'Massive')
        self.assertEqual(youtube_recommender.get_view_tier(500000), 'High')
        self.assertEqual(youtube_recommender.get_view_tier(50000), 'Moderate')
        self.assertEqual(youtube_recommender.get_view_tier(5000), 'Niche')


class TestScoringAlgorithm(unittest.TestCase):
    """Test the video scoring algorithm."""

    def test_score_high_views(self):
        """Test that higher views get higher scores."""
        viral = {'viewCount': 1000000, 'lengthSeconds': 600, 'published': '2026-02-01T00:00:00Z'}
        niche = {'viewCount': 1000, 'lengthSeconds': 600, 'published': '2026-02-01T00:00:00Z'}

        viral_score = youtube_recommender.calculate_score(viral)
        niche_score = youtube_recommender.calculate_score(niche)

        self.assertGreater(viral_score, niche_score)

    def test_score_duration_bonus(self):
        """Test that medium duration (5-20 min) gets a bonus."""
        short = {'viewCount': 10000, 'lengthSeconds': 180, 'published': '2026-02-01T00:00:00Z'}
        medium = {'viewCount': 10000, 'lengthSeconds': 600, 'published': '2026-02-01T00:00:00Z'}
        long = {'viewCount': 10000, 'lengthSeconds': 2400, 'published': '2026-02-01T00:00:00Z'}

        short_score = youtube_recommender.calculate_score(short)
        medium_score = youtube_recommender.calculate_score(medium)
        long_score = youtube_recommender.calculate_score(long)

        # Medium should be higher than short and long
        self.assertGreater(medium_score, short_score)
        self.assertGreater(medium_score, long_score)

    def test_score_returns_float(self):
        """Test that score is always a float."""
        video = {'viewCount': 10000, 'lengthSeconds': 600, 'published': '2026-02-01T00:00:00Z'}
        score = youtube_recommender.calculate_score(video)
        self.assertIsInstance(score, (int, float))


class TestGetRecommendations(unittest.TestCase):
    """Test the get_recommendations function."""

    @patch('youtube_recommender.search_youtube')
    def test_get_recommendations_filters_by_duration(self, mock_search):
        """Test that results are filtered by duration."""
        # Mock response with videos of various lengths
        mock_search.return_value = [
            {'videoId': '1', 'title': 'Tiny', 'author': 'Channel A', 'lengthSeconds': 180,
             'viewCount': 10000, 'likeCount': 500, 'published': '2026-02-01T00:00:00Z'},
            {'videoId': '2', 'title': 'Short', 'author': 'Channel B', 'lengthSeconds': 600,
             'viewCount': 10000, 'likeCount': 500, 'published': '2026-02-01T00:00:00Z'},
            {'videoId': '3', 'title': 'Long', 'author': 'Channel C', 'lengthSeconds': 2400,
             'viewCount': 10000, 'likeCount': 500, 'published': '2026-02-01T00:00:00Z'},
        ]

        # Request short videos (300-1200 seconds)
        results = youtube_recommender.get_recommendations('test', 'short', backend='youtube')

        # Should only return the short video
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Short')

    @patch('youtube_recommender.search_youtube')
    def test_get_recommendations_sorts_by_score(self, mock_search):
        """Test that results are sorted by score."""
        mock_search.return_value = [
            {'videoId': '1', 'title': 'Low Score', 'author': 'Channel A', 'lengthSeconds': 600,
             'viewCount': 1000, 'likeCount': 50, 'published': '2026-01-01T00:00:00Z'},
            {'videoId': '2', 'title': 'High Score', 'author': 'Channel B', 'lengthSeconds': 600,
             'viewCount': 100000, 'likeCount': 5000, 'published': '2026-02-15T00:00:00Z'},
        ]

        results = youtube_recommender.get_recommendations('test', 'short', backend='youtube')

        # High score should be first
        self.assertEqual(results[0]['title'], 'High Score')
        self.assertEqual(results[1]['title'], 'Low Score')
        self.assertGreater(results[0]['score'], results[1]['score'])

    def test_get_recommendations_invalid_duration(self):
        """Test that invalid duration raises ValueError."""
        with self.assertRaises(ValueError) as context:
            youtube_recommender.get_recommendations('test', 'invalid')
        self.assertIn('Invalid duration', str(context.exception))

    @patch('youtube_recommender.search_youtube')
    def test_get_recommendations_num_results_limit(self, mock_search):
        """Test that num_results parameter limits output."""
        # Return 10 videos
        mock_search.return_value = [
            {'videoId': str(i), 'title': f'Video {i}', 'author': 'Channel', 'lengthSeconds': 600,
             'viewCount': 10000, 'likeCount': 500, 'published': '2026-02-01T00:00:00Z'}
            for i in range(10)
        ]

        # Request only 3 results
        results = youtube_recommender.get_recommendations('test', 'short', backend='youtube', num_results=3)

        self.assertEqual(len(results), 3)

    @patch('youtube_recommender.search_youtube')
    def test_get_recommendations_empty_results(self, mock_search):
        """Test that empty search returns empty list."""
        mock_search.return_value = []
        results = youtube_recommender.get_recommendations('test', 'short', backend='youtube')
        self.assertEqual(results, [])


class TestFormatRecommendation(unittest.TestCase):
    """Test the format_recommendation function."""

    def test_format_recommendation_basic(self):
        """Test basic recommendation formatting."""
        video = {
            'videoId': 'abc123',
            'title': 'Test Video',
            'author': 'Test Channel',
            'lengthSeconds': 600,
            'viewCount': 50000,
            'published': '2026-02-01T00:00:00Z'
        }

        result = youtube_recommender.format_recommendation(video, include_explanation=False)

        self.assertIn('Test Video', result)
        self.assertIn('Test Channel', result)
        self.assertIn('10:00', result)  # 600 seconds
        self.assertIn('50.0K', result)
        self.assertIn('abc123', result)
        self.assertNotIn('Why this video', result)

    def test_format_recommendation_with_explanation(self):
        """Test recommendation with explanation."""
        video = {
            'videoId': 'abc123',
            'title': 'Test Video',
            'author': 'Test Channel',
            'lengthSeconds': 600,
            'viewCount': 1500000,
            'published': '2026-02-01T00:00:00Z'
        }

        result = youtube_recommender.format_recommendation(video, include_explanation=True)

        self.assertIn('Why this video', result)
        self.assertIn('Viral hit', result)


class TestExceptions(unittest.TestCase):
    """Test custom exception classes."""

    def test_api_key_error(self):
        """Test APIKeyError exception."""
        exc = youtube_recommender.APIKeyError('No API key provided')
        self.assertIsInstance(exc, Exception)
        self.assertIsInstance(exc, youtube_recommender.YouTubeRecommenderError)
        self.assertIn('API key', str(exc))

    def test_backend_error(self):
        """Test BackendError exception."""
        exc = youtube_recommender.BackendError('Connection failed')
        self.assertIsInstance(exc, Exception)
        self.assertIsInstance(exc, youtube_recommender.YouTubeRecommenderError)
        self.assertIn('Connection failed', str(exc))


class TestYouTubeAPI(unittest.TestCase):
    """Test YouTube API functionality with mocks."""

    @patch('youtube_recommender.make_request')
    def test_search_youtube_parses_duration_pt5m30s(self, mock_request):
        """Test parsing PT5M30S duration format."""
        mock_request.side_effect = [
            # Search response
            {
                'items': [
                    {
                        'id': {'videoId': 'test123'},
                        'snippet': {
                            'title': 'Test Video',
                            'channelTitle': 'Test Channel',
                            'publishedAt': '2026-02-01T00:00:00Z'
                        }
                    }
                ]
            },
            # Videos response with PT5M30S (5 min 30 sec)
            {
                'items': [
                    {
                        'statistics': {'viewCount': '10000', 'likeCount': '500'},
                        'contentDetails': {'duration': 'PT5M30S'}
                    }
                ]
            }
        ]

        videos = youtube_recommender.search_youtube('test', youtube_recommender.DURATION_FILTERS['short'])
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0]['lengthSeconds'], 330)  # 5*60 + 30

    @patch('youtube_recommender.make_request')
    def test_search_youtube_parses_duration_pt1h30m(self, mock_request):
        """Test parsing PT1H30M duration format."""
        mock_request.side_effect = [
            {
                'items': [
                    {
                        'id': {'videoId': 'test123'},
                        'snippet': {
                            'title': 'Test Video',
                            'channelTitle': 'Test Channel',
                            'publishedAt': '2026-02-01T00:00:00Z'
                        }
                    }
                ]
            },
            {
                'items': [
                    {
                        'statistics': {'viewCount': '10000', 'likeCount': '500'},
                        'contentDetails': {'duration': 'PT1H30M'}
                    }
                ]
            }
        ]

        videos = youtube_recommender.search_youtube('test', youtube_recommender.DURATION_FILTERS['long'])
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0]['lengthSeconds'], 5400)  # 1*3600 + 30*60

    @patch('youtube_recommender.make_request')
    def test_search_youtube_parses_duration_pt30s(self, mock_request):
        """Test parsing PT30S duration format."""
        mock_request.side_effect = [
            {
                'items': [
                    {
                        'id': {'videoId': 'test123'},
                        'snippet': {
                            'title': 'Test Video',
                            'channelTitle': 'Test Channel',
                            'publishedAt': '2026-02-01T00:00:00Z'
                        }
                    }
                ]
            },
            {
                'items': [
                    {
                        'statistics': {'viewCount': '10000', 'likeCount': '500'},
                        'contentDetails': {'duration': 'PT30S'}
                    }
                ]
            }
        ]

        videos = youtube_recommender.search_youtube('test', youtube_recommender.DURATION_FILTERS['tiny'])
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0]['lengthSeconds'], 30)


class TestInvidiousAPI(unittest.TestCase):
    """Test Invidious API functionality with mocks."""

    @patch('youtube_recommender.make_request')
    def test_search_invidious(self, mock_request):
        """Test Invidious search with mocked response."""
        mock_request.return_value = [
            {
                'type': 'video',
                'videoId': 'test123',
                'title': 'Test Video',
                'author': 'Test Channel',
                'lengthSeconds': 600,
                'viewCount': 10000,
                'likeCount': 500,
                'published': 1706659200  # Unix timestamp
            },
            {
                'type': 'playlist',  # Should be ignored
                'title': 'Playlist'
            }
        ]

        videos = youtube_recommender.search_invidious('test', youtube_recommender.DURATION_FILTERS['short'])
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0]['title'], 'Test Video')
        self.assertEqual(videos[0]['author'], 'Test Channel')


class TestIntegration(unittest.TestCase):
    """Integration tests for common workflows."""

    @patch('youtube_recommender.search_youtube')
    def test_full_recommendation_workflow(self, mock_search):
        """Test complete workflow from search to formatting."""
        mock_search.return_value = [
            {
                'videoId': 'abc123',
                'title': 'Learn Python in 10 Minutes',
                'author': 'Code Academy',
                'lengthSeconds': 600,
                'viewCount': 150000,
                'likeCount': 8000,
                'published': '2026-02-10T00:00:00Z'
            },
            {
                'videoId': 'def456',
                'title': 'Python Basics',
                'author': 'Tech Tutorials',
                'lengthSeconds': 300,
                'viewCount': 50000,
                'likeCount': 2000,
                'published': '2026-02-15T00:00:00Z'
            }
        ]

        # Get recommendations
        results = youtube_recommender.get_recommendations('python tutorial', 'short', backend='youtube')

        # Verify results
        self.assertEqual(len(results), 2)
        self.assertTrue(all('score' in r for r in results))

        # Format the top recommendation
        formatted = youtube_recommender.format_recommendation(results[0])

        # Verify format includes all required elements
        self.assertIn('Learn Python', formatted)
        self.assertIn('Code Academy', formatted)
        self.assertIn('10:00', formatted)
        self.assertIn('abc123', formatted)


if __name__ == '__main__':
    unittest.main()
