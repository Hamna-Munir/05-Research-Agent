"""
planner.py
Day 32 — Task decomposition: breaks a complex research question into
5-7 smaller, specific subtasks before any research is executed.
"""

import re
from openai import OpenAI
from src.config import GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL
from src.prompts import PLANNER_SYSTEM_PROMPT, build_planning_prompt

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


def create_research_plan(research_question: str) -> list[str]:
    """
    Generates a numbered list of research subtasks for a given question.

    Args:
        research_question: the user's original research question.

    Returns:
        A list of subtask strings (5-7 items, typically).
    """
    prompt = build_planning_prompt(research_question)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    raw_text = response.choices[0].message.content
    return _parse_numbered_list(raw_text)


def _parse_numbered_list(text: str) -> list[str]:
    """Extracts subtask strings from a numbered list like '1. Do X'."""
    lines = text.strip().split("\n")
    subtasks = []
    for line in lines:
        line = line.strip()
        match = re.match(r"^\d+[\.\)]\s*(.+)", line)
        if match:
            subtasks.append(match.group(1).strip())
    return subtasks if subtasks else [text.strip()]  # fallback: treat whole response as one task
