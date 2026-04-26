"""AI content generation – hooks and scripts using OpenAI."""

import os

from core.config import settings

try:
    from openai import OpenAI

    _client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
except Exception:
    _client = None


def generate_hooks(topic: str, count: int = 3) -> list[str]:
    """Generate A/B test hooks for a given topic.

    Falls back to template-based hooks when the OpenAI key is unavailable.
    """
    if _client and settings.OPENAI_API_KEY:
        try:
            response = _client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a viral content strategist. Generate short, "
                            "punchy hooks optimised for 3-second retention on TikTok / Reels."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Create {count} alternative hooks for this trending topic: {topic}. "
                            "Return only the hooks, one per line."
                        ),
                    },
                ],
                max_tokens=200,
                temperature=0.9,
            )
            hooks = [
                line.strip()
                for line in response.choices[0].message.content.strip().split("\n")
                if line.strip()
            ]
            return hooks[:count]
        except Exception:
            pass

    # Fallback: deterministic templates
    return [
        f"This changes everything for: {topic}",
        f"Nobody is talking about the truth behind: {topic}",
        f"Look at the numbers behind: {topic}",
    ]


def generate_script(hook: str, topic: str) -> str:
    """Expand a winning hook into a full narration script.

    Falls back to a template script when the OpenAI key is unavailable.
    """
    if _client and settings.OPENAI_API_KEY:
        try:
            response = _client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You write short, punchy tech-news video scripts under 60 seconds. "
                            "No stage directions – just the narration text."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Write a full narration script starting with: \"{hook}\"\n"
                            f"Topic context: {topic}\n"
                            "Keep it under 150 words."
                        ),
                    },
                ],
                max_tokens=400,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass

    # Fallback script
    return (
        f"{hook}. "
        f"Did you know that the latest news around {topic.lower()} is completely "
        "changing the landscape? Experts are calling this a once-in-a-decade shift "
        "that could reshape the entire tech industry. The numbers are staggering and "
        "the implications are massive. Stay tuned because this story is just getting started."
    )
