#!/usr/bin/env python3
"""
Data models for Reddit Persona Generator.
"""

from dataclasses import dataclass


@dataclass
class RedditPost:
    """Data class for Reddit posts and comments."""
    id: str
    title: str
    content: str
    subreddit: str
    score: int
    created_utc: float
    permalink: str
    post_type: str  # 'post' or 'comment'