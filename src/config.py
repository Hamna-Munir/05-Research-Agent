"""
config.py
Loads environment variables (API keys, settings).
Configured for Groq (groq.com) — OpenAI-compatible API.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "openai/gpt-oss-120b"

if not GROQ_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Did you add your Groq key to .env?")
