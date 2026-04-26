"""AI content generation – hooks and scripts.

Provider priority (configurable via LLM_PROVIDER env var):
  1. OpenAI GPT-4  – paid, highest quality
  2. Ollama        – FREE, runs locally (Llama 3, Mistral, etc.)
  3. Template fallback
"""

import httpx

from core.config import settings

# --- OpenAI client (lazy init) -------------------------------------------
_openai_client = None


def _get_openai_client():
    global _openai_client
    if _openai_client is not None:
        return _openai_client
    if not settings.OPENAI_API_KEY:
        return None
    try:
        from openai import OpenAI
        _openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return _openai_client
    except Exception:
        return None


# --- Ollama helper -------------------------------------------------------

def _ollama_chat(messages: list[dict], max_tokens: int = 400) -> str | None:
    """Call a local Ollama instance. Returns the response text or None."""
    try:
        resp = httpx.post(
            f"{settings.OLLAMA_BASE_URL}/api/chat",
            json={
                "model": settings.OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
                "options": {"num_predict": max_tokens},
            },
            timeout=120.0,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"].strip()
    except Exception:
        return None


# --- Public API ----------------------------------------------------------

def generate_hooks(topic: str, count: int = 3) -> list[str]:
    """Generate A/B test hooks for a given topic.

    Tries OpenAI → Ollama → template fallback.
    """
    provider = settings.LLM_PROVIDER.lower()
    system_msg = (
        "You are a viral content strategist. Generate short, "
        "punchy hooks optimised for 3-second retention on TikTok / Reels."
    )
    user_msg = (
        f"Create {count} alternative hooks for this trending topic: {topic}. "
        "Return only the hooks, one per line."
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]

    # --- OpenAI ---
    if provider in ("auto", "openai"):
        client = _get_openai_client()
        if client:
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
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

    # --- Ollama (free) ---
    if provider in ("auto", "ollama"):
        text = _ollama_chat(messages, max_tokens=200)
        if text:
            hooks = [line.strip() for line in text.split("\n") if line.strip()]
            # Strip numbering like "1. " or "- "
            cleaned = []
            for h in hooks:
                for prefix in ("1.", "2.", "3.", "- ", "* "):
                    if h.startswith(prefix):
                        h = h[len(prefix):].strip()
                        break
                if h:
                    cleaned.append(h)
            if cleaned:
                return cleaned[:count]

    # --- Template fallback ---
    return [
        f"This changes everything for: {topic}",
        f"Nobody is talking about the truth behind: {topic}",
        f"Look at the numbers behind: {topic}",
    ]


def generate_script(hook: str, topic: str) -> str:
    """Expand a winning hook into a full narration script.

    Tries OpenAI → Ollama → template fallback.
    """
    provider = settings.LLM_PROVIDER.lower()
    system_msg = (
        "You write short, punchy tech-news video scripts under 60 seconds. "
        "No stage directions – just the narration text."
    )
    user_msg = (
        f'Write a full narration script starting with: "{hook}"\n'
        f"Topic context: {topic}\n"
        "Keep it under 150 words."
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]

    # --- OpenAI ---
    if provider in ("auto", "openai"):
        client = _get_openai_client()
        if client:
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    max_tokens=400,
                    temperature=0.7,
                )
                return response.choices[0].message.content.strip()
            except Exception:
                pass

    # --- Ollama (free) ---
    if provider in ("auto", "ollama"):
        text = _ollama_chat(messages, max_tokens=400)
        if text:
            return text

    # --- Template fallback ---
    return (
        f"{hook}. "
        f"Did you know that the latest news around {topic.lower()} is completely "
        "changing the landscape? Experts are calling this a once-in-a-decade shift "
        "that could reshape the entire tech industry. The numbers are staggering and "
        "the implications are massive. Stay tuned because this story is just getting started."
    )
