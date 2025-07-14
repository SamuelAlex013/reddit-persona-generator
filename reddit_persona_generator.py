#!/usr/bin/env python3
"""
Reddit Persona Generator.

Main entry point for generating a Reddit user persona.
"""

import argparse
import sys

from config_utils import load_config
from persona_generator import PersonaGenerator


def main():
    """Main function to run the persona generator."""
    parser = argparse.ArgumentParser(
        description='Generate user persona from Reddit profile'
    )
    parser.add_argument('reddit_url', help='Reddit user profile URL')
    parser.add_argument('-o', '--output', help='Output file name (optional)')
    args = parser.parse_args()

    try:
        reddit_config, google_api_key = load_config()
        generator = PersonaGenerator(reddit_config, google_api_key)
        generator.generate_persona(args.reddit_url, args.output)
        print("\nPersona generation completed!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()