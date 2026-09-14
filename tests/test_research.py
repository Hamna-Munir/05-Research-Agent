"""
tests/test_research.py
Day 32-34 — tests for planner.py, researcher.py, and evaluator.py.

Run with:
    pytest tests/test_research.py -v

Note: these tests make real API calls (Groq) and real web searches.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.planner import create_research_plan, _parse_numbered_list
from src.researcher import execute_subtask
from src.evaluator import has_required_sections, addresses_question


def test_parse_numbered_list():
    text = "1. First task\n2. Second task\n3. Third task"
    result = _parse_numbered_list(text)
    assert result == ["First task", "Second task", "Third task"]


def test_parse_numbered_list_fallback_for_unstructured_text():
    text = "This is just a plain sentence with no numbering."
    result = _parse_numbered_list(text)
    assert len(result) == 1


def test_create_research_plan_returns_multiple_subtasks():
    plan = create_research_plan("Should a startup use AI agents for customer support?")
    assert isinstance(plan, list)
    assert len(plan) >= 3  # allow some flexibility below the ideal 5-7


def test_execute_subtask_returns_expected_structure():
    result = execute_subtask("What is RAG in AI?", max_results=2)
    assert "subtask" in result
    assert "summary" in result
    assert "sources" in result
    assert isinstance(result["sources"], list)


def test_has_required_sections_true_for_full_report():
    report = """## Executive Summary
    Text here.
    ## Key Findings
    Text here.
    ## Evidence
    Text here.
    ## Sources
    Text here.
    ## Limitations
    Text here.
    ## Recommendation
    Text here."""
    assert has_required_sections(report) is True


def test_has_required_sections_false_for_incomplete_report():
    report = "## Executive Summary\nJust a summary, nothing else."
    assert has_required_sections(report) is False


def test_addresses_question_true_for_relevant_report():
    question = "What are the benefits of remote work?"
    report = "Remote work offers benefits such as flexibility and reduced commute time."
    assert addresses_question(report, question) is True


def test_addresses_question_false_for_unrelated_report():
    question = "What are the benefits of remote work?"
    report = "The weather today is sunny with a high of 75 degrees."
    assert addresses_question(report, question) is False
