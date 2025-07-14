#!/usr/bin/env python3
"""
RedditScraper class for Reddit Persona Generator.
"""

import re
from typing import List

import praw

from models import RedditPost


class RedditScraper:
    """Handles Reddit API interactions and data scraping."""

    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        """Initialize Reddit API client."""
        try:
            # Simple PRAW initialization without extra parameters
            self.reddit = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Reddit API: {e}")

    def extract_username(self, url: str) -> str:
        """Extract username from Reddit URL."""
        # Check if it's a subreddit URL instead of user URL
        if '/r/' in url:
            raise ValueError(
                f"Provided URL is a subreddit, not a user profile. "
                f"Please use a user URL like: "
                f"https://www.reddit.com/user/username/"
            )

        patterns = [
            r'reddit\.com/user/([^/]+)',
            r'reddit\.com/u/([^/]+)',
            r'www\.reddit\.com/user/([^/]+)',
            r'www\.reddit\.com/u/([^/]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        raise ValueError(
            f"Could not extract username from URL: {url}. "
            f"Please use format: https://www.reddit.com/user/username/"
        )

    def get_user_content(self, username: str, limit: int = 100) -> List[RedditPost]:
        """Scrape user's posts and comments."""
        try:
            user = self.reddit.redditor(username)
            content = []
            for submission in user.submissions.new(limit=limit):
                content.append(RedditPost(
                    id=submission.id,
                    title=submission.title,
                    content=submission.selftext or "",
                    subreddit=str(submission.subreddit),
                    score=submission.score,
                    created_utc=submission.created_utc,
                    permalink=f"https://reddit.com{submission.permalink}",
                    post_type="post"
                ))
            for comment in user.comments.new(limit=limit):
                content.append(RedditPost(
                    id=comment.id,
                    title="",
                    content=comment.body,
                    subreddit=str(comment.subreddit),
                    score=comment.score,
                    created_utc=comment.created_utc,
                    permalink=f"https://reddit.com{comment.permalink}",
                    post_type="comment"
                ))
            return content
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg:
                print(f"Error scraping user content: {e}")
                print("\n🔧 TROUBLESHOOTING 401 ERROR:")
                print("This usually means Reddit API authentication issues.")
                print("Please check:")
                print("1. Your Reddit app type is set to 'script' (not 'web app')")
                print("2. Your Client ID and Secret are correct")
                print("3. Your Reddit account is verified (email confirmed)")
                print("4. The user profile exists and is public")
                print("\nRun 'python reddit_setup_guide.py' for detailed setup instructions.")
            elif "403" in error_msg:
                print(f"Error scraping user content: {e}")
                print("\n🔒 The user profile may be private or the account is suspended.")
            elif "404" in error_msg:
                print(f"Error scraping user content: {e}")
                print(f"\n❌ User '{username}' not found. Please check the username.")
            else:
                print(f"Error scraping user content: {e}")
            return []