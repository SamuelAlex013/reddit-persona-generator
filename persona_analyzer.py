#!/usr/bin/env python3
"""
PersonaAnalyzer class for Reddit Persona Generator.
"""

import google.generativeai as genai
from typing import List

from models import RedditPost


class PersonaAnalyzer:
    """Analyzes Reddit content to generate user personas using Gemini LLM."""

    def __init__(self, api_key: str):
        """Initialize Google Gemini client."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

    def analyze_content(self, content: List[RedditPost], username: str) -> str:
        """Analyze Reddit content and return a full persona report as text."""
        if not content:
            return "No Reddit content available for analysis."
        content_text = self._prepare_content_for_analysis(content)
        return self._generate_report_with_llm(content_text, username)

    def _prepare_content_for_analysis(self, content: List[RedditPost]) -> str:
        formatted_content = []
        for item in content[:50]:
            content_type = "POST" if item.post_type == "post" else "COMMENT"
            text = f"[{content_type}] r/{item.subreddit}"
            if item.title:
                text += f" - {item.title}"
            if item.content and item.content.strip():
                text += f"\nContent: {item.content[:500]}..."
            text += f"\nScore: {item.score}\nID: {item.id}\n---"
            formatted_content.append(text)
        return "\n".join(formatted_content)

    def _generate_report_with_llm(self, content_text: str, username: str) -> str:
        # Define the expected JSON schema for the persona
        persona_schema = {
            "demographics": {
                "age": "int or null",
                "gender": "str or null",
                "location": "str or null",
                "occupation": "str or null"
            },
            "traits": ["str"],
            "motivations": ["str"],
            "personality": ["str"],
            "behaviors": ["str"],
            "frustrations": ["str"],
            "goals": ["str"],
            "key_quote": "str",
            "summary": "str",
            "citations": {
                "demographics": ["str"],
                "traits": ["str"],
                "motivations": ["str"],
                "personality": ["str"],
                "behaviors": ["str"],
                "frustrations": ["str"],
                "goals": ["str"]
            },
            "confidence": "str",
            "data_quality": "str"
        }
        prompt = f"""
        You are an expert UX researcher and writer. Analyze the following Reddit posts and comments from user '{username}'
        and generate a professional, evidence-based persona as a strict JSON object.

        The JSON must follow this schema:
        {persona_schema}

        Instructions:
        - Only include details supported by specific evidence from the posts/comments.
        - For each field, cite the Reddit post/comment ID or permalink used for extraction.
        - Avoid generic or filler content; be specific and concise.
        - Do not include any text, explanations, or formatting outside the JSON object.
        - Return ONLY a valid JSON object, nothing else.
        - If you cannot infer a field, set it to null or an empty list.
        - Do not include any introductory or closing remarks.
        - Your response will be parsed by a strict JSON parser.

        Content to analyze:
        {content_text}
        """
        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                candidate_count=1
            )
        )
        # Clean up the response - remove markdown code block markers if present
        raw_output = response.text.strip()
        if raw_output.startswith('```json\n'):
            raw_output = raw_output[8:]  # Remove '```json\n'
        if raw_output.endswith('\n```'):
            raw_output = raw_output[:-4]  # Remove '\n```'
        elif raw_output.endswith('```'):
            raw_output = raw_output[:-3]  # Remove '```'
        return raw_output.strip()