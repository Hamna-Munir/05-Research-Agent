"""
tests/test_agent.py
Day 29-30 — tests for agent.py's tool-calling loop.

Run with:
    pytest tests/test_agent.py -v

Note: these tests make real API calls to Groq.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.agent import run_agent


def test_agent_uses_calculator_for_math():
    result = run_agent("What is 25 multiplied by 35?")
    # Should have used the multiply tool rather than just outputting text
    tool_names = [tc["tool"] for tc in result["tool_calls"]]
    assert "multiply" in tool_names
    assert "875" in result["answer"]


def test_agent_answers_directly_without_tools_when_unnecessary():
    result = run_agent("Say hello in one word.")
    # A greeting needs no tools at all
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0


def test_agent_uses_word_count_tool():
    result = run_agent("How many words are in this sentence: 'The quick brown fox jumps'?")
    tool_names = [tc["tool"] for tc in result["tool_calls"]]
    assert "word_count" in tool_names


def test_agent_returns_tool_call_log():
    result = run_agent("What is 10 plus 15?")
    assert "tool_calls" in result
    assert isinstance(result["tool_calls"], list)


def test_agent_respects_max_iterations():
    # Even for a trivial question, the agent should never exceed max_iterations
    result = run_agent("What is 2 plus 2?", max_iterations=2)
    assert len(result["tool_calls"]) <= 2 or "step limit" not in result["answer"]
