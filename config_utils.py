#!/usr/bin/env python3
"""
Configuration utilities for Reddit Persona Generator.
"""

import os
from typing import Dict, Tuple
from dotenv import load_dotenv
from pathlib import Path


def load_config() -> Tuple[Dict, str]:
    """Load configuration from environment variables and .env file."""
    # Load from .env file, overriding any existing env vars
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path, override=True)
    
    reddit_config = {
        'client_id': os.getenv('REDDIT_CLIENT_ID'),
        'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
        'user_agent': os.getenv('REDDIT_USER_AGENT', 'PersonaGenerator/1.0')
    }
    google_api_key = os.getenv('GOOGLE_API_KEY')
    
    if not all(reddit_config.values()):
        raise ValueError(
            "Reddit API configuration incomplete. Set REDDIT_CLIENT_ID, "
            "REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT in .env file."
        )
    if not google_api_key:
        raise ValueError(
            "Google API key required. Set GOOGLE_API_KEY in .env file."
        )
    return reddit_config, google_api_key
