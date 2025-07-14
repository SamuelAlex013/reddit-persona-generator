#!/usr/bin/env python3
"""
PersonaGenerator class for Reddit Persona Generator.
"""

from typing import Dict
import json

from reddit_scraper import RedditScraper
from persona_analyzer import PersonaAnalyzer


class PersonaGenerator:
    """Main class that orchestrates the persona generation process."""

    def __init__(self, reddit_config: Dict, google_api_key: str):
        """Initialize the persona generator."""
        self.scraper = RedditScraper(**reddit_config)
        self.analyzer = PersonaAnalyzer(google_api_key)

    def save_persona_as_txt(self, persona: dict, output_file: str):
        """Save persona as a professional, human-readable TXT report."""
        def section(title, content):
            return f"{title}\n{'='*len(title)}\n{content}\n"
        def bullets(items):
            return '\n'.join([f"- {item}" for item in items]) if items else "(none)"
        report = []
        # Demographics
        demo = persona.get('demographics', {})
        demo_str = f"Age: {demo.get('age', 'N/A')}\nGender: {demo.get('gender', 'N/A')}\nLocation: {demo.get('location', 'N/A')}\nOccupation: {demo.get('occupation', 'N/A')}"
        report.append(section("DEMOGRAPHICS", demo_str))
        # Traits
        report.append(section("TRAITS", bullets(persona.get('traits'))))
        # Motivations
        report.append(section("MOTIVATIONS", bullets(persona.get('motivations'))))
        # Personality
        report.append(section("PERSONALITY", bullets(persona.get('personality'))))
        # Behaviors & Habits
        report.append(section("BEHAVIORS & HABITS", bullets(persona.get('behaviors'))))
        # Frustrations
        report.append(section("FRUSTRATIONS", bullets(persona.get('frustrations'))))
        # Goals & Needs
        report.append(section("GOALS & NEEDS", bullets(persona.get('goals'))))
        # Key Quote
        report.append(section("KEY QUOTE", f'"{persona.get('key_quote', '')}"'))
        # Summary
        report.append(section("ANALYSIS SUMMARY", persona.get('summary', '')))
        # Citations
        citations = persona.get('citations', {})
        citations_str = '\n'.join([f"{k.title()}: {', '.join(v) if v else '(none)'}" for k, v in citations.items()])
        report.append(section("CITATIONS", citations_str))
        # Confidence & Data Quality
        report.append(section("CONFIDENCE LEVEL", persona.get('confidence', '')))
        report.append(section("DATA QUALITY", persona.get('data_quality', '')))
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

    def generate_persona(self, reddit_url: str, output_file: str = None) -> dict:
        """Generate a complete persona for a Reddit user using LLM JSON report."""
        try:
            username = self.scraper.extract_username(reddit_url)
            print(f"Generating persona for Reddit user: {username}")
            content = self.scraper.get_user_content(username)
            if not content:
                return {"error": f"No content found for user {username}"}
            print(f"Found {len(content)} posts/comments")
            # LLM generates the full persona report as JSON string
            report_json_str = self.analyzer.analyze_content(content, username)
            if not report_json_str or not report_json_str.strip().startswith('{'):
                print(f"LLM output was empty or not JSON: {report_json_str}")
                # Save raw output for debugging
                debug_file = f"persona/{username}_persona_raw.txt"
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(report_json_str or "<empty>")
                return {"error": "LLM output was empty or not JSON.", "raw_output_file": debug_file}
            try:
                persona = json.loads(report_json_str)
                # Check if content was blocked
                if persona.get('blocked', False):
                    print(f"Analysis blocked: {persona.get('error', 'Unknown reason')}")
                    return persona
            except json.JSONDecodeError as e:
                print(f"Error parsing LLM output as JSON: {e}")
                debug_file = f"persona/{username}_persona_raw.txt"
                with open(debug_file, 'w', encoding='utf-8') as f:
                    f.write(report_json_str)
                return {"error": "LLM output was not valid JSON.", "raw_output_file": debug_file}
            if output_file is None:
                output_file = f"persona/{username}_persona.txt"
            elif not output_file.startswith("persona/"):
                output_file = f"persona/{output_file}"
            # Save as professional TXT report
            self.save_persona_as_txt(persona, output_file)
            print(f"Professional persona report saved to: {output_file}")
            return persona
        except Exception as e:
            error_msg = f"Error generating persona: {e}"
            print(error_msg)
            return {"error": error_msg}
